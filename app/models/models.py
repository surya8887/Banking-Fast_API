from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, date
from pydantic import EmailStr
from enum import Enum

#  Model for Banking
# <=====================================================> 
class AccountTypeEnum(str, Enum):
    savings = "savings"
    current = "current"
    joint = "joint"

class LoanTypeEnum(str, Enum):
    home = "home"
    personal = "personal"
    education = "education"
    vehicle = "vehicle"
    business = "business"

class PaymentMethodEnum(str, Enum):
    cash = "cash"
    cheque = "cheque"
    online = "online"
    upi = "upi"

class TransactionTypeEnum(str, Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"
    transfer = "transfer"

class EmployeePositionEnum(str, Enum):
    manager = "manager"
    cashier = "cashier"
    clerk = "clerk"
    executive = "executive"
    loan_officer = "loan_officer"

class UserRoleEnum(str, Enum):
    admin = "admin"
    employee = "employee"
    customer = "customer"
# /------------------

# User
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: Optional[str] = Field(index=True, nullable=False)
    email: EmailStr = Field(index=True, nullable=False)
    password_hash: Optional[str]
    role: Optional[UserRoleEnum ]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

# Customer
class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    photo: Optional[str] = None
    name: str
    dob: Optional[date] = None
    phone_no: Optional[str] = None
    address: Optional[str] = None
    aadhar_card: str = Field(index=True, nullable=False)
    kyc_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Branch
class Branch(SQLModel, table=True):
    ifsc_code: str = Field(primary_key=True)
    branch_name: str
    location: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Employee
class Employee(SQLModel, table=True):
    emp_id: str = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str
    dob: Optional[date] = None
    email: EmailStr = Field(index=True)
    phone_number: Optional[str] = None
    salary: float
    position: EmployeePositionEnum
    branch_ifsc: str = Field(foreign_key="branch.ifsc_code")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Account
class Account(SQLModel, table=True):
    account_number: Optional[int] = Field(default=None, primary_key=True)
    account_type: AccountTypeEnum
    ifsc_code: str = Field(foreign_key="branch.ifsc_code")
    balance: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

# Joint Account Mapping
class AccountHolder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    account_number: int = Field(foreign_key="account.account_number")
    customer_id: int = Field(foreign_key="customer.id")
    ownership_percent: int

# Savings Account
class Savings(SQLModel, table=True):
    account_number: int = Field(primary_key=True, foreign_key="account.account_number")
    interest_rate: float

# Current Account
class Current(SQLModel, table=True):
    account_number: int = Field(primary_key=True, foreign_key="account.account_number")
    interest_rate: float

# Loan
class Loan(SQLModel, table=True):
    loan_id: str = Field(primary_key=True)
    account_id: int = Field(foreign_key="account.account_number")
    cust_id: int = Field(foreign_key="customer.id")
    amount: float
    loan_type: LoanTypeEnum
    tenure_months: int
    issued_at: datetime = Field(default_factory=datetime.utcnow)
    is_approved: bool = Field(default=False)

# Payment
class Payment(SQLModel, table=True):
    payment_id: Optional[int] = Field(default=None, primary_key=True)
    loan_id: str = Field(foreign_key="loan.loan_id")
    cust_id: int = Field(foreign_key="customer.id")
    amount: float
    method: PaymentMethodEnum
    date_time: datetime = Field(default_factory=datetime.utcnow)

# Transaction
class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    account_id: int = Field(foreign_key="account.account_number")
    amount: float
    method: PaymentMethodEnum
    transaction_type: TransactionTypeEnum
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    description: Optional[str] = None
