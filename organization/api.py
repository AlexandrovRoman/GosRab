from flask import jsonify
from flask_restful import reqparse
from app.api_utils import get_or_abort
from organization.models import Organization, Vacancy
from app.BaseAPI import BasicResource, jwt_login_required, jwt_org_required


def get_or_abort_org(org_id):
    return get_or_abort(org_id, Organization)


class OrganizationResource(BasicResource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True)
    parser.add_argument('org_type', required=True)
    parser.add_argument('org_desc', required=True)

    @jwt_org_required
    def get(self):
        self.set_authorized_org()
        response_info = self.authorized_org.to_dict(
            only=('id', 'name', 'creation_date', 'owner_id', 'org_type', 'org_desc', 'api_token'))
        vacancies = self.authorized_org.vacancies
        response_info['free_vacancies'] = [vac.to_dict(only=('id', 'salary', 'title', 'org_id'))
                                           for vac in vacancies if vac.worker_id is None]
        response_info['staff'] = [
            vac.to_dict(only=('id', 'salary', 'title', 'org_id', 'resume', 'worker_id'))
            for vac in vacancies if vac.worker_id is not None]
        return jsonify({'organization': response_info})

    @jwt_org_required
    def delete(self):
        self.set_authorized_org()
        self.authorized_org.delete()
        return jsonify({'deleting': 'OK'})

    @jwt_login_required
    def post(self):
        args = self.parser.parse_args()
        org = Organization(
            name=args['name'],
            owner_id=self.authorized_user.id,
            org_type=args['org_type'],
            org_desc=args['org_desc']
        )
        org.save(add=True)
        return jsonify({'adding': 'OK',
                        'organization': org.to_dict(
                            only=('id', 'name', 'creation_date', 'owner_id', 'org_type', 'org_desc', 'api_token'))})


class VacancyListResource(BasicResource):
    parser = reqparse.RequestParser()
    parser.add_argument('offset')

    @jwt_login_required
    def get(self):
        args = self.parser.parse_args()
        offset = 0
        if args['offset']:
            offset = abs(int(args['offset']))
        vacancies = Vacancy.get_by(worker_id=None).all(offset=offset)
        return jsonify({'vacancy': [vac.to_dict(only=('id', 'salary', 'title', 'org_id')) for vac in vacancies]})
