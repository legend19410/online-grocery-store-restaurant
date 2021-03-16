from flask import Blueprint
from flask import redirect, url_for, session, request
from ..system_management import order_manager

manage_order = Blueprint("manage_order", __name__)

@manage_order.route('/makeOrder', methods=['POST'])
def makeOrder():
    return

@manage_order.route('/scheduleOrder', methods=['POST'])
def scheduleOrder():
    return


@manage_order.route('/removeFromCart', methods=['POST'])
def removeFromCart():
    return