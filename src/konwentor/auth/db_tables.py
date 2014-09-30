from haplugin.sql import Base
from sqlalchemy import Column, Integer, ForeignKey, Table

users_2_permissions = Table(
    'users_2_permissions', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)
