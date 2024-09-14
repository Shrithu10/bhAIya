#{
# "customer_id": 1,
#"customer_name": "Evelyn Martinez",
#"avg_purchase_value": 1562.32,
#"discount_usage": 5,
#  "purchase_frequency": 15,
#  "product_tags": [
#    "electronics"
#  ],
#  "product_category": "electronics",
#  "subcategory": [
#    "smartphones",
#    "laptops"
#  ],
#  "purchase_recency": 12,
#  "geo_location": "North America"
#}

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
#         new_item = getCategoriesFromText("mistral",new_prod_description,ollama=True)["categories"][0]
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
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import requests
from mpl_toolkits.mplot3d import Axes3D

# Function to load data from a GET request
def load_data_from_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        df = pd.DataFrame(data)
        # Convert product_tags from list to a string
        df['product_tags'] = df['product_tags'].apply(lambda x: ', '.join(x))
        # Ensure columns are properly named and typed
        df.columns = [col.lower() for col in df.columns]
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# URL for the GET request (Replace with your actual endpoint)
api_url = "http://localhost:5000/get_data"

# Load data from the API
df = load_data_from_api(api_url)

# Add a mock 'cluster' column for demonstration
if not df.empty:
    df['cluster'] = np.random.choice(['High', 'Medium', 'Low'], size=len(df))

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

base_url = "http://127.0.0.1:5004"


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
            collection_i.insert_one({"id": new_id
                                     , "image": encoded_image})
            image_categories = getcategoriesFromImage(
                "mistral", encoded_image, ollama=True
            )["categories"][0]

        text_categories = getCategoriesFromText(
            "mistral", new_prod_description, ollama=True
        )["categories"][0]

        # Combine categories from image and text
        new_item = {}
        if(image_categories is not None):
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
op=st.selectbox(
        'Select ',
        ['Products Dashboard','Customer segemntation analysis']
    )
if op == 'Products Dashboard':
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
elif op=='Customer segemntation analysis':
    option = st.selectbox(
    'Select Clustering Type',
    ['Value-Based Clustering', 'Product Interest Clustering', 'RFM Clustering',
     'Discount Sensitivity Clustering', 'Geo-Location-Based Clustering', 
     'Purchase Frequency-Based Clustering', 'Behavioral Clustering', 'Combination Clustering', 
     ]
    )

    if option == 'Value-Based Clustering':
        st.header('Value-Based Clustering')

        # Sub-buttons for Value-Based Clustering
        sub_option = st.selectbox(
            'Select Visualization',
            ['Scatter Plot of Avg Purchase Value vs Purchase Frequency', 'Spending Analysis', 'Overview']
        )

        if sub_option == 'Scatter Plot of Avg Purchase Value vs Purchase Frequency':
            st.subheader('Scatter Plot of Avg Purchase Value vs Purchase Frequency')
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.scatterplot(x='avg_purchase_value', y='purchase_frequency', hue='cluster', data=df, palette='viridis', ax=ax)
                ax.set_title('Value-Based Clustering')
                ax.set_xlabel('Average Purchase Value')
                ax.set_ylabel('Purchase Frequency')
                st.pyplot(fig)

                cluster_counts = df['cluster'].value_counts()
                st.write(f"**Cluster Counts:**")
                st.write(cluster_counts)

                st.write("""
                    **Explanation:**
                    This scatter plot shows the relationship between Average Purchase Value and Purchase Frequency across different customer clusters.
                    - **Clusters:** The colors indicate different clusters ('High', 'Medium', 'Low').
                    - **Insight:** Customers in the 'High' cluster have both high purchase values and high frequency. This helps in identifying high-value, frequent customers versus those with lower purchase values and frequency.
                """)
            except Exception as e:
                st.error(f"Error: {e}")

        elif sub_option == 'Spending Analysis':
            st.header('Spending Analysis by Cluster')
            st.subheader('Average Spending per Cluster')
            try:
                # Compute average spending per cluster
                avg_spending_per_cluster = df.groupby('cluster')['avg_purchase_value'].mean()
                
                # Display the average spending per cluster
                st.write("**Average Spending per Cluster:**")
                st.write(avg_spending_per_cluster)
                
                # Create a bar plot for average spending
                fig, ax = plt.subplots(figsize=(10, 6))
                avg_spending_per_cluster.plot(kind='bar', ax=ax, color='skyblue')
                ax.set_title('Average Spending per Cluster')
                ax.set_xlabel('Cluster')
                ax.set_ylabel('Average Purchase Value')
                st.pyplot(fig)
                
                st.write("""
                    **Explanation:**
                    This bar chart displays the average spending of customers in each cluster.
                    - **Clusters:** Different clusters are represented on the x-axis.
                    - **Average Purchase Value:** The height of each bar represents the average amount spent by customers in that cluster.
                    - **Insight:** This visualization helps identify which cluster has the highest average spending. It is useful for targeting high-spending customers or understanding spending behavior across different clusters.
                """)
            except Exception as e:
                st.error(f"Error: {e}")

        elif sub_option == 'Overview':
            st.header('Cluster Overview')
            st.subheader('Cluster Counts and Insights')
            try:
                # Compute cluster counts
                cluster_counts = df['cluster'].value_counts()

                # Display cluster counts
                st.write("**Number of Customers in Each Cluster:**")
                st.write(cluster_counts)

                # Generate a bar plot for cluster counts
                fig, ax = plt.subplots(figsize=(10, 6))
                cluster_counts.plot(kind='bar', ax=ax, color='skyblue')
                ax.set_title('Number of Customers per Cluster')
                ax.set_xlabel('Cluster')
                ax.set_ylabel('Number of Customers')
                st.pyplot(fig)

                # Additional analysis based on cluster counts
                st.write("**Cluster Characteristics and Seller Actions:**")
                for cluster in cluster_counts.index:
                    avg_value = df[df['cluster'] == cluster]['avg_purchase_value'].mean()
                    st.write(f"- **{cluster} Cluster**:")
                    st.write(f"  - **Average Purchase Value**: ${avg_value:.2f}")
                    st.write(f"  - **Recommended Actions:**")
                    if cluster == 'High':
                        st.write("    - Consider offering premium services or exclusive offers to retain these high-value customers.")
                    elif cluster == 'Medium':
                        st.write("    - Target these customers with loyalty programs or personalized marketing to increase their spending.")
                    else:
                        st.write("    - Focus on strategies to boost engagement and conversion rates for these customers. Consider promotions or special discounts.")
            
            except Exception as e:
                st.error(f"Error: {e}")

    elif option == 'Product Interest Clustering':
        st.header('Product Interest Clustering - Main Categories')
        st.subheader('Clustering by Main Product Categories')
        
        try:
            # Check if required columns are in the DataFrame
            required_columns = ['product_category', 'cluster', 'subcategory']
            if not all(col in df.columns for col in required_columns):
                st.error("DataFrame must contain 'product_category', 'cluster', and 'subcategory' columns")
                st.stop()  # Stop further execution
            
            # Explode subcategories if they are lists
            if df['subcategory'].apply(lambda x: isinstance(x, list)).any():
                df_exploded = df.explode('subcategory')
            else:
                df_exploded = df
            
            # Create a search bar for main categories
            category_search = st.text_input('Search for a Main Category', '')
            if category_search:
                filtered_df = df_exploded[df_exploded['product_category'].str.contains(category_search, case=False, na=False)]
            else:
                filtered_df = df_exploded
            
            # Create a bar plot for main category counts
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.countplot(x='product_category', hue='cluster', data=filtered_df, ax=ax)
            ax.set_title('Main Category Clustering')
            ax.set_xlabel('Main Category')
            ax.set_ylabel('Count')
            st.pyplot(fig)
            
            st.write("""
                **Explanation:**
                This bar chart shows the distribution of customers across different main product categories, segmented by clusters.
                - **Clusters:** Different colors represent different clusters.
                - **Insight:** Helps to understand which main categories are most popular within each cluster. This can guide marketing and product placement strategies.
            """)
            
            # Provide an option to drill down into subcategories
            selected_main_category = st.selectbox('Select a Main Category for Subcategory Clustering', filtered_df['product_category'].unique())
            
            if selected_main_category:
                st.subheader(f'Subcategory Clustering for {selected_main_category}')
                subcategory_df = filtered_df[filtered_df['product_category'] == selected_main_category]
                
                # Create a search bar for subcategories
                subcategory_search = st.text_input('Search for a Subcategory', '')
                if subcategory_search:
                    subcategory_df = subcategory_df[subcategory_df['subcategory'].str.contains(subcategory_search, case=False, na=False)]
                
                # Aggregating subcategory data
                subcategory_counts = subcategory_df['subcategory'].value_counts()
                
                # Limit to top 10 subcategories
                top_subcategories = subcategory_counts.head(10)
                
                # Plot top subcategory counts
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.barplot(x=top_subcategories.index, y=top_subcategories.values, ax=ax)
                ax.set_title(f'Top 10 Subcategories for {selected_main_category}')
                ax.set_xlabel('Subcategory')
                ax.set_ylabel('Count')
                st.pyplot(fig)
                
                st.write("""
                    **Explanation:**
                    This bar chart shows the top 10 subcategories within the selected main category.
                    - **Subcategories:** The x-axis represents the top 10 subcategories.
                    - **Count:** The y-axis represents the number of occurrences for each subcategory.
                    - **Insight:** Provides a focused view of the most popular subcategories within the main category.
                """)
                
                st.write("""
                    **Subcategory Analysis:**
                    This section helps in identifying the preferences and trends within a specific main category, which can assist in targeted marketing and product placement strategies.
                """)
            
        except Exception as e:
            st.error(f"Error: {e}")


    elif option == 'RFM Clustering':
        st.header('Recency-Frequency-Monetary (RFM) Clustering')
        st.subheader('3D Scatter Plot')
        try:
            if not all(col in df.columns for col in ['purchase_recency', 'purchase_frequency', 'avg_purchase_value', 'cluster']):
                st.error("DataFrame must contain 'purchase_recency', 'purchase_frequency', 'avg_purchase_value', and 'cluster' columns.")
                st.stop()
            
            fig = plt.figure(figsize=(12, 8))
            ax = fig.add_subplot(111, projection='3d')
            scatter = ax.scatter(
                df['purchase_recency'], 
                df['purchase_frequency'], 
                df['avg_purchase_value'], 
                c=df['cluster'].astype('category').cat.codes, 
                cmap='viridis', 
                s=50
            )
            ax.set_xlabel('Purchase Recency')
            ax.set_ylabel('Purchase Frequency')
            ax.set_zlabel('Average Purchase Value')
            plt.title('RFM Clustering')
            st.pyplot(fig)
            
            cluster_counts = df['cluster'].value_counts()
            st.write(f"**Cluster Distribution:**")
            st.write(cluster_counts)
            
            st.write("""
                **Explanation:**
                This 3D scatter plot visualizes customer segments based on three key metrics:
                - **Purchase Recency:** The time since the last purchase.
                - **Purchase Frequency:** How often a customer makes purchases.
                - **Average Purchase Value:** The average spending per transaction.
                - **Clusters:** Different colors represent different clusters.
                - **Insight:** The plot provides a comprehensive view of customer behavior, helping to identify patterns in recency, frequency, and monetary value.
            """)
            
            st.write("**Seller Actions Based on RFM Clusters:**")
            for cluster in df['cluster'].unique():
                st.write(f"- **{cluster} Cluster:**")
                cluster_data = df[df['cluster'] == cluster]
                avg_recency = cluster_data['purchase_recency'].mean()
                avg_frequency = cluster_data['purchase_frequency'].mean()
                avg_value = cluster_data['avg_purchase_value'].mean()
                st.write(f"  - **Average Recency:** {avg_recency:.2f}")
                st.write(f"  - **Average Frequency:** {avg_frequency:.2f}")
                st.write(f"  - **Average Purchase Value:** {avg_value:.2f}")
                if cluster == 'High':
                    st.write(f"    - **Action:** Focus on retaining these customers with loyalty programs and personalized offers, as they have high engagement and spend more frequently.")
                elif cluster == 'Medium':
                    st.write(f"    - **Action:** Implement targeted marketing strategies to increase their purchase frequency and value, possibly through promotions or reminders.")
                else:
                    st.write(f"    - **Action:** Develop strategies to increase engagement and encourage more frequent purchases, such as special discounts or re-engagement campaigns.")
        
        except Exception as e:
            st.error(f"Error: {e}")

    elif option == 'Discount Sensitivity Clustering':
        st.header('Discount Sensitivity Clustering')
        st.subheader('Box Plot of Avg Purchase Value by Discount Usage')
        try:
            if not all(col in df.columns for col in ['discount_usage', 'avg_purchase_value']):
                st.error("DataFrame must contain 'discount_usage' and 'avg_purchase_value' columns.")
                st.stop()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(x='discount_usage', y='avg_purchase_value', data=df, ax=ax, palette='Set2')
            ax.set_title('Discount Sensitivity Clustering')
            ax.set_xlabel('Discount Usage')
            ax.set_ylabel('Average Purchase Value')
            st.pyplot(fig)
            
            discount_summary = df.groupby('discount_usage')['avg_purchase_value'].describe()
            st.write(f"**Discount Usage Summary:**")
            st.write(discount_summary)
            
            st.write("""
                **Explanation:**
                This box plot displays how the Average Purchase Value varies with Discount Usage categories:
                - **X-Axis:** Discount Usage categories (e.g., High, Medium, Low).
                - **Y-Axis:** Average Purchase Value.
                - **Insight:** Helps in identifying the effect of discounts on spending patterns and whether certain segments are more responsive to discounts.
            """)
            
            st.write("**Seller Actions Based on Discount Sensitivity:**")
            for discount_category in df['discount_usage'].unique():
                st.write(f"- **{discount_category} Discount Users:**")
                category_data = df[df['discount_usage'] == discount_category]
                avg_value = category_data['avg_purchase_value'].mean()
                st.write(f"  - **Average Purchase Value:** {avg_value:.2f}")
                if discount_category == 'High':
                    st.write(f"    - **Action:** These customers respond well to discounts. Consider using aggressive discount strategies to drive more sales and increase customer loyalty.")
                elif discount_category == 'Medium':
                    st.write(f"    - **Action:** Moderate discount strategies might be effective. Target these customers with occasional promotions to boost engagement and spending.")
                else:
                    st.write(f"    - **Action:** These customers are less influenced by discounts. Focus on improving product value and quality, and consider other incentives or marketing strategies to increase engagement.")
        
        except Exception as e:
            st.error(f"Error: {e}")

    elif option == 'Geo-Location-Based Clustering':
        st.header('Geo-Location-Based Clustering')
        st.subheader('General Insights by Geographic Locations')
        
        try:
            # Check if required columns are in the DataFrame
            required_columns = ['geo_location', 'cluster', 'customer_id', 'avg_purchase_value', 'purchase_frequency']
            if not all(col in df.columns for col in required_columns):
                st.error("DataFrame must contain 'geo_location', 'cluster', 'customer_id', 'avg_purchase_value', and 'purchase_frequency' columns")
                st.stop()  # Stop further execution
            
            # Create a bar plot for geographic location counts
            try:
                fig, ax = plt.subplots(figsize=(12, 6))
                geo_location_counts = df['geo_location'].value_counts()
                sns.barplot(x=geo_location_counts.index, y=geo_location_counts.values, ax=ax)
                ax.set_title('Customer Distribution by Geographic Location')
                ax.set_xlabel('Geographic Location')
                ax.set_ylabel('Count')
                plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Plotting error: {e}")
            
            st.write("""
                **General Insights:**
                This chart displays the distribution of customers across different geographic locations.
                - **Insight:** Helps to understand which geographic regions have the highest customer concentrations.
            """)
            
            # Provide an option to select a region for detailed insights
            selected_region = st.selectbox('Select a Geographic Location for Detailed Insights', df['geo_location'].unique())
            
            if selected_region:
                st.subheader(f'Detailed Insights for {selected_region}')
                region_df = df.query('geo_location == @selected_region')
                
                # Create a bar plot for cluster counts within the selected region
                try:
                    fig, ax = plt.subplots(figsize=(12, 6))
                    cluster_counts = region_df['cluster'].value_counts()
                    sns.barplot(x=cluster_counts.index, y=cluster_counts.values, ax=ax)
                    ax.set_title(f'Customer Distribution by Cluster in {selected_region}')
                    ax.set_xlabel('Cluster')
                    ax.set_ylabel('Count')
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Plotting error: {e}")
                
                st.write("""
                    **Detailed Insights:**
                    This chart displays the distribution of customers across different clusters within the selected geographic location.
                    - **Clusters:** Different colors represent different clusters.
                    - **Insight:** Helps to understand which clusters are predominant within the selected region.
                """)
                
                # Detailed insights for each cluster in the selected region
                clusters = region_df['cluster'].unique()
                for cluster in clusters:
                    st.subheader(f'Detailed Insights for Cluster {cluster} in {selected_region}')
                    cluster_df = region_df.query('cluster == @cluster')
                    
                    # Aggregating data for the selected cluster
                    total_customers = cluster_df['customer_id'].nunique()
                    avg_purchase_value = cluster_df['avg_purchase_value'].mean()
                    avg_purchase_frequency = cluster_df['purchase_frequency'].mean()
                    
                    st.write(f"- **Total Customers in Cluster {cluster}:** {total_customers}")
                    st.write(f"- **Average Purchase Value in Cluster {cluster}:** ${avg_purchase_value:.2f}")
                    st.write(f"- **Average Purchase Frequency in Cluster {cluster}:** {avg_purchase_frequency:.2f}")
                    
                    # Create a bar plot for purchase value and frequency
                    try:
                        fig, ax = plt.subplots(figsize=(12, 6))
                        sns.barplot(x=['Avg Purchase Value', 'Avg Purchase Frequency'], 
                                    y=[avg_purchase_value, avg_purchase_frequency], 
                                    ax=ax, palette='viridis')
                        ax.set_title(f'Cluster {cluster} Metrics in {selected_region}')
                        ax.set_ylabel('Value')
                        st.pyplot(fig)
                    except Exception as e:
                        st.error(f"Plotting error: {e}")
                    
                    # Additional recommendations
                    st.write("""
                        **Recommendations:**
                        Based on the selected cluster:
                        - **Regional Marketing:** Tailor marketing campaigns to target customers in the most lucrative regions and clusters.
                        - **Localized Promotions:** Offer region-specific promotions or discounts based on purchasing behavior and frequency.
                        - **Inventory Management:** Adjust inventory and supply chain logistics based on regional demand patterns.
                        - **Customer Engagement:** Develop region-specific engagement strategies to enhance customer satisfaction and loyalty.
                    """)

        except Exception as e:
            st.error(f"Error: {e}")

    elif option == 'Purchase Frequency-Based Clustering':
        st.header('Purchase Frequency-Based Clustering')
        st.subheader('Histogram of Purchase Frequency')
        
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.histplot(df, x='purchase_frequency', hue='cluster', multiple='stack', palette='tab10', ax=ax)
            ax.set_title('Purchase Frequency-Based Clustering')
            ax.set_xlabel('Purchase Frequency')
            ax.set_ylabel('Count')
            st.pyplot(fig)
            
            frequency_summary = df.groupby('cluster')['purchase_frequency'].describe()
            st.write("**Purchase Frequency Summary by Cluster:**")
            st.write(frequency_summary)
            
            st.write("""
                **Explanation:**
                This histogram shows the distribution of Purchase Frequency across different clusters.
                - **X-Axis:** Purchase Frequency.
                - **Y-Axis:** Count of customers.
                - **Clusters:** Different colors represent different clusters.
                - **Insight:** Helps in understanding the frequency of customer purchases and the distribution of customers within each cluster.
            """)
        except Exception as e:
            st.error(f"Error: {e}")

    elif option == 'Behavioral Clustering':
        st.header('Behavioral Clustering')
        st.subheader('Pair Plot of Purchase Frequency and Recency')
        
        try:
            # Only use numerical data for pairplot
            fig = sns.pairplot(df[['purchase_frequency', 'purchase_recency', 'cluster']], hue='cluster')
            plt.suptitle('Behavioral Clustering', y=1.02)
            st.pyplot(fig)
            
            behavior_summary = df.groupby('cluster').agg({
                'purchase_frequency': ['mean', 'std'],
                'purchase_recency': ['mean', 'std']
            })
            st.write("**Behavioral Summary by Cluster:**")
            st.write(behavior_summary)
            
            st.write("""
                **Explanation:**
                This pair plot visualizes the relationship between Purchase Frequency and Purchase Recency across different clusters.
                - **Diagonal Plots:** Show the distribution of individual features.
                - **Off-Diagonal Plots:** Show relationships between pairs of features.
                - **Clusters:** Different colors represent clusters.
                - **Insight:** Useful for exploring how purchase behavior is related between different clusters.
            """)
        except Exception as e:
            st.error(f"Error: {e}")

    elif option == 'Combination Clustering':
        st.header('Combination Clustering')
        st.subheader('Heatmap of Avg Purchase Value by Product Category and Geo-Location')
        
        try:
            heatmap_data = df.pivot_table(index='geo_location', columns='product_category', values='avg_purchase_value', aggfunc='mean')
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, ax=ax)
            ax.set_title('Combination Clustering Heatmap')
            st.pyplot(fig)
            
            avg_purchase_by_category = df.groupby('product_category')['avg_purchase_value'].mean()
            st.write("**Average Purchase Value by Product Category:**")
            st.write(avg_purchase_by_category)
            
            st.write("""
                **Explanation:**
                This heatmap displays the average purchase value across different product categories and geographical locations.
                - **X-Axis:** Product Categories.
                - **Y-Axis:** Geo Locations.
                - **Colors:** Represent average purchase values.
                - **Insight:** Helps in understanding the relationship between product categories and regions, and how this information can be used to improve marketing strategies.
            """)
        except Exception as e:
            st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.markdown("© 2024 bhAIya Seller Dashboard. All rights reserved.")




#api for segmentation data
# from flask import Flask, jsonify
# import pymongo

# app = Flask(__name__)

# # MongoDB connection
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client['segmenttrial']
# collection = db['segt']

# # Define a route for the API
# @app.route('/get_data', methods=['GET'])
# def get_data():
#     # Fetch data from MongoDB
#     data = list(collection.find({}, {'_id': 0}))  # Exclude the MongoDB ObjectID from the response
#     return jsonify(data)

# if __name__ == '__main__':
#     app.run(debug=True)
