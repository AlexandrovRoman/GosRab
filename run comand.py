from app.__init__ import db
from app.__init__ import user_datastore

user_datastore.create_user(email='qqq@gmail.com', name='me', surname='meee', midlename='my')
db.session.commit()
from users.models import User
user = User.query.first()
print(user.id, user.email, user.name, user.midlename, user.surname)