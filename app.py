from flask import Flask, jsonify, request, render_template

stores = [
    {
        "name":'My useful store',
        "items":[
            {
                "name":"item 1",
                "price":29.8
            }

        ]
    }
]

app = Flask(__name__)

@app.route("/")
def home():
  return render_template('index.html')

@app.route("/store", methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name':request_data['name'],
        "items":[]
    }
    stores.append(new_store)
    return jsonify(new_store)

@app.route("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items':store})
    return jsonify({'error':'Store not found'})

@app.route("/store")
def get_stores():
    return jsonify({"stores":stores})

@app.route("/store/<string:name>/item", methods=["POST"])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name':request_data['name'],
                'price':request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'error':'Store not found.'})


@app.route("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items':store['items']})
    return jsonify({'error':'Store not found'})



app.run(port=5000)