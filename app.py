from flask import Flask, render_template, request, jsonify, session
import requests as req
from config import *

app = Flask(__name__)
app.secret_key = "secret_2026"


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        req.post(
            url,
            data={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"},
            timeout=5,
        )
    except:
        pass


def get_config():
    return {
        "name": RESTAURANT_NAME,
        "slogan": RESTAURANT_SLOGAN,
        "hero": RESTAURANT_HERO,
        "desc": RESTAURANT_DESC,
        "primary": PRIMARY_COLOR,
        "secondary": SECONDARY_COLOR,
        "dev": DEVELOPER_NAME,
    }


@app.route("/")
def index():
    table = request.args.get("table")
    if table:
        session["table"] = table
    cart = session.get("cart", [])
    return render_template("index.html", cart=cart, cfg=get_config())


@app.route("/menu")
def menu():
    table = request.args.get("table")
    if table:
        session["table"] = table
    cart = session.get("cart", [])
    categories = list(dict.fromkeys(item["category"] for item in MENU))
    return render_template(
        "menu.html", menu=MENU, categories=categories, cart=cart, cfg=get_config()
    )


@app.route("/cart")
def cart_page():
    cart = session.get("cart", [])
    total = sum(i["price"] * i["qty"] for i in cart)
    table = session.get("table", None)
    return render_template(
        "cart.html", cart=cart, total=total, table=table, cfg=get_config()
    )


@app.route("/api/cart/add", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    item_id = data.get("id")
    item = next((i for i in MENU if i["id"] == item_id), None)
    if not item:
        return jsonify({"success": False})
    cart = session.get("cart", [])
    existing = next((i for i in cart if i["id"] == item_id), None)
    if existing:
        existing["qty"] += 1
    else:
        cart.append(
            {
                "id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "emoji": item["emoji"],
                "qty": 1,
            }
        )
    session["cart"] = cart
    session.modified = True
    return jsonify({"success": True, "cart_count": sum(i["qty"] for i in cart)})


@app.route("/api/cart/remove", methods=["POST"])
def remove_from_cart():
    data = request.get_json()
    cart = session.get("cart", [])
    cart = [i for i in cart if i["id"] != data.get("id")]
    session["cart"] = cart
    session.modified = True
    return jsonify({"success": True, "cart_count": sum(i["qty"] for i in cart)})


@app.route("/checkout", methods=["POST"])
def checkout():
    cart = session.get("cart", [])
    if not cart:
        return jsonify({"success": False})
    data = request.get_json()
    name = data.get("name", "?")
    table = data.get("table", "?")
    total = sum(item["price"] * item["qty"] for item in cart)
    msg = f"🔔 <b>Nouvelle commande — {RESTAURANT_NAME}</b>\n\n"
    msg += f"🪑 <b>Table N°{table}</b>\n"
    msg += f"👤 <b>Nom:</b> {name}\n\n🛒 <b>Commande:</b>\n"
    for item in cart:
        msg += f"{item['emoji']} {item['name']} x{item['qty']} = {item['price'] * item['qty']} DA\n"
    msg += f"\n💰 <b>Total: {total} DA</b>"
    send_telegram(msg)
    session.pop("cart", None)
    return jsonify({"success": True})


@app.route("/ping")
def ping():
    return "pong", 200


if __name__ == "__main__":
    app.run(debug=True)
