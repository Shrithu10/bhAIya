# import streamlit as st
# import pymongo
# from pymongo import MongoClient
# import base64
# from PIL import Image
# from io import BytesIO
# import requests
# import pandas as pd

# from streamlit_navigation_bar import st_navbar

# page = st_navbar(["Home" ,"Add","Remove" ,"Products" ,"Sales","Customer details ","Support"])

# # st.logo("C:/Users/Administrator 1/Desktop/baby.jpg")

# ##08082A;
# ##extra colour replacement

# st.markdown(
#     """
#     <style>
#     [data-testid="stAppViewContainer"] > .main {
#         background-color: #000018;  /* Black background */
#         color: #fff;  /* White text */
#     }

#     [data-testid="stForm"] {
#         background-color: #fff;  /* White form background */
#         color: #000;  /* Black form text */
#     }

#     label, span,h1,h3{
#         color: #fff;  /* White text for headings, paragraphs, labels, spans, and list items */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
# if page =="Home":
#     st.title('bhAIya')
#     st.title('Seller Dashboard')

# # MongoDB connection
# client = MongoClient('localhost', 27017)
# db = client['bhAIya']
# collection_a = db['database']
# collection_i = db['imageDatabase']


# # Function to encode image to Base64
# def encode_image(image):
#     buffered = BytesIO()
#     image.save(buffered, format="JPEG")
#     return base64.b64encode(buffered.getvalue()).decode()

# # Function to decode Base64 to image
# def decode_image(encoded_image):
#     image_bytes = base64.b64decode(encoded_image)
#     return Image.open(BytesIO(image_bytes))

# # Streamlit app code
# #action = st.selectbox('Choose Action', ['Add Item', 'Delete Item', 'Upload Image',])


# base_url = "http://127.0.0.1:5004"


# import requests
# if page =="Add":
#     st.title('bhAIya - Add products')

#     actions = ['Select an action', 'Add Item','Upload Image']

#     # Use the selectbox with a default placeholder option
#     action = st.selectbox('Choose Action', actions)
#     # Add Item Form
#     if action == 'Add Item':
#         with st.form(key='add_item_form'):
#             new_id = st.text_input('ID')
#             new_masterCategory = st.text_input('Master Category')
#             new_sub_categories = st.text_input('Product Display Name')
#             new_additional_details = st.text_input('Additional Details')
#             new_price = st.text_input('Price')
#             submit_button = st.form_submit_button(label='Submit')

#             if submit_button:
#                 new_item = {
#                     'Main category': new_masterCategory.split(','),
#                     'Sub categories': new_sub_categories.split(','),
#                     'Additional details': new_additional_details.split(','),
#                     'id': int(new_id),
#                     'price': float(new_price),
#                 }
#                 response = requests.post(base_url+"/addOne", json={"data": new_item})
#                 if response.status_code == 200:
#                     st.success('Item added successfully!')
#                 else:
#                     st.error('Failed to add item.')

#     # Delete Item Form


#     # Upload Image Form
#     elif action == 'Upload Image':
#         with st.form(key='upload_image_form'):
#             image_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
#             image_id = st.text_input('Image ID')
#             submit_button = st.form_submit_button(label='Upload')

#             if submit_button and image_file:
#                 image = Image.open(image_file)
#                 encoded_image = encode_image(image)
#                 image_item = {

#                     'image': "b'"+ encoded_image,
#                     'id': int(image_id),
#                 }
#                 response = requests.post(base_url+"/addOne", json={"imgData": image_item})
#                 if response.status_code == 200:
#                     st.success('Image uploaded successfully!')
#                 else:
#                     st.error('Failed to upload image.')

# if page =="Remove":
#     st.title('bhAIya - Remove products')

#     with st.form(key='delete_item_form'):
#         delete_id = st.text_input('ID to delete')
#         submit_button = st.form_submit_button(label='Submit')

#         if submit_button:
#             try:
#                 # Convert the ID to the appropriate type (int, if necessary)
#                 response = requests.post(base_url+"/removeOne", json={"id": int(delete_id)})

#                 if response.status_code == 200:
#                     st.success('Item deleted successfully!')
#                 else:
#                     st.error(f'Failed to delete item: {response.json().get("detail", "Unknown error")}')
#             except ValueError:
#                 st.error("Invalid ID format. Please enter a numeric ID.")


# st.write()
# st.write()
# st.write()
# if page =="Products":
#     st.title('bhAIya')
#     items = list(collection_a.find())

#     # Convert items to DataFrame
#     df = pd.DataFrame(items)
#     st.subheader('Item List')
#     # Display first 10 items and allow scrolling for others
#     st.dataframe(df.head(100), height=300)

# import streamlit as st
# import pymongo
# from pymongo import MongoClient
# import base64
# from PIL import Image
# from io import BytesIO
# import requests
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go

# from utils import getcategoriesFromImage,getCategoriesFromText

# # Custom CSS for a visually appealing dashboard
# st.markdown(
#     """
# <style>
#     /* Main container */
#     .main {
#         background-color: #1E1E1E;
#         color: #FFFFFF;
#     }

#     /* Headings */
#     h1, h2, h3 {
#         color: #90EE90;  /* Light green for more subtle headings */
#         font-family: 'Helvetica Neue', sans-serif;
#     }

#     /* Subheadings and labels */
#     label, .stSelectbox label {
#         color: #BDBDBD;
#         font-weight: 500;
#     }

#     /* Forms */
#     [data-testid="stForm"] {
#         background-color: #2C2C2C;
#         padding: 20px;
#         border-radius: 10px;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#     }

#     /* Input fields */
#     .stTextInput > div > div > input,
#     .stTextArea > div > div > textarea,
#     .stSelectbox > div > div > select {
#         background-color: #3C3C3C;
#         color: #FFFFFF;
#         border: 1px solid #4CAF50;
#         border-radius: 5px;
#     }

#     /* Buttons */
#     .stButton > button {
#         background-color: #4CAF50;
#         color: #FFFFFF;
#         border: none;
#         border-radius: 5px;
#         padding: 10px 20px;
#         font-weight: bold;
#         transition: all 0.3s ease;
#     }

#     .stButton > button:hover {
#         background-color: #45a049;
#         box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
#     }

#     /* File uploader */
#     .stFileUploader > div > button {
#         background-color: #2196F3;
#         color: #FFFFFF;
#         border: none;
#         border-radius: 5px;
#         padding: 10px 20px;
#         font-weight: bold;
#         transition: all 0.3s ease;
#     }

#     .stFileUploader > div > button:hover {
#         background-color: #1E88E5;
#         box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
#     }

#     /* Dataframe */
#     .stDataFrame {
#         border: 1px solid #4CAF50;
#         border-radius: 5px;
#     }

#     /* Success and error messages */
#     .stSuccess, .stError {
#         padding: 10px;
#         border-radius: 5px;
#         margin-top: 10px;
#     }

#     .stSuccess {
#         background-color: rgba(76, 175, 80, 0.1);
#         border: 1px solid #4CAF50;
#     }

#     .stError {
#         background-color: rgba(244, 67, 54, 0.1);
#         border: 1px solid #F44336;
#     }
# </style>
# """,
#     unsafe_allow_html=True,
# )

# # MongoDB connection
# client = MongoClient("localhost", 27017)
# db = client["bhAIya"]
# collection_a = db["database"]
# collection_i = db["imageDatabase"]

# base_url = "http://127.0.0.1:5004"
# categories = {}
# all_data=collection_a.find()
# total_products = collection_a.count_documents({})


# # Function to encode image to Base64
# def encode_image(image):
#     buffered = BytesIO()
#     image.save(buffered, format="JPEG")
#     return base64.b64encode(buffered.getvalue()).decode()


# # Function to decode Base64 to image
# def decode_image(encoded_image):
#     image_bytes = base64.b64decode(encoded_image)
#     return Image.open(BytesIO(image_bytes))

# def get_category_count(all_data,categories={}):
#     for data in all_data:
#         cat=data["Main category"][0]
#         categories[cat]=categories.get(cat,0)+1
#     return len(categories)

# def get_total_price():
#     all_data=collection_a.find()
#     total_price=0
#     for data in all_data:
#         total_price+=data["price"]
#     print(total_price)
#     return total_price

# def preprocess_for_pie(categories):
#     categories_name=[]
#     categories_count=[]
#     for key in sorted(categories,key=categories.get,reverse=True)[:15]:
#         categories_name.append(key)
#         categories_count.append(categories[key])
#     categories_name.append("Others")
#     categories_count.append(sum([categories[key] for key in categories.keys() if key not in categories_name]))
#     return categories_name,categories_count

# def get_for_price_distribution():
#     min_price = collection_a.find_one(sort=[("price", 1)])["price"]
#     max_price = collection_a.find_one(sort=[("price", -1)])["price"]
#     range_size = (max_price - min_price) / 10
#     price_ranges = [f"Rs. {min_price + i * range_size:.2f} - Rs. {min_price + (i + 1) * range_size:.2f}" for i in range(10)]
#     product_counts = [collection_a.count_documents({"price": {"$gte": min_price + i * range_size, "$lt": min_price + (i + 1) * range_size}}) for i in range(10)]
#     return price_ranges, product_counts


# st.title("bhAIya Analytics Dashboard")

# # Sidebar for Add and Remove functions
# st.sidebar.title("Product Management")

# # Add Item Form
# st.sidebar.subheader("Add Item")
# with st.sidebar.form(key="add_item_form"):
#     new_id = st.text_input("ID")
#     new_prod_description = st.text_area("Product description")
#     new_price = st.text_input("Price")
#     submit_button = st.form_submit_button(label="Add Item")

#     if submit_button:
#         new_item = getCategoriesFromText("mistral:latest",new_prod_description,ollama=True)["categories"][0]
#         new_item["id"] = int(new_id)
#         new_item["price"] = float(new_price)
#         print(new_item)
#         response = requests.post(base_url + "/addOne", json={"data": new_item})
#         if response.status_code == 200:
#             st.sidebar.success("Item added successfully!")
#         else:
#             st.sidebar.error("Failed to add item.")

# # Remove Item Form
# st.sidebar.subheader("Remove Item")
# with st.sidebar.form(key="delete_item_form"):
#     delete_id = st.text_input("ID to delete")
#     submit_button = st.form_submit_button(label="Remove Item")

#     if submit_button:
#         try:
#             response = requests.post(
#                 base_url + "/removeOne", json={"id": int(delete_id)}
#             )

#             if response.status_code == 200:
#                 st.sidebar.success("Item deleted successfully!")
#             else:
#                 st.sidebar.error(
#                     f'Failed to delete item: {response.json().get("detail", "Unknown error")}'
#                 )
#         except ValueError:
#             st.sidebar.error("Invalid ID format. Please enter a numeric ID.")

# # Main content area with placeholder charts
# # Placeholder metrics
# col1, col2, col3 = st.columns(3)
# with col1:
#     st.metric("Total Products", total_products)
# with col2:
#     st.metric("Total Categories", get_category_count(all_data,categories))
# with col3:
#     st.metric("Average Price", f"Rs. {get_total_price()/ total_products}")

# # Placeholder chart: Product Category Distribution
# st.subheader("Product Category Distribution")
# categories_name,categories_count=preprocess_for_pie(categories)
# fig = px.pie(values=categories_count, names=categories_name, title="Product Categories")
# st.plotly_chart(fig)

# # Placeholder chart: Price Distribution
# st.subheader("Price Distribution")
# price_ranges,product_counts=get_for_price_distribution()
# fig = px.bar(x=price_ranges, y=product_counts, title="Price Distribution", labels={"x": "Price Range", "y": "Number of Products"})
# st.plotly_chart(fig)


# # Footer
# st.markdown("---")
# st.markdown("© 2024 bhAIya Seller Dashboard. All rights reserved.")


import streamlit as st
import pymongo
from pymongo import MongoClient
import base64
from PIL import Image
from io import BytesIO
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils import getcategoriesFromImage, getCategoriesFromText

# Custom CSS for a visually appealing dashboard
st.markdown(
    """
<style>
    /* Main container */
    .main {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #90EE90;  /* Light green for more subtle headings */
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Subheadings and labels */
    label, .stSelectbox label {
        color: #BDBDBD;
        font-weight: 500;
    }
    
    /* Forms */
    [data-testid="stForm"] {
        background-color: #2C2C2C;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: #3C3C3C;
        color: #FFFFFF;
        border: 1px solid #4CAF50;
        border-radius: 5px;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #4CAF50;
        color: #FFFFFF;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #45a049;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    
    /* File uploader */
    .stFileUploader > div > button {
        background-color: #2196F3;
        color: #FFFFFF;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > button:hover {
        background-color: #1E88E5;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    
    /* Dataframe */
    .stDataFrame {
        border: 1px solid #4CAF50;
        border-radius: 5px;
    }
    
    /* Success and error messages */
    .stSuccess, .stError {
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
    
    .stSuccess {
        background-color: rgba(76, 175, 80, 0.1);
        border: 1px solid #4CAF50;
    }
    
    .stError {
        background-color: rgba(244, 67, 54, 0.1);
        border: 1px solid #F44336;
    }
</style>
""",
    unsafe_allow_html=True,
)

# MongoDB connection
client = MongoClient("localhost", 27017)
db = client["bhAIya"]
collection_a = db["database"]
collection_i = db["imageDatabase"]

base_url = "http://127.0.0.1:5000"


# Function to encode image to Base64
def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()


# Function to decode Base64 to image
def decode_image(encoded_image):
    image_bytes = base64.b64decode(encoded_image)
    return Image.open(BytesIO(image_bytes))


@st.cache_data
def fetch_data():
    all_data = list(collection_a.find())
    return all_data


def process_data(all_data):
    total_products = len(all_data)
    categories = {}
    total_price = 0
    for data in all_data:
        cat = data["Main category"][0]
        categories[cat] = categories.get(cat, 0) + 1
        total_price += data["price"]

    avg_price = total_price / total_products if total_products > 0 else 0
    return total_products, len(categories), avg_price, categories


def preprocess_for_pie(categories):
    categories_name = []
    categories_count = []
    for key in sorted(categories, key=categories.get, reverse=True)[:15]:
        categories_name.append(key)
        categories_count.append(categories[key])
    categories_name.append("Others")
    categories_count.append(
        sum(
            [categories[key] for key in categories.keys() if key not in categories_name]
        )
    )
    return categories_name, categories_count


def get_price_distribution(all_data):
    prices = [item["price"] for item in all_data]
    if not prices:
        return [], []
    min_price, max_price = min(prices), max(prices)
    range_size = (max_price - min_price) / 10 if max_price > min_price else 1
    price_ranges = [
        f"Rs. {min_price + i * range_size:.2f} - Rs. {min_price + (i + 1) * range_size:.2f}"
        for i in range(10)
    ]
    product_counts = [
        sum(
            1
            for price in prices
            if min_price + i * range_size <= price < min_price + (i + 1) * range_size
        )
        for i in range(10)
    ]
    return price_ranges, product_counts


st.title("bhAIya Analytics Dashboard")

# Sidebar for Add and Remove functions
st.sidebar.title("Product Management")

# Add Item Form
st.sidebar.subheader("Add Item")
with st.sidebar.form(key="add_item_form"):
    new_id = st.text_input("ID")
    new_prod_description = st.text_area("Product description")
    new_price = st.text_input("Price")
    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
    submit_button = st.form_submit_button(label="Add Item")
    image_categories = None

    if submit_button:
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            encoded_image = encode_image(image)
            collection_i.insert_one({"id": new_id, "image": encoded_image})
            image_categories = getcategoriesFromImage(
                "llava-phi3:latest ", encoded_image, ollama=True
            )["categories"][0]

        text_categories = getCategoriesFromText(
            "mistral:latest", new_prod_description, ollama=True
        )["categories"][0]

        # Combine categories from image and text
        new_item = {}
        if image_categories is not None:
            for key in text_categories.keys():
                new_item[key] = list(set(text_categories[key] + image_categories[key]))
        else:
            new_item = text_categories
        new_item["id"] = int(new_id)
        new_item["price"] = float(new_price)

        response = requests.post(base_url + "/addOne", json={"data": new_item})
        if response.status_code == 200:
            st.sidebar.success("Item added successfully!")
        else:
            st.sidebar.error("Failed to add item.")

# Remove Item Form
st.sidebar.subheader("Remove Item")
with st.sidebar.form(key="delete_item_form"):
    delete_id = st.text_input("ID to delete")
    submit_button = st.form_submit_button(label="Remove Item")

    if submit_button:
        try:
            response = requests.post(
                base_url + "/removeOne", json={"id": int(delete_id)}
            )
            collection_i.delete_one({"id": delete_id})
            if response.status_code == 200:
                st.sidebar.success("Item deleted successfully!")
            else:
                st.sidebar.error(
                    f'Failed to delete item: {response.json().get("detail", "Unknown error")}'
                )
        except ValueError:
            st.sidebar.error("Invalid ID format. Please enter a numeric ID.")

# Fetch and process data
all_data = fetch_data()
total_products, total_categories, avg_price, categories = process_data(all_data)

# Main content area with updated charts
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Products", total_products)
with col2:
    st.metric("Total Categories", total_categories)
with col3:
    st.metric("Average Transaction Sale", f"Rs. {avg_price:.2f}")

# Product Category Distribution
st.subheader("Product Category Distribution")
categories_name, categories_count = preprocess_for_pie(categories)
fig = px.pie(values=categories_count, names=categories_name, title="Product Categories")
st.plotly_chart(fig)

# Price Distribution
st.subheader("Price Distribution")
price_ranges, product_counts = get_price_distribution(all_data)
fig = px.bar(
    x=price_ranges,
    y=product_counts,
    title="Price Distribution",
    labels={"x": "Price Range", "y": "Number of Products"},
)
st.plotly_chart(fig)

# Footer
st.markdown("---")
st.markdown("© 2024 bhAIya Seller Dashboard. All rights reserved.")
