import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Message(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'message'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    from_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"), nullable=False, index=True)
    to_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"), nullable=True, index=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_friend = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    from_user = orm.relation('User', foreign_keys=[from_id])
    to_user = orm.relation('User', foreign_keys=[to_id])
