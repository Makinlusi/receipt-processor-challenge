#stater for the webservice
from flask import Flask, request, jsonify
import uuid
import math

app = Flask(__name__)
receipt_data = {}
receipts = {}  # In-memory dictionary to store receipts


@app.route('/receipts/process', methods=['POST'])
def process_receipts():
    receipt = request.get_json()
    # process the receipt and calculate the points
    points = calculate_points(receipt)
    # generate a unique ID for the receipt
    receipt_id = str(uuid.uuid4())
    # store the receipt ID and points in memory (e.g., a dictionary)
    store_receipt(receipt_id, points)
    # return the response as JSON
    response = {'id': receipt_id}
    return jsonify(response), 200


@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    # Retrieve the points for the specified receipt ID from memory
    points = retrieve_points(receipt_id)

    if points is None:
        return jsonify({'error': 'Receipt not found'}), 404

    # Return the response as JSON
    response = {'points': points}
    return jsonify(response), 200


def retrieve_points(receipt_id):
    
    receipt_points = receipt_data.get(receipt_id)  # Assuming receipt_data is a dictionary storing receipt points

    return receipt_points




def calculate_points(receipt):
    points = 0

    # Rule 1: One point for every alphanumeric character in the retailer name
    retailer_name = receipt.get('retailer', '')
    alphanumeric_count = sum(char.isalnum() for char in retailer_name)
    points += alphanumeric_count

    # Rule 2: 50 points if the total is a round dollar amount with no cents
    total = float(receipt.get('total', 0))
    if total == round(total):
        points += 50

    # Rule 3: 25 points if the total is a multiple of 0.25
    if total % 0.25 == 0:
        points += 25

    # Rule 4: 5 points for every two items on the receipt
    item_count = len(receipt.get('items', []))
    points += (item_count // 2) * 5

    # Rule 5: Multiply the price by 0.2 and round up if item description length is a multiple of 3
    items = receipt.get('items', [])
    for item in items:
        description_length = len(item.get('shortDescription', '').strip())
        if description_length % 3 == 0:
            price = float(item.get('price', 0))
            points += math.ceil(price * 0.2)  # Fix: Round up using math.ceil

    # Rule 6: 6 points if the day in the purchase date is odd
    purchase_date = receipt.get('purchaseDate', '')
    day = int(purchase_date.split('-')[-1])
    if day % 2 != 0:
        points += 6

    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = receipt.get('purchaseTime', '')
    hour = int(purchase_time.split(':')[0])
    if 14 < hour < 16:
        points += 10

    # Rule 8: Additional 10 points for having 4 items on the receipt
    if item_count % 4 == 0:
        points += 10

    return points



def store_receipt(receipt_id, points):
    receipt_data[receipt_id] = points


if __name__ == '__main__':
    app.run(debug=True)
