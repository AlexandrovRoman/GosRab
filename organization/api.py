from flask import jsonify
from flask_restful import reqparse
from app.api_utils import get_or_abort
from organization.models import Organization, Vacancy
from app.BaseAPI import BasicResource


def get_or_abort_org(org_id):
    return get_or_abort(org_id, Organization)


class OrganizationResource(BasicResource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True)
    parser.add_argument('org_type', required=True)
    parser.add_argument('org_desc', required=True)

    def get(self, org_id):
        self.set_authorized_user()
        if not self.authorized_user:
            return self.basic_error('Login before using API')

        org = get_or_abort_org(org_id)
        response_info = org.to_dict(
            only=('id', 'name', 'creation_date', 'owner_id', 'org_type', 'org_desc'))
        response_info['free_vacancies'] = [vac.to_dict(only=('id', 'salary', 'title', 'org_id'))
                                           for vac in org.vacancies if vac.worker_id is None]
        if self.authorized_user.id == org.owner_id:
            response_info['staff'] = [vac.to_dict(only=('id', 'salary', 'title', 'org_id', 'resume', 'worker_id'))
                                      for vac in org.vacancies if vac.worker_id is not None]
        return jsonify({'organization': response_info})

    def delete(self, org_id):
        self.set_authorized_user()
        if not self.authorized_user:
            return self.basic_error('Login before using API')

        org = get_or_abort_org(org_id)
        if self.authorized_user.id != org.owner_id:
            return self.basic_error('delete is not allowed to this organization')
        org.delete()
        return jsonify({'deleting': 'OK'})

    def post(self):
        self.set_authorized_user()
        if not self.authorized_user:
            return self.basic_error('Login before using API')

        args = self.parser.parse_args()
        org = Organization.new(
            name=args['name'],
            owner_id=self.authorized_user.id,
            org_type=args['org_type'],
            org_desc=args['org_desc']
        )
        org.save(add=True)
        return jsonify({'adding': 'OK'})


class VacancyListResource(BasicResource):
    def get(self):
        self.set_authorized_user()
        if not self.authorized_user:
            return self.basic_error('Login before using API')
        vacancies = Vacancy.all().filter_by(worker_id=None)
        return jsonify({'vacancy': [vac.to_dict(
            only=('id', 'salary', 'title', 'org_id')) for vac in vacancies]})
