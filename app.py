from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os

app = Flask(__name__, template_folder='templates')
CORS(app)

DATA_FILE = 'backend/developers.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/developers', methods=['GET'])
def get_developers():
    return jsonify(load_data())

@app.route('/api/developers', methods=['POST'])
def add_developer():
    dev = request.json
    data = load_data()
    dev['id'] = len(data) + 1
    data.append(dev)
    save_data(data)
    return jsonify({'message': 'Developer added'}), 201

@app.route('/api/developers/<int:dev_id>', methods=['PUT'])
def update_developer(dev_id):
    update = request.json
    data = load_data()
    for dev in data:
        if dev['id'] == dev_id:
            dev.update(update)
            save_data(data)
            return jsonify({'message': 'Developer updated'})
    return jsonify({'message': 'Developer not found'}), 404

@app.route('/api/developers/<int:dev_id>', methods=['DELETE'])
def delete_developer(dev_id):
    data = load_data()
    data = [dev for dev in data if dev['id'] != dev_id]
    save_data(data)
    return jsonify({'message': 'Developer deleted'})

if __name__ == '__main__':
    app.run(debug=True)