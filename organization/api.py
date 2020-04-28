from flask import jsonify
from flask_login import current_user
from flask_restful import reqparse, Resource
from app.api import abort_obj_not_found
from organization.models import Organization


def abort_org_not_found(org_id):
    abort_obj_not_found(org_id, Organization)


class OrganizationResource(Resource):
    def get(self, org_id):
        abort_org_not_found(org_id)
        org = Organization.get(org_id)
        if org.owner_id != getattr(current_user, "id", None):
            return jsonify({'organization': 'Operation not allowed to this organization'})
        return jsonify({'organization': org.to_dict(
            only=('id', 'name', 'creation_date', 'vacancies', 'owner_id', 'org_type', 'org_desc'))})

    def delete(self, org_id):
        abort_org_not_found(org_id)
        if org_id.owner_id != getattr(current_user, "id", None):
            return jsonify({'deleting': 'Operation not allowed to this organization'})
        org = Organization.get(org_id)
        org.delete()
        return jsonify({'deleting': 'OK'})


class OrganizationListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True)
    parser.add_argument('org_type', required=True)
    parser.add_argument('org_desc', required=True)

    def get(self):
        orgs = Organization.all()
        return jsonify({'organization': [org.to_dict(
            only=('id', 'name', 'creation_date', 'vacancies', 'owner_id', 'org_type', 'org_desc')) for org in orgs]})

    def post(self):
        args = self.parser.parse_args()
        org = Organization.new(
            name=args['name'],
            owner_id=getattr(current_user, "id", None),
            org_type=args['org_type'],
            org_desc=args['org_desc']
        )
        org.save(add=True)
        return jsonify({'adding': 'OK'})
