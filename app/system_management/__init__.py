from ..database.db_access import branch_access,customer_access,employee_access,\
                                 grocery_access, order_access, cart_access,order_groceries_access,\
                                 payment_access
from CartManager import CartManager
from CustomerAccountManager import AccountManager
from EmployeeAccountManager import EmployeeAccountManager
from GroceryManager import GroceryManager
from OrderManager import OrderManger


grocery_manager = GroceryManager(grocery_access)#object used to manipulate all grocery operations
#order_manager = OrderManager()
cart_manager = CartManager(cart_access)
customer_manager = AccountManager(customer_access) #create an object that manages all operations on a customer's account
employee_manager = EmployeeAccountManager(employee_access)#create an object that manage all operations on an employee account
