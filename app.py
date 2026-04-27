from flask import Flask, render_template, request, jsonify, session
import requests as req

app = Flask(__name__)
app.secret_key = "fastfood_secret_2026"

TELEGRAM_TOKEN = "8708650898:AAFUKwQRo04xeKUptXQf-mEm_W2LmSkAVbU"
TELEGRAM_CHAT_ID = "5274379305"


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    req.post(
        url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    )


MENU = [
    # Tacos
    {
        "id": 1,
        "name": "Tacos Poulet",
        "price": 400,
        "category": "Tacos",
        "emoji": "🌮",
        "desc": "Tacos au poulet grillé",
    },
    {
        "id": 2,
        "name": "Tacos Mexicain",
        "price": 400,
        "category": "Tacos",
        "emoji": "🌮",
        "desc": "Tacos mexicain épicé",
    },
    {
        "id": 3,
        "name": "Tacos Kabda",
        "price": 450,
        "category": "Tacos",
        "emoji": "🌮",
        "desc": "Tacos au foie",
    },
    {
        "id": 4,
        "name": "Tacos Chawarma",
        "price": 400,
        "category": "Tacos",
        "emoji": "🌮",
        "desc": "Tacos chawarma",
    },
    {
        "id": 5,
        "name": "Tacos Viande",
        "price": 450,
        "category": "Tacos",
        "emoji": "🌮",
        "desc": "Tacos à la viande",
    },
    {
        "id": 6,
        "name": "Tacos Mixte",
        "price": 500,
        "category": "Tacos",
        "emoji": "🌮",
        "desc": "Tacos mixte",
    },
    {
        "id": 7,
        "name": "Tacos Crispy",
        "price": 600,
        "category": "Tacos",
        "emoji": "🌮",
        "desc": "Tacos crispy",
    },
    {
        "id": 8,
        "name": "Tacos Poulet + Assiette 3 Fromages",
        "price": 600,
        "category": "Tacos",
        "emoji": "🌮",
        "desc": "Poulet avec assiette 3 fromages",
    },
    {
        "id": 9,
        "name": "Tacos Viande + Assiette 3 Fromages",
        "price": 650,
        "category": "Tacos",
        "emoji": "🌮",
        "desc": "Viande avec assiette 3 fromages",
    },
    # Calzoni
    {
        "id": 10,
        "name": "Calzoni Poulet",
        "price": 450,
        "category": "Calzoni",
        "emoji": "🫓",
        "desc": "Calzoni au poulet",
    },
    {
        "id": 11,
        "name": "Calzoni Viande",
        "price": 550,
        "category": "Calzoni",
        "emoji": "🫓",
        "desc": "Calzoni à la viande",
    },
    {
        "id": 12,
        "name": "Calzoni Kbda",
        "price": 500,
        "category": "Calzoni",
        "emoji": "🫓",
        "desc": "Calzoni au foie",
    },
    # Makloub
    {
        "id": 13,
        "name": "Makloub Poulet",
        "price": 350,
        "category": "Makloub",
        "emoji": "🥙",
        "desc": "Makloub au poulet",
    },
    {
        "id": 14,
        "name": "Makloub Mexicain",
        "price": 350,
        "category": "Makloub",
        "emoji": "🥙",
        "desc": "Makloub mexicain",
    },
    {
        "id": 15,
        "name": "Makloub Kabda",
        "price": 400,
        "category": "Makloub",
        "emoji": "🥙",
        "desc": "Makloub au foie",
    },
    {
        "id": 16,
        "name": "Makloub Viande",
        "price": 400,
        "category": "Makloub",
        "emoji": "🥙",
        "desc": "Makloub à la viande",
    },
    # Grec
    {
        "id": 17,
        "name": "Grec Poulet",
        "price": 400,
        "category": "Grec",
        "emoji": "🥗",
        "desc": "Grec au poulet",
    },
    {
        "id": 18,
        "name": "Grec Mexicain",
        "price": 400,
        "category": "Grec",
        "emoji": "🥗",
        "desc": "Grec mexicain",
    },
    {
        "id": 19,
        "name": "Grec Chawarma",
        "price": 400,
        "category": "Grec",
        "emoji": "🥗",
        "desc": "Grec chawarma",
    },
    {
        "id": 20,
        "name": "Grec Viande",
        "price": 450,
        "category": "Grec",
        "emoji": "🥗",
        "desc": "Grec à la viande",
    },
    # Malfouf
    {
        "id": 21,
        "name": "Malfouf Poulet",
        "price": 400,
        "category": "Malfouf",
        "emoji": "🌯",
        "desc": "Malfouf au poulet",
    },
    {
        "id": 22,
        "name": "Malfouf Chawarma",
        "price": 400,
        "category": "Malfouf",
        "emoji": "🌯",
        "desc": "Malfouf chawarma",
    },
    {
        "id": 23,
        "name": "Malfouf Mexicain",
        "price": 400,
        "category": "Malfouf",
        "emoji": "🌯",
        "desc": "Malfouf mexicain",
    },
    {
        "id": 24,
        "name": "Malfouf Kabda",
        "price": 450,
        "category": "Malfouf",
        "emoji": "🌯",
        "desc": "Malfouf au foie",
    },
    {
        "id": 25,
        "name": "Malfouf Viande",
        "price": 450,
        "category": "Malfouf",
        "emoji": "🌯",
        "desc": "Malfouf à la viande",
    },
    # Pizza
    {
        "id": 26,
        "name": "Pizza Poulet",
        "price": 400,
        "category": "Pizza",
        "emoji": "🍕",
        "desc": "Pizza au poulet",
    },
    {
        "id": 27,
        "name": "Pizza Marguerite",
        "price": 250,
        "category": "Pizza",
        "emoji": "🍕",
        "desc": "Pizza marguerite classique",
    },
    {
        "id": 28,
        "name": "Pizza Poulet Fumée",
        "price": 450,
        "category": "Pizza",
        "emoji": "🍕",
        "desc": "Pizza poulet fumé",
    },
    {
        "id": 29,
        "name": "Pizza Végétarien",
        "price": 450,
        "category": "Pizza",
        "emoji": "🍕",
        "desc": "Pizza végétarienne",
    },
    {
        "id": 30,
        "name": "Pizza Viande",
        "price": 500,
        "category": "Pizza",
        "emoji": "🍕",
        "desc": "Pizza à la viande",
    },
    {
        "id": 31,
        "name": "Pizza 2 Saisons",
        "price": 500,
        "category": "Pizza",
        "emoji": "🍕",
        "desc": "Pizza 2 saisons",
    },
    {
        "id": 32,
        "name": "Pizza 4 Saisons",
        "price": 600,
        "category": "Pizza",
        "emoji": "🍕",
        "desc": "Pizza 4 saisons",
    },
    {
        "id": 33,
        "name": "Pizza Thon",
        "price": 450,
        "category": "Pizza",
        "emoji": "🍕",
        "desc": "Pizza au thon",
    },
    {
        "id": 34,
        "name": "Pizza 3 Fromages",
        "price": 500,
        "category": "Pizza",
        "emoji": "🍕",
        "desc": "Pizza 3 fromages",
    },
    {
        "id": 35,
        "name": "Pizza 4 Fromages",
        "price": 600,
        "category": "Pizza",
        "emoji": "🍕",
        "desc": "Pizza 4 fromages",
    },
    {
        "id": 36,
        "name": "Pizza Champignon",
        "price": 500,
        "category": "Pizza",
        "emoji": "🍕",
        "desc": "Pizza aux champignons",
    },
    {
        "id": 37,
        "name": "Pizza Chef",
        "price": 650,
        "category": "Pizza",
        "emoji": "🍕",
        "desc": "Pizza spéciale chef",
    },
    {
        "id": 38,
        "name": "Pizza Mixte",
        "price": 600,
        "category": "Pizza",
        "emoji": "🍕",
        "desc": "Pizza mixte",
    },
    # Burger
    {
        "id": 39,
        "name": "Cheese Burger",
        "price": 450,
        "category": "Burger",
        "emoji": "🍔",
        "desc": "Cheese burger classique",
    },
    {
        "id": 40,
        "name": "Double Cheese Burger",
        "price": 550,
        "category": "Burger",
        "emoji": "🍔",
        "desc": "Double cheese burger",
    },
    {
        "id": 41,
        "name": "Chicken Burger",
        "price": 450,
        "category": "Burger",
        "emoji": "🍔",
        "desc": "Burger au poulet croustillant",
    },
    # Plats
    {
        "id": 42,
        "name": "Plat Chawarma",
        "price": 600,
        "category": "Plats",
        "emoji": "🍽️",
        "desc": "Plat chawarma complet",
    },
    {
        "id": 43,
        "name": "Plat Mexicain",
        "price": 600,
        "category": "Plats",
        "emoji": "🍽️",
        "desc": "Plat mexicain complet",
    },
    {
        "id": 44,
        "name": "Plat Escalope Grillé",
        "price": 700,
        "category": "Plats",
        "emoji": "🍽️",
        "desc": "Escalope grillée",
    },
    {
        "id": 45,
        "name": "Plat de Chef 1 Personne",
        "price": 1200,
        "category": "Plats",
        "emoji": "🍽️",
        "desc": "Plat de chef pour 1 personne",
    },
    {
        "id": 46,
        "name": "Plat 1 Personne",
        "price": 1200,
        "category": "Plats",
        "emoji": "🍽️",
        "desc": "Plat complet pour 1 personne",
    },
    {
        "id": 47,
        "name": "Plat Escalope à la Crème",
        "price": 900,
        "category": "Plats",
        "emoji": "🍽️",
        "desc": "Escalope à la crème",
    },
    {
        "id": 48,
        "name": "Plat Kintaki",
        "price": 850,
        "category": "Plats",
        "emoji": "🍽️",
        "desc": "Plat kintaki",
    },
    {
        "id": 49,
        "name": "Plat Kabda",
        "price": 850,
        "category": "Plats",
        "emoji": "🍽️",
        "desc": "Plat kabda",
    },
    {
        "id": 50,
        "name": "Plat de Chef 2 Personnes",
        "price": 1900,
        "category": "Plats",
        "emoji": "🍽️",
        "desc": "Plat de chef pour 2 personnes",
    },
    # Gratin
    {
        "id": 51,
        "name": "Gratin Poulet",
        "price": 400,
        "category": "Gratin",
        "emoji": "🥘",
        "desc": "Gratin au poulet",
    },
    {
        "id": 52,
        "name": "Gratin Viande",
        "price": 500,
        "category": "Gratin",
        "emoji": "🥘",
        "desc": "Gratin à la viande",
    },
    # Brochettes
    {
        "id": 53,
        "name": "Brochette Poulet",
        "price": 300,
        "category": "Brochettes",
        "emoji": "🍢",
        "desc": "Brochette de poulet",
    },
    {
        "id": 54,
        "name": "Brochette Mexicain",
        "price": 300,
        "category": "Brochettes",
        "emoji": "🍢",
        "desc": "Brochette mexicaine",
    },
    {
        "id": 55,
        "name": "اللحم",
        "price": 50,
        "category": "Brochettes",
        "emoji": "🍢",
        "desc": "Brochette de viande",
    },
    {
        "id": 56,
        "name": "سكالوب",
        "price": 30,
        "category": "Brochettes",
        "emoji": "🍢",
        "desc": "Escalope",
    },
    {
        "id": 57,
        "name": "مرقاز",
        "price": 50,
        "category": "Brochettes",
        "emoji": "🍢",
        "desc": "Merguez",
    },
    # Desserts
    {
        "id": 58,
        "name": "Tiramisu",
        "price": 450,
        "category": "Desserts",
        "emoji": "🍰",
        "desc": "Tiramisu maison",
    },
    {
        "id": 59,
        "name": "Mousse au Chocolat",
        "price": 250,
        "category": "Desserts",
        "emoji": "🍫",
        "desc": "Mousse au chocolat",
    },
    {
        "id": 60,
        "name": "Crème Brûlée",
        "price": 300,
        "category": "Desserts",
        "emoji": "🍮",
        "desc": "Crème brûlée maison",
    },
    {
        "id": 61,
        "name": "Cheese Cake",
        "price": 400,
        "category": "Desserts",
        "emoji": "🍰",
        "desc": "Cheese cake",
    },
    {
        "id": 62,
        "name": "Galb Louz",
        "price": 40,
        "category": "Desserts",
        "emoji": "🍯",
        "desc": "Galb louz traditionnel",
    },
    {
        "id": 63,
        "name": "Galb Louz Chocolat",
        "price": 60,
        "category": "Desserts",
        "emoji": "🍫",
        "desc": "Galb louz au chocolat",
    },
]


@app.route("/")
def index():
    cart = session.get("cart", [])
    return render_template("index.html", cart=cart)


@app.route("/menu")
def menu():
    cart = session.get("cart", [])
    categories = list(dict.fromkeys(item["category"] for item in MENU))
    return render_template("menu.html", menu=MENU, categories=categories, cart=cart)


@app.route("/cart")
def cart():
    cart = session.get("cart", [])
    total = sum(i["price"] * i["qty"] for i in cart)
    return render_template("cart.html", cart=cart, total=total)


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
    total = sum(i["price"] * i["qty"] for i in cart)
    return jsonify(
        {"success": True, "total": total, "cart_count": sum(i["qty"] for i in cart)}
    )


@app.route("/api/cart/remove", methods=["POST"])
def remove_from_cart():
    data = request.get_json()
    item_id = data.get("id")
    cart = session.get("cart", [])
    cart = [i for i in cart if i["id"] != item_id]
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
    data = request.get_json()
    name = data.get("name", "غير محدد")
    phone = data.get("phone", "غير محدد")
    total = sum(item["price"] * item["qty"] for item in cart)
    message = f"🔔 <b>طلب جديد!</b>\n\n👤 <b>الاسم:</b> {name}\n📞 <b>الهاتف:</b> {phone}\n\n🛒 <b>الطلب:</b>\n"
    for item in cart:
        message += f"{item['emoji']} {item['name']} x{item['qty']} = {item['price'] * item['qty']} DA\n"
    message += f"\n💰 <b>Total: {total} DA</b>"
    send_telegram(message)
    session.pop("cart", None)
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
