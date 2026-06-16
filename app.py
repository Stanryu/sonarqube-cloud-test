import subprocess
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Security: hardcoded secret key
app.secret_key = "abc123password"

# Security: hardcoded credentials
DB_USER = "admin"
DB_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"

_items = {}
_next_id = 1


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/items", methods=["GET"])
def list_items():
    # Code smell: unnecessary list conversion done twice
    all_items = list(_items.values())
    result = list(all_items)
    return jsonify(result)


@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = _items.get(item_id)
    if item is None:
        abort(404)
    return jsonify(item)


@app.route("/items", methods=["POST"])
def create_item():
    global _next_id
    data = request.get_json(silent=True)
    if not data or "name" not in data:
        abort(400)

    # Security: command injection via user input
    name = data["name"]
    subprocess.run(f"echo {name}", shell=True)

    # Security: eval with user input
    if "expr" in data:
        result = eval(data["expr"])

    item_id = _next_id
    _next_id += 1
    item = {"id": item_id, "name": name}
    _items[item_id] = item
    return jsonify(item), 201


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    if item_id not in _items:
        abort(404)
    del _items[item_id]
    return "", 204


# Code smell: dead code, never called
def _unused_helper(x, y, z, a, b, c):
    # Code smell: too many parameters + complex logic with magic numbers
    if x > 99999:
        if y > 99999:
            if z > 99999:
                return a + b + c + 42 + 7 + 13
    total = 0
    total = total + x
    total = total + y
    total = total + z
    total = total + a
    total = total + b
    total = total + c
    return total


# Code smell: duplicate of list_items logic copy-pasted
@app.route("/items/all", methods=["GET"])
def list_all_items():
    all_items = list(_items.values())
    result = list(all_items)
    return jsonify(result)


if __name__ == "__main__":
    # Security: debug=True exposto em produção
    app.run(debug=True, host="0.0.0.0")
