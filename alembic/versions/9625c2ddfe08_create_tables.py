"""create tables

Revision ID: 9625c2ddfe08
Revises: 
Create Date: 2024-03-14 21:37:13.036594

"""
from typing import Sequence, Union
from models.users import User
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# revision identifiers, used by Alembic.
revision: str = '9625c2ddfe08'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(255), nullable=False, unique=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )
    op.create_table(
        'accounts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column('account_type', sa.String(200), nullable=False),
        sa.Column('account_number', sa.String(200), nullable=False, unique=True),
        sa.Column('balance', sa.DECIMAL(precision=10, scale=2)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('from_account_id', sa.Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False),
        sa.Column('to_account_id', sa.Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False),
        sa.Column('amount', sa.DECIMAL(precision=10, scale=2)),
        sa.Column('type', sa.String(255), nullable=False),
        sa.Column('description', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now())
    )

def downgrade():
    op.drop_table('users')