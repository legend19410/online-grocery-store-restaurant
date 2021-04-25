
class CartManager:

    def __init__(self, cartAccess, groceryAccess):
        self.groceryAccess = groceryAccess
        self.cartAccess = cartAccess

    def addToCart(self, request, user):

        '''extract request params'''
        getParam = self.getRequestType(request)
        cartId = user['cust_id']
        quantity = getParam('quantity')
        itemId = getParam('item_id')

        '''sanitize data'''

        '''add item to cart and return all cart items for customer'''
        cart = self.cartAccess.addToCart(int(itemId), int(cartId), int(quantity))
        response = []
        if cart:
            for grocery in cart:
                cost_before_tax = grocery.quantity * grocery.cart_items.cost_per_unit
                GCT = self.groceryAccess.getTax(grocery.item_id, 'GCT') * grocery.quantity
                SCT = self.groceryAccess.getTax(grocery.item_id, 'SCT') * grocery.quantity
                total = float(cost_before_tax) + float(GCT) + float(SCT)
                total_weight = str(grocery.quantity * grocery.cart_items.grams_per_unit) + " grams"
                response.append({'grocery_id': str(grocery.item_id),\
                                                    'quantity': str(grocery.quantity), \
                                                    'cost_before_tax': str(cost_before_tax),\
                                                    'name': grocery.cart_items.name, \
                                                    'total_weight': total_weight, 'GCT': str(GCT), 'SCT': str(SCT),\
                                                    'total': str(total)})

            return {'items':response, 'grand_total':self.cartAccess.getTotalOnCart(cartId)}
        return False


    def emptyCart(self, session):

        try:
            cartId = session['cust_id']
            isEmpty = self.cartAccess.emptyCart(int(cartId))
            if isEmpty:
                return {'msg':'cart emptied'}
            else:
                return {'msg':'operation failed'}
        except:
            return {'msg':'operation failed'}

    def removeItemFromCart(self, grocery_id, user):

        # getParam = self.getRequestType(request)
        # itemId = getParam('grocery_id')
        cartId = user['cust_id']

        cartItems = self.cartAccess.removeItem(cartId, grocery_id)
        response = {}
        if cartItems:
            for grocery in cartItems:
                cost_before_tax = grocery.quantity * grocery.cart_items.cost_per_unit
                GCT = self.groceryAccess.getTax(grocery.item_id, 'GCT') * grocery.quantity
                SCT = self.groceryAccess.getTax(grocery.item_id, 'SCT') * grocery.quantity
                total = float(cost_before_tax) + float(GCT) + float(SCT)
                total_weight = str(grocery.quantity * grocery.cart_items.grams_per_unit) + " grams"
                response[str(grocery.item_id)] = {'grocery_id': str(grocery.item_id), \
                                                    'quantity': str(grocery.quantity), \
                                                    'cost_before_tax': str(cost_before_tax), \
                                                    'name': grocery.cart_items.name, \
                                                    'total_weight': total_weight, 'GCT': str(GCT), 'SCT': str(SCT), \
                                                    'total': str(total)}
            return {'items':response, 'grand_total':self.cartAccess.getTotalOnCart(cartId)}
        return False

    def checkoutCart(self, user):

        cartId = user['cust_id']
        order = self.cartAccess.checkoutCart(int(cartId))
        if order:
            return {'order':{'order_id':str(order.id), 'order_date':order.orderDate, 'status':str(order.status), \
                    'customer_id':str(order.customer_id), 'customer':(order.customer.first_name + " "+ order.customer.last_name)}}
        return False

    def updateCartItem(self, request, user):

        getParam = self.getRequestType(request)
        itemId = getParam('item_id')
        quantity = getParam('quantity')
        cartId = user['cust_id']

        grocery = self.cartAccess.updateCartItem(int(cartId),int(itemId),int(quantity))
        if grocery:
            cost_before_tax = grocery.quantity * grocery.cart_items.cost_per_unit
            GCT = self.groceryAccess.getTax(grocery.item_id, 'GCT') * grocery.quantity
            SCT = self.groceryAccess.getTax(grocery.item_id, 'SCT') * grocery.quantity
            total = float(cost_before_tax) + float(GCT) + float(SCT)
            total_weight = str(grocery.quantity * grocery.cart_items.grams_per_unit) + " grams"
            return {'grocery_id': str(grocery.item_id), \
                                                'quantity': str(grocery.quantity), \
                                                'cost_before_tax': str(cost_before_tax), \
                                                'name': grocery.cart_items.name, \
                                                'total_weight': total_weight, 'GCT': str(GCT), 'SCT': str(SCT), \
                                                'total': str(total)}
        else:
            return False

    def getAllCartItems(self, user):

        cartId = user['cust_id']
        cartItems = self.cartAccess.getAllCartItems(cartId)
        response = []
        if cartItems:
            for grocery in cartItems:
                cost_before_tax = grocery.quantity*grocery.cart_items.cost_per_unit
                GCT = self.groceryAccess.getTax(grocery.item_id,'GCT')*grocery.quantity
                SCT = self.groceryAccess.getTax(grocery.item_id,'SCT')*grocery.quantity
                total = float(cost_before_tax) + float(GCT) + float(SCT)
                total_weight = str(grocery.quantity*grocery.cart_items.grams_per_unit)+" grams"
                response.append ({'grocery_id': str(grocery.item_id), 'quantity': str(grocery.quantity), \
                                                    'cost_before_tax': str(cost_before_tax),'name':grocery.cart_items.name,\
                                                    'total_weight':total_weight,'GCT':str(GCT),'SCT':str(SCT),'total': str(total)})
            return {'items':response, 'grand_total':self.cartAccess.getTotalOnCart(cartId)}
        return False


    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get