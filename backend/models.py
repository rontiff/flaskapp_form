from config import db

# Define the table model ,  inherit from db.Model
class Contact(db.Model):   
                   
    id = db.Column(db.Integer, primary_key=True)                         
    first_name = db.Column(db.String(80), unique=False, nullable=False) 
    last_name = db.Column(db.String(80), unique=False, nullable=False)  
    email = db.Column(db.String(120), unique=False, nullable=False)    
    number = db.Column(db.String(20), unique=False, nullable=False)    

    
    # __repr__ method. define a string representation for an instance of a class.
    def __repr__(self):
        return f"Contact(firstName = {self.first_name}, lastName = {self.last_name}, email = {self.email}), numer = {self.number}"
    
    # Method to convert python object to JSON format.
    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "number": self.number,
        }

