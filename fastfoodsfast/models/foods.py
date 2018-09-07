from uuid import uuid4

# create an empty list of fooditems
# each fooditem will be contained in a dict
FOODITEMS = []

# create a class Fooditem to define fooditem
class Fooditem(object):

    def __init__(self, name, price, imagesrc):
        self.fooditem_id = str(uuid4())
        self.name = name
        self.price = price
        self.imagesrc = imagesrc

    def __repr__(self):
        return "Food added: {} - {}".format(self.name, self.price)

# create an empty list to hold orders
# each order will be held in a dictbin the list

ORDERS = []

class Order(object):
    
    def __init__(self, customer, fooditem, price, status="Pending"):
        self.order_id = str(uuid4())
        self.customer = customer
        self.fooditem = fooditem
        self.price = price
        self.status = status

    def __repr__(self):
        return "Order {} by {}".format(self.fooditem, self.customer)
        