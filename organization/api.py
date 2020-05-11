from flask import jsonify
from flask_restful import reqparse
from app.api_utils import get_or_abort
from app.tokens import check_tokens
from organization.models import Organization, Vacancy
from app.BaseAPI import BasicResource, jwt_login_required


def get_or_abort_org(org_id):
    return get_or_abort(org_id, Organization)


class OrganizationResource(BasicResource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True)
    parser.add_argument('org_type', required=True)
    parser.add_argument('org_desc', required=True)

    @jwt_login_required
    def get(self, org_id):
        org = get_or_abort_org(org_id)
        response_info = org.to_dict(
            only=('id', 'name', 'creation_date', 'owner_id', 'org_type', 'org_desc'))
        vacancies = org.vacancies
        response_info['free_vacancies'] = [vac.to_dict(only=('id', 'salary', 'title', 'org_id'))
                                           for vac in vacancies if vac.worker_id is None]
        if self.authorized_user.id == org.owner_id:
            response_info['staff'] = [
                vac.to_dict(only=('id', 'salary', 'title', 'org_id', 'resume', 'worker_id'))
                for vac in vacancies if vac.worker_id is not None]
            response_info['api_token'] =  org.api_token
        return jsonify({'organization': response_info})

    @jwt_login_required
    def delete(self, org_id, org_token):
        org = get_or_abort_org(org_id)
        self.set_authorized_user()

        if not check_tokens(org.api_token, org_token):
            return self.basic_error('delete is not allowed to this organization')
        org.delete()
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

    @jwt_login_required
    def get(self, offset=0):
        vacancies = Vacancy.all(offset=offset).filter_by(worker_id=None)
        return jsonify({'vacancy': [vac.to_dict(only=('id', 'salary', 'title', 'org_id')) for vac in vacancies]})
