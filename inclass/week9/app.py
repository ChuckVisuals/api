from flask import Flask, jsonify, request

app = Flask(__name__)

# MockData
mock = [
   {"game": "val",
    "description": "description",
    "hours": 300},
   {"game": "minecraft",
    "description": "description",
    "hours": 50},
   {"game": "FMV",
    "description": "description",
    "hours": 1000}
]

# Helper
def find(corn_id):
    pass

# GET /items - Read all corn
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(mock), 200

# POST /items return based on hours
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    
    print(data)
    
    hours = data['hours']

    for m in mock:
        print(m)
        if m['hours'] >= int(hours):
            return jsonify(m), 202
    return jsonify(), 404

# PUT /items/<id> - Update info
@app.route('/add_items', methods=['PUT'])
def update_item():
    
    data = request.get_json()
    
    print(data.keys())
    
    if data.keys() == {'game', 'description', 'hours'}:
        mock.append(data)
        return jsonify(mock), 200
    else:
        return jsonify(), 400

    data = request.json
    #update info
    pass

# DELETE
# @app.route('/delete_item', methods=['DELETE'])
# def delete_item():
    
#     data = request.get_json()
#     for m in mock:
#         if m['game'] is data['game']:
#             mock.remove(m)
#             return jsonify(mock), 200
#     return jsonify(), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
