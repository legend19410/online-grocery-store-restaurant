from ... import db
from ..Models import Customer
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

class CustomerAccess:

    """retrieve a customer record from the database given their email and password"""
    def login(self, email, password):
        customer = Customer.query.filter_by(email=email).first()
        if customer is not None and check_password_hash(customer.password, password):
            return customer
        else:
            return False

    """register a customer to the db"""
    def registerCustomer(self, firstName, lastName, telephone, email, password, town, parish):
        customer = {}
        try:
            customer = Customer(first_name, last_name, telephone, email, gender, password, parish)
            db.session.add(customer)
            db.session.commit()
            customer = self.getCustomerById(customer.id)
            return customer
        except IntegrityError as e:
            db.session.rollback()
            return False

    def getCustomerById(self, id):
        customer = Customer.query.filter_by(id=id).first()
        try:
            if customer.id == int(id):
                print(customer)
                return customer
            else:
                return False
        except:
            return False

    def updateAccount(self, customerId, attribute, value):
        customer = self.getCustomerById(customerId)
        if customer:
            if attribute == 'first_name':
                customer.first_name = encrypter.encrypt(value)
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'last_name':
                customer.last_name = encrypter.encrypt(value)
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'telephone':
                customer.telephone = encrypter.encrypt(value)
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'email':
                customer.email = encrypter.encrypt(value)
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'gender':
                customer.gender = encrypter.encrypt(value)
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'password':
                customer.password = generate_password_hash(value, method='pbkdf2:sha256:310000', salt_length=256)
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'town':
                customer.town = encrypter.encrypt(value)
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'parish':
                customer.parish = encrypter.encrypt(value)
                db.session.commit()
                return self.getCustomerById(customerId)

        return False

    def getCart(self, cartId):

        customer = self.getCustomerById(cartId)
        if customer:
            return customer.cart_items
        else:
            return False