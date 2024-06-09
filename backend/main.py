
from flask import request, jsonify, send_from_directory
from config import app, db
from models import Contact


# Route main page
@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')


# Route to serve other static files in the frontend directory.
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory('../frontend', path)


# Route handle GET requests
@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()                           
    json_contacts = [contact.to_json() for contact in contacts]   
    return jsonify({"contacts": json_contacts})               



# Route handle POST requests. Create a new contact.
@app.route("/create_contact", methods=["POST"])
def create_contact():

    data = request.json                
    
    first_name = data.get("firstName")  
    last_name = data.get("lastName")
    email = data.get("email")
    number = data.get("number")

    # Validation.
    if not first_name or not last_name or not email or not number:                     
        return jsonify({"message": "Please include everything."}), 400
    
    # Validation.
    existing_contact = Contact.query.filter_by(first_name=first_name, last_name=last_name, email=email, number=number).first()
    if existing_contact:
        return jsonify({"message": "Contact already exists."}), 400

    # Create new Contact instance
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email, number=number)   

    try:
        # save to database
        db.session.add(new_contact)                  
        db.session.commit()                           

    except Exception as e:
        return jsonify({"message": str(e)}), 400     

    
    return jsonify({"message": "User created"}), 201   
  



# Route to handle PATCH requests.
@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    
    # get user id
    contact = Contact.query.get(user_id)                        
    # check if id exist
    if not contact:                                               
        return jsonify({"message": "User not found"}), 404
    
    # update user requested data.
    data = request.json                                          
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)
    contact.number = data.get("number", contact.number)
    
    # save to database
    db.session.commit()                                            
    
    return jsonify({"message": "User updated"}), 200              




# Route to handle DELETE requests.
@app.route("/update_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    # get delete user id
    contact = Contact.query.get(user_id)               
    # check of id exist
    if not contact:                                       
        return jsonify({"message": "User not found"}), 404
    
    # delete id
    db.session.delete(contact)                             
    #save at database
    db.session.commit()                                

    # Return a success message.
    return jsonify({"message": "User deleted"}), 200



# Run Flask Application
if __name__ == "__main__":
    with app.app_context():     
        db.create_all()   
    app.run(debug=True)
