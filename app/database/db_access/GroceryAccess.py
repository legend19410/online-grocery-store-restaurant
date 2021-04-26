from ... import db
from ..Models import Grocery
from ..Models import Taxes
from ..Models import Taxes_on_goods
from sqlalchemy import and_, or_, not_

class GroceryAccess:

    def create_grocery(self, name, description, quantity, units, price, grams_per_unit,category):

        grocery = Grocery(name=name, description=description, quantity=quantity, units=units, cost_per_unit=price,\
                          grams_per_unit=grams_per_unit,category=category)
        db.session.add(grocery)
        db.session.commit()
        return self.searchForGrocery(grocery.id)

    def updateGrocery(self, groceryId, attribute, value):

        grocery = self.searchForGrocery(groceryId)
        if grocery:
            if attribute == 'name':
                grocery.name = value
                db.session.commit()
                return self.searchForGrocery(groceryId)
            if attribute == 'description':
                grocery.description = value
                db.session.commit()
                return self.searchForGrocery(groceryId)
            if attribute == 'quantity':
                grocery.quantity = int(value)
                db.session.commit()
                return self.searchForGrocery(groceryId)
            if attribute == 'units':
                grocery.units = value
                db.session.commit()
                return self.searchForGrocery(groceryId)
            if attribute == 'cost_per_unit':
                grocery.cost_per_unit = float(value)
                db.session.commit()
                return self.searchForGrocery(groceryId)
            if attribute == 'grams_per_unit':
                grocery.grams_per_unit = float(value)
                db.session.commit()
                return self.searchForGrocery(groceryId)
            if attribute == 'category':
                grocery.category = value
                db.session.commit()
                return self.searchForGrocery(groceryId)
        return False

    def searchForGrocery(self, grocery_id):
        grocery = Grocery.query.filter_by(id=grocery_id).first()
        try:
            if grocery.id:
                return grocery
            else:
                return False
        except:
            return False

    def getGroceries(self):
        groceries = Grocery.query.filter_by().all()
        try:
            if groceries[0].name:
                return groceries
        except:
            return False

    def getGroceriesByCategory(self,category):
        groceries = Grocery.query.filter_by(category=category).all()
        try:
            if groceries[0].name:
                return groceries
        except:
            return False

    def removeGroceryItem(self, groceryId):

        grocery = self.searchForGrocery(groceryId)
        if grocery:
            db.session.delete(grocery)
            db.session.commit()
        return self.getGroceries()
    
    def getTaxType(self, groceryId, type):
        grocery = self.searchForGrocery(groceryId)
        if grocery:
            tax = Taxes_on_goods.query.filter(and_(Taxes_on_goods.tax.like(type), Taxes_on_goods.grocery_id.like(groceryId))).first()
            try:
                if tax.grocery_id:
                    return tax
            except:
                return False
        else:
            return False
    
    def getTax(self, groceryId, type):
        taxOnItem = self.getTaxType(groceryId, type)
        if taxOnItem:
            return float(taxOnItem.tax_type.rate) * float(taxOnItem.grocery.cost_per_unit)
        else:
            return 0



