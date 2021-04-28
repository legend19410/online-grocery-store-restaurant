class GroceryManager:
    def __init__(self, grocery_access):
        self.grocery_access = grocery_access
        
    def addGrocery(self, request):

        try:
            getParam = self.getRequestType(request)
            name = getParam('grocery_name')
            description = getParam('description')
            quantity = getParam('quantity')
            price = getParam('price')
            units = getParam('units')
            grams_per_unit = getParam('grams_per_unit')
            category = getParam('category')

            """validate the data"""

            """add grocery item to stock"""
            grocery = self.grocery_access.create_grocery(name, description, int(quantity), units, float(price), float(grams_per_unit),category)
            if grocery:
                return {'msg':'success', 'data':{'grocery':self.__getGroceryDetails(grocery)}}, 200
            else:
                return {'msg':'request to create new grocery item failed', 'error':'create-0001'}, 404
        except Exception as e:
            print(e)
            return {'msg':'request failed', 'error':'ise-0001'}, 500

    def updateGrocery(self, request):

        try:
            getParam = self.getRequestType(request)
            groceryId = getParam('grocery_id')
            attribute = getParam('attribute')
            value = getParam('value')

            '''validate and sanitize data'''

            '''perform update'''
            grocery = self.grocery_access.updateGrocery(groceryId, attribute, value)
            if grocery:
                return {'msg':'success', 'data':{'grocery':self.__getGroceryDetails(grocery)}}, 200
            else:
                return {'msg':'update failed', 'error':'create-0001'}, 404
        except Exception as e:
            print(e)
            return {'msg':'request failed', 'error':'ise-0001'}, 500

    def deleteGrocery(self, request):

        try:
            getParam = self.getRequestType(request)
            groceryId = getParam('grocery_id')

            '''validate and sanitize data'''

            '''remove grocery from db'''
            groceries = self.grocery_access.removeGroceryItem(int(groceryId))
            response = []
            if groceries:
                for grocery in groceries:
                    {'msg':'success', 'data':{'groceries':response.append(self.__getGroceryDetails(grocery))}}, 200
                return response
            else:
                return {'msg':'no groceries in stock', 'data':{}}, 200
        except Exception as e:
            print(e)
            return {'msg':'request failed', 'error':'ise-0001'}, 500

    def getGroceries(self, request):

        try:
            groceries = self.grocery_access.getGroceries()
            response = []
            if groceries:
                for grocery in groceries:
                    response.append(self.__getGroceryDetails(grocery))
                return {'msg':'success', 'data':{'groceries':response}},200
            else:
                return {'msg':'no grocery found', 'data':{}}, 200
        except Exception as e:
            print (e)
            return {'msg':'request failed', 'error':'ise-0001'}, 500

    def getGroceriesByCategory(self, request):

        try:
            getParam = self.getRequestType(request)
            category = getParam('category')

            groceries = self.grocery_access.getGroceriesByCategory(category)
            response = []
            if groceries:
                for grocery in groceries:
                    response.append(self.__getGroceryDetails(grocery))
                return {'msg':'success', 'data':{'groceries':response}}, 200
            else:
                return {'msg':'no grocery found', 'data':{}}, 200
        except Exception as e:
            print(e)
            return {'msg':'request failed', 'error':'ise-0001'}, 500

    def getGrocery(self, request):

        try:
            getParam = self.getRequestType(request)
            groceryId = getParam('grocery_id')

            grocery = self.grocery_access.searchForGrocery(int(groceryId))
            if grocery:
                return {'msg':'success', 'data':{'grocery':self.__getGroceryDetails(grocery)}}, 200
            else:
                return {'msg':'no grocery found', 'data':{}}, 200
        except Exception as e:
            print(e)
            return {'msg':'request failed', 'error':'ise-0001'}, 500

    def __getGroceryDetails(self, grocery):

        return {'id': str(grocery.id), 'name': grocery.name, 'description': grocery.description, \
                        'quantity': str(grocery.quantity), 'units': grocery.units, \
                        'cost_per_unit': str(grocery.cost_per_unit), 'grams_per_unit':str(grocery.grams_per_unit),\
                'category':grocery.category}


    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get
