
class RatingManager:
    def __init__(self, rating_access):
        self.rating_access = rating_access

    def rateGrocery(self, user, request):
        try:
            getParam = self.getRequestType(request)
            custId = user['cust_id']
            itemId = getParam('item_id')
            rating = getParam('rating')

            rating = self.rating_access.rateGrocery(int(custId),int(itemId), int(rating))
            if rating:
                return self.__getRatingDetails(rating)
            else:
                return {'msg':'operation could not be completed'}
        except:
            return {'msg':'failed request'}

    def getAllMyRating(self,user):
        try:
            custId = user['cust_id']

            response = {}
            ratings = self.rating_access.getAllMyRating(int(custId))
            if ratings:
                for rating in ratings:
                    response[rating.cust_id] = self.__getRatingDetails(rating)
                return response
            else:
                return {'msg':'you have not rated any of the existing groceries'}
        except:
            return {'msg':'failed request'}

    def getDataFrame(self):
        return self.rating_access.getDataFrame()

    def __getRatingDetails(self,rating):
        return {'customer_id':rating.cust_id,'customer_name':(rating.customer_ratings.first_name+" "+\
                        rating.customer_ratings.last_name), 'grocery_name':rating.grocery_ratings.name,\
                        'grocery_id':rating.item_id,'rating':rating.rating}

    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get

