from math import nan
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pandas as pd
import requests

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook_receiver():
    # Parse the data from the file to a JSON to request
    file = request.files['file']
    bodies = parse_dataframe(file)
    # Keep the Identifier handy for the output request
    identifier = request.form['id']
    if len(bodies) > 1:
        for body in bodies:
            x = post_items(body, identifier) 
            continue
    else:
        x = post_items(bodies, identifier)       
        return jsonify({"status": 200}), 200
    return jsonify({"message": "webhook received succesfully"}), 200

cardKingdom = ['CK', "CardKingdom", "CARDKINGDOM"]
mintCard = ['MINT', 'MINTCARD']
api = "http://backend:8080/api/v1/order"


def post_items(body, identifier):
    endpoint = api + "/" + identifier + "/items"
    x = requests.post(endpoint, json=body)
    if x.status_code == 200:
        return x
    else:
        raise Exception()

def parse_dataframe(file):
    dfs = pd.read_excel(file, sheet_name=None)
    bodies = []
    for key in dfs.keys():
        container = []
        df = dfs[key]
        df.reset_index()
        
        for index, row in df.iterrows():
            new_item = {
                "retailer": key,
                "responsible": row["Quien pide"],
                "itemName" : row["Nombre de la carta"],
                "quantity": row["Cantidad"],
                "reportedPrice" :row["Precio"],
                "mainQuality": deal_with_qualities(row["Condición 1"]),
                "alternateQuality": deal_with_qualities(row["Condición 2"]),
                "source": row["Link Abugames"]
            }
            container.append(new_item)
        bodies.append(container)
    return bodies
    

near_mint = ["NM"]
excellent = ["EX","SP"]
very_good = ["VG"]
good = ["G"]

def deal_with_qualities(row):
    if row == '' or row == nan:
        return "EMPTY"
    elif row in near_mint:
        return "NEAR_MINT"
    elif row in excellent:
        return "EXCELLENT"
    elif row in very_good:
        return "GOOD"
    elif row in good:
        return "LIGTHLY_PLAYED"
    else:
        return "NEAR_MINT"
        

if __name__ == '__main__':
    app.run(debug=True)