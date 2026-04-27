from flask import Flask, render_template, request, jsonify, session
import requests

TELEGRAM_TOKEN = "8708650898:AAFUKwQRo04xeKUptXQf-mEm_W2LmSkAVbU"
TELEGRAM_CHAT_ID = "5274379305"


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})


app = Flask(__name__)
app.secret_key = "fastfood_secret_2026"

MENU = [
    {
        "id": 1,
        "name": "Burger Classic",
        "price": 850,
        "category": "Burgers",
        "emoji": "🍔",
        "desc": "Bœuf haché, cheddar, salade, tomate",
    },
    {
        "id": 2,
        "name": "Double Smash",
        "price": 1200,
        "category": "Burgers",
        "emoji": "🍔",
        "desc": "Double steak, sauce spéciale maison",
    },
    {
        "id": 3,
        "name": "Crispy Chicken",
        "price": 950,
        "category": "Chicken",
        "emoji": "🍗",
        "desc": "Poulet croustillant, mayo épicée",
    },
    {
        "id": 4,
        "name": "Wrap Chicken",
        "price": 800,
        "category": "Chicken",
        "emoji": "🌯",
        "desc": "Poulet grillé, légumes, sauce yaourt",
    },
    {
        "id": 5,
        "name": "Frites Maison",
        "price": 300,
        "category": "Sides",
        "emoji": "🍟",
        "desc": "Frites fraîches, sel & épices",
    },
    {
        "id": 6,
        "name": "Onion Rings",
        "price": 350,
        "category": "Sides",
        "emoji": "🧅",
        "desc": "Rondelles oignons panées croustillantes",
    },
    {
        "id": 7,
        "name": "Coca-Cola",
        "price": 200,
        "category": "Drinks",
        "emoji": "🥤",
        "desc": "33cl bien frais",
    },
    {
        "id": 8,
        "name": "Milkshake Vanille",
        "price": 450,
        "category": "Drinks",
        "emoji": "🥛",
        "desc": "Milkshake crémeux fait maison",
    },
    {
        "id": 9,
        "name": "Sundae Chocolat",
        "price": 400,
        "category": "Desserts",
        "emoji": "🍨",
        "desc": "Glace vanille, sauce chocolat",
    },
    {
        "id": 10,
        "name": "Brownie",
        "price": 350,
        "category": "Desserts",
        "emoji": "🍫",
        "desc": "Brownie chaud, cœur fondant",
    },
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/menu")
def menu():
    categories = list(dict.fromkeys(item["category"] for item in MENU))
    return render_template("menu.html", menu=MENU, categories=categories)


@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    total = sum(item["price"] * item["qty"] for item in cart_items)
    return render_template("cart.html", cart=cart_items, total=total)


@app.route("/api/cart/add", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    cart = session.get("cart", [])
    item_id = data.get("id")
    product = next((p for p in MENU if p["id"] == item_id), None)
    if not product:
        return jsonify({"error": "Produit introuvable"}), 404
    existing = next((i for i in cart if i["id"] == item_id), None)
    if existing:
        existing["qty"] += 1
    else:
        cart.append({**product, "qty": 1})
    session["cart"] = cart
    session.modified = True
    total_items = sum(i["qty"] for i in cart)
    return jsonify({"success": True, "cart_count": total_items})


@app.route("/api/cart/remove", methods=["POST"])
def remove_from_cart():
    data = request.get_json()
    cart = session.get("cart", [])
    cart = [i for i in cart if i["id"] != data.get("id")]
    session["cart"] = cart
    session.modified = True
    total = sum(i["price"] * i["qty"] for i in cart)
    return jsonify(
        {"success": True, "total": total, "cart_count": sum(i["qty"] for i in cart)}
    )


@app.route("/api/cart/clear", methods=["POST"])
def clear_cart():
    session["cart"] = []
    session.modified = True
    return jsonify({"success": True})


@app.route("/checkout", methods=["POST"])
def checkout():
    cart = session.get("cart", [])
    if not cart:
        return jsonify({"success": False})
    total = sum(item["price"] * item["qty"] for item in cart)
    message = "🔔 طلب جديد!\n\n"
    for item in cart:
        message += f"{item['emoji']} {item['name']} x{item['qty']} = {item['price'] * item['qty']} DA\n"
    message += f"\n💰 Total: {total} DA"
    send_telegram(message)
    session.pop("cart", None)
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
