import jwt
from flask import jsonify, session
from flask_restful import reqparse, Resource

from app import Config
from utils.api import check_tokens, create_jwt
from users.api import BasicUserResource
from utils.api import get_or_abort, BasicResource as _BasicResource, jwt_login_required, jwt_org_required
from organization.models import Organization, Vacancy


def get_or_abort_org(org_id):
    return get_or_abort(org_id, Organization)


class OrgApiEntryPoint(Resource):
    def get(self, org_id, jwt_):
        org = Organization.get_by(id=org_id)
        if org and check_tokens(jwt_, org.api_token):
            session['current_org_jwt'] = create_jwt(org.to_dict(only=('id', 'name')))
            return jsonify({'authorization': 'OK'})
        return jsonify({'error': 'incorrect Organization ID or JWT'})

    def delete(self):
        session.pop('current_org_jwt', None)
        return jsonify({'sign out of organization': 'OK'})

    @staticmethod
    def get_authorized_org():
        try:
            return Organization.get_by(
                id=jwt.decode(session['current_org_jwt'], Config.JWT_SECRET_KEY)['payload']['id'])
        except (TypeError, KeyError):
            return None


class BasicOrgResource(_BasicResource):
    @staticmethod
    def basic_error(message):
        return jsonify({'error': message})

    def set_authorized_org(self):
        self.authorized_org = OrgApiEntryPoint.get_authorized_org()


class OrganizationResource(BasicOrgResource, BasicUserResource):
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
        org.save()
        return jsonify({'adding': 'OK',
                        'organization': org.to_dict(
                            only=('id', 'name', 'creation_date', 'owner_id', 'org_type', 'org_desc', 'api_token'))})


class VacancyListResource(BasicOrgResource, BasicUserResource):
    parser = reqparse.RequestParser()
    parser.add_argument('offset')

    @jwt_login_required
    def get(self):
        args = self.parser.parse_args()
        try:
            offset = abs(int(args.get('offset')))
        except TypeError:
            offset = 0
        vacancies = Vacancy.get_by(worker_id=None).all(offset=offset)
        return jsonify({'vacancy': [vac.to_dict(only=('id', 'salary', 'title', 'org_id')) for vac in vacancies]})
