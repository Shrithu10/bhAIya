from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import requests
import base64
from PIL import Image
import io
import traceback
import firebase_admin
from firebase_admin import credentials, auth
import os
import uuid
import hashlib
import json
from datetime import datetime
import logging
from dotenv import load_dotenv
from io import BytesIO
import pycurl
from utils import (
    getcategoriesFromImage,
    getCategoriesFromText,
    getCategoriesFromQuery,
    getImage,
)
from similarity import find_top_k_similar,get_personal_recommendations
from comfyui_util import queue_prompt
from pymongo import MongoClient
from flask_cors import CORS

load_dotenv()


mongoDatabase = MongoClient(os.getenv("CONNECTION_STRING"))["bhAIya"]

# DATABASE_NAME="database"
# DATABASE_NAME="database_500"
# DATABASE_NAME="amazon_database"
DATABASE_NAME = "only_clothes"
# DATABASE_NAME = os.getenv("DATABASE_NAME")

# IMAGES_DATABASE= "imageDatabase"
# IMAGES_DATABASE= "imageDatabase_500"
# IMAGES_DATABASE = "amazon_images"
IMAGES_DATABASE = "only_clothes_images"
# IMAGES_DATABASE = os.getenv("IMAGES_DATABASE")


users_collection = mongoDatabase[os.getenv("USERS_COLLECTION")]


try:
    # database = mongoDatabase["database"].find({}, {"_id": 0})
    # database = mongoDatabase["database_500"].find({}, {"_id": 0})
    database = mongoDatabase[DATABASE_NAME].find({}, {"_id": 0})
    database = list(database)
    print("Data loaded")
except Exception as e:
    print("Error loading main database")
try:
    # imgDatabase = mongoDatabase["imageDatabase"].find({}, {"_id": 0})
    # imgDatabase = mongoDatabase["imageDatabase_500"].find({}, {"_id": 0})
    imgDatabase = mongoDatabase[IMAGES_DATABASE].find({}, {"_id": 0})
    imgDatabase = list(imgDatabase)
    print("Image database loaded")
except Exception as e:
    print("Error loading image database")

# load_dotenv()

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set a secret key for session management
CORS(app, resources={r"/*": {"origins": "*"}})

BACKEND_URL = os.getenv("BACKEND_URL_SERVER")
OLLAMA_URL = os.getenv("OLLAMA_URL_SERVER")
json
cred = credentials.Certificate(
    os.getenv("FIREBASE_CREDENTIALS")
)
firebase_admin.initialize_app(cred)

# def ollama_request(model, prompt, image=None):
#     url = f"{OLLAMA_URL}/api/generate"
#     data = {
#         "model": model,
#         "prompt": prompt,
#         "stream": False
#     }
#     if image:
#         data["images"] = [image]

#     response = requests.post(url, json=data)
#     if response.status_code == 200:
#         return response.json()["response"]
#     else:
#         raise Exception(f"Ollama request failed: {response.text}")


def ollama_request(model, prompt, image=None):
    url = f"{OLLAMA_URL}/api/generate"
    data = {"model": model, "prompt": prompt, "stream": False}
    if image:
        data["images"] = [image]

    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.HTTPHEADER, ["Content-Type: application/json"])
    c.setopt(c.POST, 1)
    c.setopt(c.POSTFIELDS, json.dumps(data))

    try:
        c.perform()
        status_code = c.getinfo(pycurl.HTTP_CODE)
        if status_code == 200:
            body = buffer.getvalue().decode("utf-8")
            return json.loads(body)["response"]
        else:
            raise Exception(
                f"Ollama request failed: {buffer.getvalue().decode('utf-8')}"
            )
    finally:
        c.close()


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/verify_token", methods=["POST"])
def verify_token():
    id_token = request.json["idToken"]
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
        email = decoded_token["email"]
        session["logged_in"] = True
        session["user_type"] = "user"
        session["email"] = email
        session["uuid"] = hashlib.sha256(email.encode()).hexdigest()
        session["username"] = email.split("@")[0]
        return jsonify({"success": True}), 200
    except auth.InvalidIdTokenError:
        return jsonify({"error": "Invalid token"}), 400


@app.route("/login", methods=["POST"])
def handle_login():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    user_type = request.form.get("user_type")

    if username and password:  # Add your authentication logic here
        session["logged_in"] = True
        session["user_type"] = user_type
        session["email"] = email
        session["username"] = username
        session["uuid"] = hashlib.sha256(username.encode()).hexdigest()
        logging.info(f"User {username} logged in")
        if user_type == "user":
            return redirect(url_for("index"))
        else:
            return redirect("http://localhost:8501")
    else:
        return render_template("login.html", error="Invalid credentials")


@app.route("/get_profile", methods=["GET"])
def get_profile():
    if not session.get("logged_in"):
        return jsonify({"error": "Not logged in"}), 401

    return jsonify({"username": session["username"], "email": session["email"]})


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/index")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in") or session.get("user_type") != "admin":
        return redirect(url_for("login"))
    return render_template("dash.html")

@app.route('/payment-confirmation', methods=['GET'])
def payment_confirmation():
    return render_template('payment_confirmation.html')


import stripe

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@app.route('/api/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        data = request.json
        amount = data['amount']

        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency='usd',
            automatic_payment_methods={
                'enabled': True,
            },
        )

        return jsonify({
            'clientSecret': intent.client_secret
        })
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route('/cart')
def checkout():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('cart.html')

@app.route('/bundles')
def bundles():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('cart.html')

@app.route('/profile')
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('profile.html')

from flask import jsonify, request, session

@app.route('/get_user_data', methods=['GET'])
def get_user_data():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not logged in'}), 401
    
    user = users_collection.find_one({'email': session['email']})
    if(user.get('name')):
        name = user.get('name')
    else:
        name = session['username']
    if user:
        return jsonify({
            'name': name,
            'age': user.get('age'),
            'gender': user.get('gender'),
            'location': user.get('location'),
            'description': user.get('description'),
            'prompt': user.get('prompt'),
        })
    return jsonify({}), 404

@app.route('/save_user_data', methods=['POST'])
def save_user_data():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    users_collection.update_one(
        {'email': session['email']},
        {'$set': {
            'name': data.get('name'),
            'age': data.get('age'),
            'gender': data.get('gender'),
            'location': data.get('location'),
            'description': data.get('description')
        }},
        upsert=True
    )
    return jsonify({'message': 'Profile saved successfully'}), 200

@app.route('/save_prompt', methods=['POST'])
def save_prompt():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    users_collection.update_one(
        {'email': session['email']},
        {'$set': {'prompt': data.get('prompt')}},
        upsert=True
    )
    return jsonify({'message': 'Prompt saved successfully'}), 200

@app.route('/get_orders', methods=['GET'])
def get_orders():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not logged in'}), 401
    
    # Placeholder for order retrieval logic
    # Replace this with actual order retrieval from your database
    orders = [
        {'id': '1', 'date': '2023-08-30', 'status': 'Shipped'},
        {'id': '2', 'date': '2023-08-29', 'status': 'Processing'}
    ]
    return jsonify(orders), 200

@app.route('/view-product', methods=['POST'])
def view_product():
    if 'email' not in session:
        return jsonify({'success': False, 'error': 'User not logged in'}), 401

    product_id = request.json.get('product_id')
    email = session['email']

    try:
        users_collection.update_one(
            {'email': email},
            {'$addToSet': {'viewed': product_id}},
            upsert=True
        )
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error viewing product: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# @app.route('/add-to-cart', methods=['POST'])
# def add_to_cart():
#     if 'email' not in session:
#         return jsonify({'success': False, 'error': 'User not logged in'}), 401

#     product_id = request.json.get('product_id')
#     email = session['email']

#     try:
#         users_collection.update_one(
#         {'email': email},
#         {'$inc': {'cart.' + product_id: 1}},
#         upsert=True
#     )
#         return jsonify({'success': True})
#     except Exception as e:
#         print(f"Error adding product to cart: {e}")
#         return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if 'email' not in session:
        return jsonify({'success': False, 'error': 'User not logged in'}), 401

    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity', 1)  # Default to 1 if quantity not provided
    email = session['email']

    try:
        users_collection.update_one(
            {'email': email},
            {'$set': {f'cart.{product_id}': quantity}},
            upsert=True
        )
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error adding product to cart: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/get_cart_items', methods=['GET'])
def get_cart_items():
    if not session.get('logged_in'):
        return jsonify([])

    user = users_collection.find_one({'email': session['email']})
    
    if not user or 'cart' not in user:
        return jsonify([])

    cart_items = []
    
    for product_id, quantity in user['cart'].items():
        try:
            product = next((p for p in database if p['id'] == str(product_id)), None)
            if not product:
                product = next((p for p in database if p['id'] == int(product_id)), None)
        except Exception as e:
            print(f"Error fetching product details: {str(e)}")
            continue

        try:
            image_data = next((p for p in imgDatabase if p['id'] == str(product_id)), None)
            if not image_data:
                image_data = next((p for p in imgDatabase if p['id'] == int(product_id)), None)
        except Exception as e:
            print(f"Error fetching image data: {str(e)}")
            continue

        if product:
            cart_items.append({
                'id': product['id'],
                'price': float(product['price']),
                'image': image_data['image'],
                'quantity': quantity
            })

    return jsonify(cart_items)


@app.route('/update_cart_quantity', methods=['POST'])
def update_cart_quantity():
    if not session.get('logged_in'):
        return jsonify({'success': False, 'error': 'User not logged in'}), 401

    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity')
    email = session['email']

    if quantity < 1:
        return jsonify({'success': False, 'error': 'Quantity must be at least 1'}), 400

    try:
        users_collection.update_one(
            {'email': email},
            {'$set': {f'cart.{product_id}': quantity}},
            upsert=True
        )
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error updating cart quantity: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route("/get_details", methods=["POST"])
def get_details():
    if not session.get("logged_in"):
        return jsonify({"error": "Not logged in"}), 401

    product_id = request.json.get("id")
    print("Product ID:", product_id)

    id_data = {"id": str(product_id)}

    try:
        data = id_data
        # response = requests.post(f"{BACKEND_URL}/getCategories", json=id_data)
        # if response.ok:
        id = data["id"]
        # data=mongoDatabase["database"].find({"id":int(id)},{"_id":0})
        # data=mongoDatabase["database_500"].find({"id":str(id)},{"_id":0})
        try:
            data = mongoDatabase[DATABASE_NAME].find({"id": str(id)}, {"_id": 0})
            imageData = getImage(imgDatabase, str(id))
            data_send = list(data)[0]

        except Exception as e:
            data = mongoDatabase[DATABASE_NAME].find({"id": int(id)}, {"_id": 0})
            imageData = getImage(imgDatabase, int(id))
            data_send = list(data)[0]
        data_send["image"] = imageData
        product_details = data_send
        return jsonify(product_details)
        # else:
        #     return jsonify({"error": f"Backend error: {response.text}"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error communicating with backend: {str(e)}"}), 500


@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    if not session.get("logged_in"):
        return jsonify({"error": "Not logged in"}), 401

    desc = request.form.get("description")
    image = request.files.get("image")

    data = {}
    if desc:
        data["text"] = desc

    print("Sending to FastAPI:", data)

    if image and image.filename:
        try:
            img = Image.open(image)
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            image_data = base64.b64encode(buffered.getvalue()).decode()
            data["img64"] = image_data
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return jsonify({"error": f"Error processing image: {str(e)}"}), 500

    textCategories = None
    imgCategories = None
    text = data.get("text", None)
    img64 = data.get("img64", None)
    if img64:
        if img64[0] == "b":
            img64 = img64[2:-1]
    categories = {}
    print(text)
    if text != None:
        textCategories = getCategoriesFromQuery("mistral:latest", text, ollama=True)[
            "categories"
        ][0]
    if img64 != None:
        imgCategories = getcategoriesFromImage(
            "llava-phi3:latest", imagePath=None, imgb64=img64, ollama=True
        )["categories"][0]
    if text != None and img64 != None:
        for key in textCategories.keys():
            categories[key] = list(set(textCategories[key] + imgCategories[key]))
    elif text != None:
        categories = textCategories
    else:
        categories = imgCategories
    print(categories)
    results = find_top_k_similar(categories, database, top_k=5)
    l = []
    for result in results:
        result[1]["image"] = getImage(imgDatabase, result[1]["id"])
        l.append(result[1])

    return l

    # try:
    #     response = requests.post(f"{BACKEND_URL}/data", json=data)

    #     if response.ok:
    #         result = response.json()
    #         return jsonify(result)
    #     else:
    #         return jsonify({"error": f"FastAPI error: {response.text}"}), 500
    # except requests.exceptions.RequestException as e:
    #     print(f"Error communicating with FastAPI: {str(e)}")
    #     return jsonify({"error": f"Error communicating with FastAPI: {str(e)}"}), 500
    # except Exception as e:
    #     print(f"Unexpected error: {str(e)}")
    #     print(traceback.format_exc())
    #     return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route("/item/<string:item_id>")
def item_page(item_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("item.html", item_id=str(item_id))


@app.route("/save_chat_history", methods=["POST"])
def save_chat_history():
    if not session.get("logged_in"):
        return jsonify({"error": "Not logged in"}), 401

    user_uuid = session["uuid"]
    data = request.json

    # Create a unique file for each user
    user_file = f"chat_history_{user_uuid}.json"

    user_data = {
        "email": session["email"],
        "last_updated": datetime.now().isoformat(),
        "conversations": data["conversations"],
        "currentConversationId": data["currentConversationId"],
    }

    with open(user_file, "w") as f:
        json.dump(user_data, f)

    return jsonify({"message": "Chat history saved successfully"}), 200


@app.route("/get_chat_history", methods=["GET"])
def get_chat_history():
    if not session.get("logged_in"):
        return jsonify({"error": "Not logged in"}), 401

    user_uuid = session["uuid"]
    user_file = f"chat_history_{user_uuid}.json"

    if os.path.exists(user_file):
        with open(user_file, "r") as f:
            user_history = json.load(f)
        return jsonify(user_history), 200
    else:
        return jsonify({"conversations": {}, "currentConversationId": None}), 200

@app.route("/product_chat", methods=["POST"])
def product_chat():
    if not session.get("logged_in"):
        return jsonify({"error": "Not logged in"}), 401

    product_id = request.json.get("id")
    user_message = request.json.get("message")
    product_description = request.json.get("description", "")

    try:
        # Fetch product details from FastAPI backend
        # response = requests.post(f"{BACKEND_URL}/getCategories", json={"id": product_id})
        data = {"id": product_id}
        id = data["id"]
        # data=mongoDatabase["database"].find({"id":int(id)},{"_id":0})
        # data=mongoDatabase["database_500"].find({"id":str(id)},{"_id":0})
        try:
            data = mongoDatabase[DATABASE_NAME].find({"id": str(id)}, {"_id": 0})
            imageData = getImage(imgDatabase, str(id))
            data_send = list(data)[0]

        except Exception as e:
            data = mongoDatabase[DATABASE_NAME].find({"id": int(id)}, {"_id": 0})
            imageData = getImage(imgDatabase, int(id))
            data_send = list(data)[0]
        data_send["image"] = imageData
        # print(data_send)
        product_details = data_send
        del product_details["image"]
        print("These are the product details: ", product_details)
        # Generate a prompt for Llama 3.1
        prompt = f"""
        You are an AI shopping assistant. You have the following product details:
        {product_details}
        Product description: {product_description}
        The customer asks: {user_message}
        Provide a helpful and informative response based on the product details and description.
        """
        # Generate response using Llama 3.1
        response = ollama_request("mistral:latest", prompt)
        return jsonify({"response": response})

        # if response.ok:
        #     product_details = response.json()
        #     del(product_details['image'])
        #     print("These are the product details: ", product_details)

        #     # Generate a prompt for Llama 3.1
        #     prompt = f"""
        #     You are an AI shopping assistant. You have the following product details:
        #     {product_details}

        #     Product description: {product_description}

        #     The customer asks: {user_message}

        #     Provide a helpful and informative response based on the product details and description.
        #     """

        #     # Generate response using Llama 3.1
        #     response = ollama_request("mistral:latest", prompt)

        #     return jsonify({"response": response})
        # else:
        #     return jsonify({"error": f"Backend error: {response.text}"}), 500
    except Exception as e:
        return (
            jsonify(
                {
                    "error": f"Error in product chat: {str(e)} this is payload {product_details.keys()}"
                }
            ),
            500,
        )


@app.route("/generate_image_description", methods=["POST"])
def generate_image_description():
    if not session.get("logged_in"):
        return jsonify({"error": "Not logged in"}), 401

    product_id = request.json.get("id")

    try:
        # Fetch product details from FastAPI backend
        # response = requests.post(f"{BACKEND_URL}/getCategories", json={"id": product_id})
        # if response.ok:
        data = {"id": product_id}
        id = data["id"]
        # data=mongoDatabase["database"].find({"id":int(id)},{"_id":0})
        # data=mongoDatabase["database_500"].find({"id":str(id)},{"_id":0})
        try:
            data = mongoDatabase[DATABASE_NAME].find({"id": str(id)}, {"_id": 0})
            imageData = getImage(imgDatabase, str(id))
            data_send = list(data)[0]

        except Exception as e:
            data = mongoDatabase[DATABASE_NAME].find({"id": int(id)}, {"_id": 0})
            imageData = getImage(imgDatabase, int(id))
            data_send = list(data)[0]
        data_send["image"] = imageData
        product_details = data_send
        image_data = product_details.get("image")
        if image_data:
            if image_data[0] == "b":
                image_data = image_data[2:-1]

        if not image_data:
            return jsonify({"error": "No image data found"}), 400

        # Generate image description using LLaVA
        prompt = "Describe this product image in detail."
        description = ollama_request("llava-phi3:latest", prompt, image=image_data)

        return jsonify({"description": description})
        # else:
        #     return jsonify({"error": f"Backend error: {response.text}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error generating image description: {str(e)}"}), 500


@app.get("/getHistory")
async def getHistory(data: dict):
    id = data["currentConversationId"]
    data = mongoDatabase["history"].find({"currentConversationId": id}, {"_id": 0})
    data = list(data)[0]
    return data


@app.post("/addHistory")
async def addHistory(data: dict):
    incoming_data = data
    id = incoming_data["currentConversationId"]
    current_data = mongoDatabase["history"].find(
        {"currentConversationId": id}, {"_id": 0}
    )
    current_data = list(current_data)
    if current_data != []:
        conversations = incoming_data["conversations"]
        last_updated = incoming_data["last_updated"]
        x = mongoDatabase["history"].update_one(
            {"currentConversationId": id},
            {"$set": {"conversations": conversations, "last_updated": last_updated}},
        )
        print(x)
    else:
        x = mongoDatabase["history"].insert_one(data)
        print(x)


@app.post("/addOne")
async def addOne(data: dict):
    """
    Payload
    {"data":{
                "id":0,
                "price":123,
                "Main category":[],
                "Sub categories":[],
                "Additional details":[]
            },
            "imgData":{
                  "id":0,
                  "image":"b'/9j/4AAQSk'"
              }
    }
    """
    if data.get("data", None):
        print("inserting into main database")
        try:
            x = mongoDatabase["database"].insert_one(data["data"])
            print(x)
        except Exception as e:
            print(e)
            print("Error inserting into main database")

    if data.get("imgData", None):
        print("inserting into image database")
        try:
            x = mongoDatabase["imageDatabase"].insert_one(data["imgData"])
            print(x)
        except Exception as e:
            print("Error inserting into image database")


@app.post("/removeOne")
async def removeOne(data: dict):
    """
    Payload : 0(any integer, id to be removed)
    """
    id = data["id"]
    print("deleting from database")
    try:
        x = mongoDatabase["database"].delete_one({"id": id})
        print(x)
    except Exception as e:
        print("Error deleting from main database")

    try:
        x = mongoDatabase["imageDatabase"].delete_one({"id": id})
        print(x)
    except Exception as e:
        print("Error deleting image database")


@app.post("/addMany")
async def addMany(data: dict):
    """
    payload
    {
        "data":[{
            "id":0,
            "price":123,
            "Main category":[],
            "Sub categories":[],
            "Additional details":[]
        },{
            "id":0,
            "price":123,
            "Main category":[],
            "Sub categories":[],
            "Additional details":[]
        }],
        "imgData":[{
            "id":0,
            "image":"b'/9j/4AAQSk'"

        },{
            "id":0,
            "image":"b'/9j/4AAQSk'"

        }]
    }
    """
    if data.get("data", None):
        print("inserting many into database")
        try:
            x = mongoDatabase["database"].insert_many(data.get("data"))
            print(x)
        except Exception as e:
            print("Error inserting many into main database")

    if data.get("imgData", None):
        try:
            x = mongoDatabase["imageDatabase"].insert_many(data.get("imgData"))
            print(x)
        except Exception as e:
            print("Error inserting many into image database")


# @app.route("/personal_recommendations",methods=["POST"])
# def personal_recommendations():
#     """
#         {
#       "user_id":123,
#       "categories":["clothes", "t-shirt","Mens fashion"],
#       "already_bought":[452,532]
#     }
#     """
#     if not session.get("logged_in"):
#         return jsonify({"error": "Not logged in"}), 401
#     # preffered_categories = request.json.get("categories")
#     # already_bought = request.json.get("already_bought")
#     # user_id = request.json.get("user_id")

#     user_visited_ids = users_collection.find_one({'email': session['email']}).get('visited')
#     user_order_ids = users_collection.find_one({'email': session['email']}).get('cart')




#     return {user_id:get_personal_recommendations(preffered_categories,database,already_bought,10)}

def append_images_to_recommendations(basket_data, imgDatabase):
    updated_basket_data = []
    
    for score, product in basket_data:
        product_id = product['id']
        
        # Find the corresponding image in the imgDatabase
        image_entry = next((img for img in imgDatabase if img['id'] == product_id), None)
        
        if image_entry:
            # Append the image URL to the product information
            product['image'] = image_entry.get('image', '')
        else:
            # If no image is found, add a placeholder or leave it empty
            product['image'] = ''
        
        updated_basket_data.append((score, product))
    
    return updated_basket_data


products_collection = mongoDatabase[DATABASE_NAME]
@app.route("/personal_recommendations", methods=["GET"])
def personal_recommendations():
    if not session.get("logged_in"):
        return jsonify({"error": "Not logged in"}), 401
    
    user_email = session.get("email")  # Get email from session
    if not user_email:
        return jsonify({"error": "User email not found in session"}), 400

    # Fetch user data
    user = users_collection.find_one({"email": user_email})
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Get product IDs from cart and viewed
    cart_product_ids = list(user.get('cart', {}).keys())
    viewed_product_ids = user.get('viewed', [])
    product_ids = cart_product_ids + viewed_product_ids
    
    # Get categories from these products
    categories = []
    for product_id in product_ids:
        product = products_collection.find_one({"id": product_id})
        if product:
            categories.extend(product.get('Main category', []))
            categories.extend(product.get('Sub categories', []))
            categories.extend(product.get('Additional details', []))

    # Remove duplicates
    categories = list(set(categories))

    # Get already bought products
    already_bought = [order['product_id'] for order in user.get('orders', [])]

    user_basket_data = {
        "user_id": user_email,
        "categories": categories,
        "already_bought": already_bought}
    print(user_basket_data)
    basket_data= get_personal_recommendations(user_basket_data['categories'], list( mongoDatabase[DATABASE_NAME].find({}, {"_id": 0})), user_basket_data['already_bought'], 10)
    updated_basket_data = append_images_to_recommendations(basket_data, imgDatabase)
    print(updated_basket_data)
    return jsonify(updated_basket_data)
    


@app.route("/generate_custom_image", methods=["POST"])
def generate_custom_image():
    if not session.get("logged_in"):
        return jsonify({"error": "Not logged in"}), 401
    query = request.form.get("description")
    return queue_prompt(query, steps=1)

if __name__ == "__main__":
    # app.run(debug=True,port=5002)
    app.run(debug=True)
