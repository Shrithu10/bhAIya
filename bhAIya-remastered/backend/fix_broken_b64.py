import pymongo
from tqdm import tqdm

def fix_base64_string(base64_string):
    # Check if the string starts with "b'" and ends with "'"
    if base64_string.startswith("b'") and base64_string.endswith("'"):
        # Remove the "b'" prefix and the trailing "'"
        base64_string = base64_string[2:-1]
    return base64_string

def validate_and_fix_images_in_mongo():
    # Set up MongoDB connection
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["bhAIya"]
    collection = db["merged_images_3.6"]

    # Get the total count of elements for the progress bar
    total_elements = collection.count_documents({})

    # Iterate through all elements in the collection
    for element in tqdm(collection.find(), total=total_elements):
        image_base64 = element.get('image', '')
        element_id = element['id']

        # Check and fix the base64 string if necessary
        fixed_base64 = fix_base64_string(image_base64)

        # Update the MongoDB element if the string was modified
        if fixed_base64 != image_base64:
            collection.update_one({"id": element_id}, {"$set": {"image": fixed_base64}})
            print(f"Fixed base64 string for element ID: {element_id}")

if __name__ == "__main__":
    validate_and_fix_images_in_mongo()
