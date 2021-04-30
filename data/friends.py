import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Friend(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'friend'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    from_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"), nullable=False, index=True)
    to_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"), nullable=False, index=True)
    from_user = orm.relation('User', foreign_keys=[from_id])
    to_user = orm.relation('User', foreign_keys=[to_id])
