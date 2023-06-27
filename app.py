from flask import Flask, request, jsonify
import uuid
import math

app = Flask(__name__)
receipt_data = {}


@app.route('/receipts/process', methods=['POST'])
def process_receipts():
    receipt = request.get_json()
    points = calculate_points(receipt)
    receipt_id = str(uuid.uuid4())
    store_receipt(receipt_id, points)
    response = {'id': receipt_id}
    return jsonify(response), 200


@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    points = retrieve_points(receipt_id)

    if points is None:
        return jsonify({'error': 'Receipt not found'}), 404

    response = {'points': points}
    return jsonify(response), 200


def retrieve_points(receipt_id):
    receipt_points = receipt_data.get(receipt_id)
    return receipt_points


def calculate_points(receipt):
    points = 0
    retailer_name = receipt.get('retailer', '')
    alphanumeric_count = sum(char.isalnum() for char in retailer_name)
    points += alphanumeric_count

    total = float(receipt.get('total', 0))
    if total == round(total):
        points += 50

    if total % 0.25 == 0:
        points += 25

    item_count = len(receipt.get('items', []))
    points += (item_count // 2) * 5

    items = receipt.get('items', [])
    for item in items:
        description_length = len(item.get('shortDescription', '').strip())
        if description_length % 3 == 0:
            price = float(item.get('price', 0))
            points += math.ceil(price * 0.2)

    purchase_date = receipt.get('purchaseDate', '')
    day = int(purchase_date.split('-')[-1])
    if day % 2 != 0:
        points += 6

    purchase_time = receipt.get('purchaseTime', '')
    hour = int(purchase_time.split(':')[0])
    if 14 < hour < 16:
        points += 10

    if item_count % 4 == 0:
        points += 10

    return points


def store_receipt(receipt_id, points):
    receipt_data[receipt_id] = points


if __name__ == '__main__':
    app.run(debug=True)
