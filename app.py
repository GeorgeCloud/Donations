from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs
import os
app = Flask(__name__)

uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor')
client = MongoClient(uri)
db = client.get_default_database()

charities = db.charities
donations = db.donations
fs = gridfs.GridFS(db)

def create_charity(charity_name, description):
    charities.insert_one({
        'name': charity_name,
        'description': description,
        'created_on': 'datetime',
    })

def create_donation_document(request_form):
    donation = {
        'amount': request_form['amount'],
        'message': request_form['message'],
        'user_id': 0,                               # default user
        'charity_id': request_form['charity_id'],
    }
    return donation

@app.route('/', methods=['GET'])
def charity_index():
    sorting_method = 'x' or request.form['sorting_method']
    all_charities = charities.find({})

    return render_template('index_charities.html', charities=all_charities)

@app.route('/charity/new', methods=['GET'])
def new_charity():
    return render_template('new_charity.html')

@app.route('/charity/<charity_id>', methods=['GET'])
def show_charity(charity_id):
    current_charity = charities.find_one({'_id': ObjectId(charity_id)})
    charity_donations = donations.find({'charity_id': charity_id})

    return render_template('show_charity.html', charity=current_charity, donations=charity_donations)

@app.route('/donation/create', methods=['POST'])
def create_donation():
    new_donation = create_donation_document(request.form)

    donations.insert_one(new_donation)

    return redirect(url_for('show_charity', charity_id=request.form['charity_id']))


if __name__ == "__main__":
    app.run(debug=True)
