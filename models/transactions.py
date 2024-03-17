from models.base import Base
from sqlalchemy import Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import func
from models.accounts import Account

class Transaction(Base):
    __tablename__ = "transactions"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_account_id = mapped_column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"))
    to_account_id = mapped_column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"))
    amount = mapped_column(DECIMAL(precision=10, scale=2))
    type = mapped_column(String(255), nullable= False)
    description = mapped_column(String(255), nullable= False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # accounts = relationship("accounts", cascade="all,delete-orphan")

    def __repr__(self):
        return f'<Transaction {self.type}>'
    
    def serialize(self, full=True):
        if full:
            return {
                'id': self.id,
                'from_account_id': self.from_account_id,
                'to_account_id': self.to_account_id,
                'amount': self.amount,
                'type': self.type,
                'description': self.description,
                'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        else:
            return {
                'id': self.id,
                'type': self.type,
                'description': self.description,
                'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }