# Importing Flask Module/lib
from flask import Flask
from flask_pymongo import PyMongo

# Import BSON (to convert BSON to JSON)
from bson.json_util import dumps
from flask import jsonify, request

# To generate random string
from bson.objectid import ObjectId

# Importing Hashing lib
from werkzeug.security import generate_password_hash, check_password_hash

# Initializing Flask application
app = Flask(__name__)

# Set secret key
app.secret_key = "secretkey"

# Configuring URL for DB
app.config['MONGO_URI'] = "mongodb://localhost:27017/Users"

# Passing app variable
mongo = PyMongo(app)

# To add new user to DB
@app.route('/add', methods = ['POST'])
def add_user():
	_json = request.json
	_name = _json['name']
	_email = _json['email']
	_password = _json['pwd']

	# Validating values
	if _name and _email and _password and request.method == 'POST':

		_hashed_password = generate_password_hash(_password)

		# Generating Unique id randomly
		id = mongo.db.user.insert({'name': _name, 'email': _email, 'pwd': _hashed_password})

		# Passing message
		resp = jsonify("User added successfully")
		resp.status_code = 200
		return resp

	else:

		# Error Message by calling Function
		return not_found()

# To show all users in the DB
@app.route('/users')
def users():
	users = mongo.db.user.find()
	resp = dumps(users)
	return resp

# To display information about specific User
@app.route('/user/<id>')
def user(id):
	user = mongo.db.user.find_one({'_id' : ObjectId(id)})
	resp = dumps(user)
	return resp

# To Update user details
@app.route('/update/<id>', methods = ['PUT'])
def update_user(id):
	_id = id
	_json = request.json
	_name = _json['name']
	_email = _json['email']
	_password = _json['pwd']

	if _name and _email and _password and _id and request.method == "PUT":
		_hashed_password = generate_password_hash(_password)
		mongo.db.user.update_one({'_id' : ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
								 {'$set' : {'name' : _name, 'email' : _email, 'pwd' : _hashed_password}})
		resp = jsonify("User Updated Successfully")
		resp.status_code = 200
		return resp

	else:
		return not_found()

# To Delete User
@app.route('/delete/<id>', methods = ['DELETE'])
def delete_user(id):
	mongo.db.user.delete_one({'_id' : ObjectId(id)})
	resp = jsonify("User Deleted Successfully")
	resp.status_code = 200
	return resp

# Display Errors
@app.errorhandler(404)
def not_found(error = None):
	message = {
		'status' : 404,
		'message' : 'Not Found' + request.url
	}
	resp = jsonify(message)
	resp.status_code = 404
	return resp

# To run application
if __name__ == "__main__":

	# To restart app automatically
	app.run(debug = True)