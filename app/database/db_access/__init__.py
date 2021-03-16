from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .BranchAccess import BranchAccess
from .CartAccess import CartAccess
from .CustomerAccess import CustomerAccess
from .EmployeeAccess import EmployeeAccess
from .GroceryAccess import GroceryAccess
from .OrderAccess import OrderAccess
from .OrderGroceriesAccess import OrderGroceriesAccess
from .PaymentAccess import PaymentAccess

branch_access = BranchAccess()
customer_access = CustomerAccess()
employee_access = EmployeeAccess
grocery_access = GroceryAccess()
order_access = OrderAccess()
cart_access = CartAccess(grocery_access, order_access, customer_access)
order_groceries_access = OrderGroceriesAccess()
payment_access = PaymentAccess()