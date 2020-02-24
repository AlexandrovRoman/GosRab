from app import create_session, login_manager
from datetime import datetime
from organisations.models import Organisation
from users.models import User

def organistion_add(name, personnel_id, date=datetime.now):
    session = create_session()
    org = Organisation()
    org.name = name
    org.personnel_id = personnel_id
    org.personnel = session.query(User).filter(User.id == personnel_id).first()
    org.date = date
    session.add(org)
    session.commit()