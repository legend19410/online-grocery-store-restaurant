from app import encrypter
class AccountManager:

    def __init__(self, customer_access, MLManager, orderAccess):
        self.MLManager = MLManager
        self.customer_access = customer_access
        self.orderAccess = orderAccess

    def createAccount(self, request):

        """extract details from the request"""
        getParam = self.getRequestType(request)
        firstName = getParam('first_name')
        lastName = getParam('last_name')
        telephone = getParam('telephone')
        email = getParam('email')
        gender = getParam('gender')
        password = getParam('password')
        town = getParam('town')
        parish = getParam('parish')

        """sanitize and verify details"""

        """create account with sanitized data"""
        customer = self.customer_access.registerCustomer(firstName, lastName, telephone, email, password, town, parish)
        if customer:
            return True
        return False

    def login(self, request):

        getParam = self.getRequestType(request)
        email = getParam('email')
        password = getParam('password')
        
        """sanitize email and password"""

        """get the customer's account"""
        customer = self.customer_access.login(email, password)
        if customer:
            return {
                "cust_id": str(customer.id),
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'telephone': customer.telephone,
                'town': customer.town,
                'parish': customer.parish
            }
        return False

    def getCustomer(self, customerId):

        customer = self.customer_access.getCustomerById(int(customerId))
        if customer:
            return self.__getCustomerDetails(customer)
        return False


    def updateAccount(self, request, user):

        getParam = self.getRequestType(request)
        customerId = user['cust_id']
        attribute = getParam('attribute')
        value = getParam('value')

        '''validate and sanitize data'''
        
        '''perform update'''
        customer = self.customer_access.updateAccount(int(customerId), attribute, value)
        if customer:
            return self.__getCustomerDetails(customer)
        return False

    def setDeliveryLocation(self, user, request, order_id):
        getParam = self.getRequestType(request)
        street = getParam('street')
        parish = getParam('parish')
        town = getParam('town')
        cust_id = user['cust_id']
        

        order = self.orderAccess.setDeliveryLocation(int(cust_id),int(order_id),street,parish,town)
        if order:
            emp = order.employee

            if emp:
                empName = (encrypter.decrypt(emp.first_name) + " " + encrypter.decrypt(emp.last_name))
            else:
                empName = 'False'
            return self.__getOrderDetails(order,empName)
        return False


    def getRecommendedGroceries(self, custId):
        groceries = ''
        if self.customer_access.getCustomerById(custId):
            groceries = self.MLManager.getRecommendGroceries(custId)
            if groceries:
                return str(groceries)
            return False
        raise NameError

        
    def cancelOrder(self,user, order_id):
        orderId = int(order_id)
        custId = user['cust_id']
        
        cancelled_order = self.orderAccess.cancelOrder(int(custId), orderId)
        if cancelled_order:
            emp = cancelled_order.employee
 
            if emp:
                empName = (encrypter.decrypt(emp.first_name) + " " + encrypter.decrypt(emp.last_name))
            else:
                empName = 'False'
            return self.__getOrderDetails(cancelled_order, empName)
        return False

        
    def getMyOrders(self, user, request):
        getParam = self.getRequestType(request)
        status = getParam('status')

        order_start_date = getParam('order_start_date')
        if order_start_date is not None:
            order_start_date = order_start_date + " 00:00:00"
        
        order_end_date = getParam('order_end_date')
        if order_end_date is not None:
            order_end_date = order_end_date+" 23:59:59"

        delivery_start_date = getParam('delivery_start_date')
        if delivery_start_date is not None:
            delivery_start_date = delivery_start_date + " 00:00:00"
        
        delivery_end_date = getParam('delivery_end_date')
        if delivery_end_date is not None:
            delivery_end_date = delivery_end_date + " 23:59:59"

        delivery_town = getParam('delivery_town')
        delivery_parish = getParam('delivery_parish')
        
        cust_id = user['cust_id']

        orders = self.orderAccess.getOrders(cust_id, status, order_start_date, order_end_date,\
                                                    delivery_start_date, delivery_end_date, delivery_town,\
                                                    delivery_parish)
        response = []
        if orders:
            print('Orders',orders)
            for order in orders:
                emp = order.employee
                if emp:
                    empName = (encrypter.decrypt(empFname.first_name) + " " + encrypter.decrypt(empLname.last_name))
                else:
                    empName = 'False'
                response.append(
                    {
                        'order_id':str(order.id),
                        'summary':self.__getOrderDetails(order, empName),
                        'items': self.__getOrderItemsDetails(order.id)
                    }
                )
        return response



    def __getCustomerDetails(self, customer):

        return {
            "cust_id": str(customer.id),
            'first_name': encrypter.decrypt(customer.first_name),
            'last_name': encrypter.decrypt(customer.last_name),
            'telephone': encrypter.decrypt(customer.telephone),
            'email': encrypter.decrypt(customer.email),
            'town': encrypter.decrypt(customer.town),
            'parish': encrypter.decrypt(customer.parish)
        }

    def __getOrderDetails(self, order,empName):
        return {
            'order_id': str(order.id), 
            'order_date': str(order.orderdate),
            'status': encrypter.decrypt(str(order.status)), 
            'customer_id': str(order.customer_id),
            'customer': (encrypter.decrypt(order.customer.first_name) + " " + encrypter.decrypt(order.customer.last_name)),
            'delivery_date': str(order.deliverydate),
            'delivery_street': encrypter.decrypt(order.deliverystreet),
            'delivery_town': encrypter.decrypt(order.deliverytown), 
            'delivery_parish': encrypter.decrypt(order.deliveryparish), 
            'checkout_by': empName,
            'total':self.orderAccess.getTotalOnOrder(order.id)
        }

    def __getOrderItemsDetails(self,orderId):
        orderItems = self.orderAccess.getItemsInOrder(orderId)
        response = []
        if orderItems:
            for grocery in orderItems:
                cost_before_tax = grocery.quantity * grocery.groceries.cost_per_unit
                GCT = self.orderAccess.getTax(grocery.grocery_id, 'GCT') * grocery.quantity
                SCT = self.orderAccess.getTax(grocery.grocery_id, 'SCT') * grocery.quantity
                total = float(cost_before_tax) + float(GCT) + float(SCT)
                total_weight = str(grocery.quantity * grocery.groceries.grams_per_unit) + " grams"
                response.append (
                    {
                        'grocery_id': str(grocery.grocery_id),
                        'quantity': str(grocery.quantity),
                        'cost_before_tax': str(cost_before_tax),
                        'sku': encrypter.decrypt(grocery.sku),
                        'name': grocery.groceries.name,
                        'total_weight': total_weight,
                        'GCT': str(GCT),
                        'SCT': str(SCT),
                        'total': str(total)
                    }
                )
            return response
        else:
            return {orderId:'no groceries on order'}

    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get