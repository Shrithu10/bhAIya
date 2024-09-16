# bhAIya - The Multi Modal Search Engine

## Inspiration

In the bustling streets of India, shopkeepers, affectionately called "Bhaiya," play a crucial role. They help customers find the products they need at the best prices. However, many shopkeepers struggle to meet customer needs due to the vast range of products they handle. Observing this challenge, we thought: what if technology could help? What if we could create an application that acts like a knowledgeable Bhaiya, bridging the gap between customers and products?

## What It Does

**bhAIya** is a unique AI-powered application designed to bridge the gap between consumers and the companies that make their products. Here's how it works:

### Key Features of bhAIya

1. **Product Recommendations**:
   - **AI-Powered Suggestions**: bhAIya uses advanced AI technology to provide personalized product recommendations based on customer needs and preferences.
   - **Smart Search**: Users can search for products by description or image, ensuring they find exactly what they’re looking for.

2. **Image Recognition**:
   - **Snap and Learn**: Customers can take a picture of any product in a store and instantly receive detailed information, including product specs, price details, and past recommendations.

3. **User-Friendly Interface**:
   - **Easy Navigation**: The app is designed to be intuitive and easy to use, making it accessible to a wide range of users, from tech-savvy individuals to those less familiar with technology.

4. **Enhanced Shopping Experience**:
   - **Informed Decisions**: By providing comprehensive product details, bhAIya helps users make well-informed purchasing decisions.

5. **Products Bundle Generation**:
   - **Curated Bundles**: bhAIya suggests product bundles based on user preferences, grouping complementary items for convenience.
   - **Cost-Efficiency**: Bundling helps users save by offering related products at competitive prices.

6. **Personalized Product Generation Based on Prompts**:
   - **Custom Product Suggestions**: Users provide prompts, and bhAIya generates personalized product recommendations.
   - **Interactive Shopping Assistant**: The AI adapts to user inputs, delivering tailored results in real-time.

7. **Multilingual Approach**:
   - **Support for Multiple Languages**: bhAIya can communicate with users in different languages, ensuring accessibility for diverse audiences.
   - **Seamless Translations**: Users can interact in their preferred language, and bhAIya will provide answers and recommendations accordingly.

## bhAIya seller dashboard:
The seller dashboard of bhAIya helps the seller in a lot of methods to cluster the segments of cutomers based on different paramters,helping them in different business development methods.The seller can also use this to keep a track of the products in the website and can add,modify or delete products as well.

**Geo-Location-Based Clustering:** Segment customers based on their location.
**Purchase Frequency-Based Clustering:** Group customers by how often they make purchases.
**Behavioral Clustering:** Understand and cluster customers based on their behavior patterns.
**Discount Sensitivity Clustering:** Identify customers who respond to discounts.
**Recency-Frequency-Monetary (RFM) Clustering:** Segment customers by recent activity, purchase frequency, and monetary value.
**Product Interest Clustering:** Classify customers by their interests in specific products.
**Value-Based Clustering:** Segment customers by the value they bring to the business. 

## How We Built It

**bhAIya** is written in Python and powered by the mistral:latest, along with assistance from the Llava-phi Vision model. bhAIya takes the shopkeeper's database as input and adapts to the products listed in the shop. It creates a specialized database for each store using insights from the large language model and uses it to fulfill users' queries. It uses **Few Shot learning** to identify categories from the user's prompt and match it with the already generated categories in the database. These categories on both sides are converted into vector embeddings using Word2Vec and are matched together using Cosine similarity. The top n results are returned back.
 
## Working pictures 
![image](https://github.com/user-attachments/assets/6c1e0b4a-4937-4ef7-800e-e9235317d7a5)

![image](https://github.com/user-attachments/assets/c2196119-a320-46c8-b24a-9fb4b65035ae)

## Custom product generation
![image](https://github.com/user-attachments/assets/b66832c8-a134-4dda-ac66-a0e831b1e438)


## bhAIya seller dashboard
![image](https://github.com/user-attachments/assets/37d818cf-a195-4661-a290-31cf8261ca0b)

## Demo videos:
https://github.com/user-attachments/assets/aab28e87-03be-41e4-832c-71933e0cefc4

## Custom products bundle recommendation system:
https://github.com/user-attachments/assets/4cf604b4-e7b5-4bac-b3a1-034914f95930

## Seller dashboard demo: 
https://github.com/user-attachments/assets/438693b6-a81c-4b3c-a462-933e56ab8b5f

## Full video: 
https://github.com/user-attachments/assets/fb3586df-6ab1-45a1-a9ee-d2b1635f0729










