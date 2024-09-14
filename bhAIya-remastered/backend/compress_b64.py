import json
import base64
import io
from PIL import Image
import os
import sys

def analyze_json_structure(data, prefix=''):
    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            if key == 'image' and isinstance(value, str):
                print(f"Found potential image at: {new_prefix}")
                print(f"String length: {len(value)}")
                print(f"First 20 characters: {value[:20]}")
                print("--------------------")
            else:
                analyze_json_structure(value, new_prefix)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            analyze_json_structure(item, f"{prefix}[{i}]")

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

def process_json(input_file, output_file):
    # Read the input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    print("Analyzing JSON structure...")
    analyze_json_structure(data)

    print("\nProcessing images...")
    total_images = 0
    compressed_images = 0
    total_original_size = 0
    total_compressed_size = 0

    def process_item(item):
        nonlocal total_images, compressed_images, total_original_size, total_compressed_size
        if isinstance(item, dict):
            for key, value in item.items():
                if key == 'image' and isinstance(value, str):
                    total_images += 1
                    print(f"Processing image for key: {key}")
                    original_size = len(value)
                    total_original_size += original_size
                    
                    # Compress the image
                    compressed_base64, format_used = compress_image(value)
                    
                    if compressed_base64 is not None:
                        compressed_size = len(compressed_base64)
                        total_compressed_size += compressed_size
                        if compressed_size < original_size:
                            # Update the JSON with the compressed image
                            item[key] = compressed_base64
                            compressed_images += 1
                        else:
                            print(f"Compression did not reduce size for this image")
                    else:
                        print(f"Skipped compression for this image")
                    
                    print("--------------------")
                elif isinstance(value, (dict, list)):
                    process_item(value)
        elif isinstance(item, list):
            for sub_item in item:
                process_item(sub_item)

    process_item(data)

    # Write the updated data to the output JSON file
    with open(output_file, 'w') as f:
        json.dump(data, f)

    print(f"Total images processed: {total_images}")
    print(f"Images successfully compressed: {compressed_images}")
    print(f"Total original size: {total_original_size} bytes")
    print(f"Total compressed size: {total_compressed_size} bytes")
    if total_original_size > 0:
        overall_compression = (total_original_size - total_compressed_size) / total_original_size * 100
        print(f"Overall compression: {overall_compression:.2f}%")

    return data

# Usage
input_file = 'imageClothesResult.json'
output_file = 'compressed_imageClothesResult.json'

# Process the JSON and get the processed data
processed_data = process_json(input_file, output_file)

# Verify that the files were accessed and modified
if os.path.exists(output_file):
    print(f"Compressed images saved to {output_file}")

    # Print overall file size reduction
    original_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(output_file)
    overall_reduction = (original_size - compressed_size) / original_size * 100
    print(f"Overall file size reduction: {overall_reduction:.2f}%")

    # Additional verification
    print(f"Number of items in processed data: {len(processed_data)}")
else:
    print("Error: Output file was not created. Check file permissions and paths.")