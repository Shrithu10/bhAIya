# bhAIya

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

## How We Built It

**bhAIya** is written in Python and powered by the mistral:latest, along with assistance from the Llava-phi Vision model. bhAIya takes the shopkeeper's database as input and adapts to the products listed in the shop. It creates a specialized database for each store using insights from the large language model and uses it to fulfill users' queries. It uses **Few Shot learning** to identify categories from the user's prompt and match it with the already generated categories in the database. These categories on both sides are converted into vector embeddings using Word2Vec and are matched together using Cosine similarity. The top n results are returned back.
 
## Working pictures 
![image](https://github.com/user-attachments/assets/6c1e0b4a-4937-4ef7-800e-e9235317d7a5)

![image](https://github.com/user-attachments/assets/c2196119-a320-46c8-b24a-9fb4b65035ae)
## bhAIya seller dashboard:
![image](https://github.com/user-attachments/assets/37d818cf-a195-4661-a290-31cf8261ca0b)





