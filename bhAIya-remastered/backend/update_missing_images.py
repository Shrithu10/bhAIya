import os
import base64
import pymongo
from PIL import Image
import io
from tqdm import tqdm

def is_valid_base64(s):
    try:
        return base64.b64encode(base64.b64decode(s)) == s.encode()
    except Exception:
        return False


def compress_image(base64_string, max_size=(250, 250), quality=85):
    if not is_valid_base64(base64_string):
        print("Invalid base64 string. Skipping this image.")
        return None, None

    try:
        img_data = base64.b64decode(base64_string)
    except:
        print("Error decoding base64 string. Skipping this image.")
        return None, None

    original_size = len(img_data)
    
    try:
        img = Image.open(io.BytesIO(img_data))
    except:
        print("Error opening image. Skipping this image.")
        return None, None

    print(f"Original image size: {img.size}")
    print(f"Original image mode: {img.mode}")

    # Convert to RGB if it's not
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Resize the image while maintaining aspect ratio
    img.thumbnail(max_size)
    print(f"Resized image size: {img.size}")

    # Strip metadata
    data = list(img.getdata())
    img_without_exif = Image.new(img.mode, img.size)
    img_without_exif.putdata(data)

    # Try WebP first, fall back to JPEG if WebP is not available
    buffer = io.BytesIO()
    try:
        img_without_exif.save(buffer, format="WebP", quality=quality)
        format_used = "WebP"
    except Exception:
        img_without_exif.save(buffer, format="JPEG", quality=quality, optimize=True)
        format_used = "JPEG"

    # Encode the compressed image to base64
    compressed_data = buffer.getvalue()
    compressed_size = len(compressed_data)
    compressed_base64 = base64.b64encode(compressed_data).decode('utf-8')

    compression_ratio = (original_size - compressed_size) / original_size * 100

    print(f"Original size: {original_size} bytes")
    print(f"Compressed size: {compressed_size} bytes")
    print(f"Compression ratio: {compression_ratio:.2f}%")
    print(f"Format used: {format_used}")

    return compressed_base64, format_used

def update_images_in_mongo():
    # Set up MongoDB connection
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["bhAIya"]
    collection = db["merged_images_3.6"]

    # Path to the images folder
    images_folder = r"C:\Users\nikhi\Downloads\bhAIya dataset\clothes dataset\data\images"

    # Retrieve all elements with an empty 'images' field
    elements = collection.find({"image": ""})
    elements = list(elements)
    print(elements)

    pbar = tqdm(len(elements), desc="Updating images in MongoDB")
    for element in elements:
        image_id = element['id']
        image_path = os.path.join(images_folder, f"{image_id}.jpg")  # Assuming image format is .jpg

        if os.path.exists(image_path):
            # Read the image and convert it to base64
            with open(image_path, "rb") as image_file:
                base64_string = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Compress the image
            compressed_base64, format_used = compress_image(base64_string)

            # Update the MongoDB element with the compressed base64 string
            collection.update_one({"id": image_id}, {"$set": {"image": compressed_base64}})
        pbar.update(1)

if __name__ == "__main__":
    update_images_in_mongo()
