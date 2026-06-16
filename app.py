from flask import Flask, jsonify, request, abort
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)

_items = {}
_next_id = 1


def _get_next_id():
    global _next_id
    item_id = _next_id
    _next_id += 1
    return item_id


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/items", methods=["GET"])
def list_items():
    return jsonify(list(_items.values()))


@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = _items.get(item_id)
    if item is None:
        abort(404)
    return jsonify(item)


@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json(silent=True)
    if not data or "name" not in data:
        abort(400)
    item_id = _get_next_id()
    item = {"id": item_id, "name": data["name"]}
    _items[item_id] = item
    return jsonify(item), 201


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    if item_id not in _items:
        abort(404)
    del _items[item_id]
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
