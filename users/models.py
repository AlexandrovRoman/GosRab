from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=True)
    surname = db.Column(db.String(80), nullable=True)
    fathername = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(40),
                      index=True, unique=True, nullable=True)
    hashed_password = db.Column(db.String, nullable=True)
    # birth_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String, nullable=True,
                       default='standart_user')  # standart_user, admin, organistaion, superuser

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

# session = create_session()
# for i in range(1, 5):
#     user = User()
#     user.name = f"Имя {i}"
#     user.surname = f'Фамилия {i}'
#     user.fathername = f'Отчество {i}'
#     user.email = f"email{i}@email.ru"
#     user.set_password(f'password_{i}')
#     # user.birth_date = datetime.date(1998, 7, i)
#     session.add(user)
#     session.commit()
