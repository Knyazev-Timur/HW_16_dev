from flask import Flask
import json

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


app = Flask (__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    first_name =db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer,db.CheckConstraint("age > 0"))
    email = db.Column(db.String(100), nullable=False)
    # role_id =db.Column(db.Integer, db.ForeignKey("role.id"))
    # role = relationship("Role")
    role = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))



# class Role(db.Model):
#     __tablename__ = "role"
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200))
#
#     users = relationship("User")

#
# class Offer(db.Model):
#     __tablename__ = "offer"
#     id = db.Column(db.Integer,  primary_key=True)
#     order_id = db.Column(db.Integer, nullable=False)
#     # executor_id = db.Column(db.Integer, db.ForeignKey())
#
#
#
#
#
# class Order(db.Model):
#     __tablename__ = "order"
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.String(300), nullable=False)
#     start_date = db.Column(db.Date)
#     end_date = db.Column(db.Date)
#     address = db.Column(db.String(200), nullable=False)
#     price = db.Column(db.Integer)
#     customer_id = db.Column(db.Integer)
#     executor_id = db.Column(db.Integer)


# offer = Role(id=1, name="Offer")
# user_01=User(id=1, first_name="Jhon", last_name="Lennon", age=200, email="jl@yahoo.com", role=offer, phone="+1234567899")


def read_json(file_name):
    with open(file_name, "r", encoding='UTF-8') as read_file:
        return json.load(read_file)


def users_model():
    users=read_json("data/users.json")

    for index, user in enumerate(users):
        user_name=f'user_{index+1}'
        # if user.get("role") == "executor":
        #     role_user = Role(id=1, name="executor")
        # elif user.get("role") =="customer":
        #     role_user = Role(id=2, name="customer")
        user_name=User(id=user.get("id"), first_name=user.get("first_name"), last_name=user.get("last_name"), age=user.get("age"), email=user.get("email"), role=user.get("role"), phone=user.get("phone"))

        with app.app_context():
            db.session.add(user_name)
            db.session.commit()


def get_all_users():
    with app.app_context():
        all_users=User.query.all()

        for user in all_users:
            first_name = user.first_name
            last_name = user.last_name
            role = user.role
            print(first_name, last_name, role)


with app.app_context():
    db.create_all()

users_model()

if __name__ == "__main__":
    app.run(debug=True)