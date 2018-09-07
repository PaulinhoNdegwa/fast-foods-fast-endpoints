from uuid import uuid4

# Create an empty list USERS that will store all user objects
USERS = []

# Create a class User that will define user objects
class User(object):
    
    def __init__(self, email, password):
        """Initialiazing the User"""
        self.user_id = str(uuid4())
        self.email = email
        self.password = password
    
    def __repr__(self):
        return ("User: {}".format(self.email))