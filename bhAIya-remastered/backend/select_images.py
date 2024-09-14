# This code is to create a sub directory of the images for products that have been selected



import os
import shutil
import pandas as pd

DATASET_PATH = r"C:\Users\nikhi\Downloads\bhAIya dataset\with_price\with_price.csv"
columnsToAccept = [
        "id",
        "gender",
        "masterCategory",
        "subCategory",
        "articleType",
        "baseColour",
        "season",
        "year",
        "usage",
        "productDisplayName",
        "price"
    ]
idColumn = "id"
priceColumn="price"
top_n_rows=500
data = pd.read_csv(DATASET_PATH, on_bad_lines="skip")
data=data.head(top_n_rows)

# Define paths
IMAGES_PATH = r"C:\Users\nikhi\Downloads\bhAIya dataset\images\images"
NEW_IMAGES_FOLDER = r"C:\Users\nikhi\Downloads\bhAIya dataset\selected_images"

# Create new folder if it doesn't exist
os.makedirs(NEW_IMAGES_FOLDER, exist_ok=True)

# Get list of IDs from the dataframe
id_list = data['id'].tolist()

# Copy matching images to the new folder
for image_file in os.listdir(IMAGES_PATH):
    file_name, file_extension = os.path.splitext(image_file)
    if int(file_name) in id_list:
        src_path = os.path.join(IMAGES_PATH, image_file)
        dst_path = os.path.join(NEW_IMAGES_FOLDER, image_file)
        shutil.copy2(src_path, dst_path)

# Save the path of the new folder in a variable
SELECTED_IMAGES_PATH = NEW_IMAGES_FOLDER

print(f"Selected images have been copied to: {SELECTED_IMAGES_PATH}")
print(f"Number of images copied: {len(os.listdir(SELECTED_IMAGES_PATH))}")