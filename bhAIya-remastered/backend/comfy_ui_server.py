from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
import json
from urllib import request as ub_request
import random
import time
import os
import base64
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

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

def queue_prompt(prompt, steps=1):
    workflow = {
        "5": {
            "inputs": {
                "width": 512,
                "height": 512,
                "batch_size": 1
            },
            "class_type": "EmptyLatentImage",
            "_meta": {
                "title": "Empty Latent Image"
            }
        },
        "6": {
            "inputs": {
                "text": prompt,
                "clip": [
                    "11",
                    0
                ]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {
                "title": "CLIP Text Encode (Prompt)"
            }
        },
        "8": {
            "inputs": {
                "samples": [
                    "30",
                    0
                ],
                "vae": [
                    "10",
                    0
                ]
            },
            "class_type": "VAEDecode",
            "_meta": {
                "title": "VAE Decode"
            }
        },
        "10": {
            "inputs": {
                "vae_name": "flux_vae.safetensors"
            },
            "class_type": "VAELoader",
            "_meta": {
                "title": "Load VAE"
            }
        },
        "11": {
            "inputs": {
                "clip_name1": "clip-vit-large-patch14.safetensors",
                "clip_name2": "t5\\google_t5-v1_1-xxl_encoderonly-fp8_e4m3fn.safetensors",
                "type": "flux"
            },
            "class_type": "DualCLIPLoader",
            "_meta": {
                "title": "DualCLIPLoader"
            }
        },
        "27": {
            "inputs": {
                "unet_name": "flux1-schnell-Q4_K_S.gguf"
            },
            "class_type": "UnetLoaderGGUF",
            "_meta": {
                "title": "Unet Loader (GGUF)"
            }
        },
        "30": {
            "inputs": {
                "seed": 96015080338362,
                "steps": steps,
                "cfg": 1.5,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1,
                "model": [
                    "27",
                    0
                ],
                "positive": [
                    "6",
                    0
                ],
                "negative": [
                    "31",
                    0
                ],
                "latent_image": [
                    "5",
                    0
                ]
            },
            "class_type": "KSampler",
            "_meta": {
                "title": "KSampler"
            }
        },
        "31": {
            "inputs": {
                "text": "",
                "clip": [
                    "11",
                    0
                ]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {
                "title": "CLIP Text Encode (Prompt)"
            }
        },
        "33": {
            "inputs": {
                "output_path": "C:\\Users\\nikhi\\Downloads\\bhAIya-main\\bhAIya-remastered\\backend\\static\\imageGen",
                "filename_prefix": "ComfyUI",
                "filename_delimiter": "_",
                "filename_number_padding": 4,
                "filename_number_start": "false",
                "extension": "png",
                "dpi": 300,
                "quality": 100,
                "optimize_image": "true",
                "lossless_webp": "false",
                "overwrite_mode": "false",
                "show_history": "false",
                "show_history_by_prefix": "true",
                "embed_workflow": "true",
                "show_previews": "true",
                "images": [
                    "8",
                    0
                ]
            },
            "class_type": "Image Save",
            "_meta": {
                "title": "Image Save"
            }
        }
    }
    # Set the text prompt for our positive CLIPTextEncode
    workflow["6"]["inputs"]["text"] = prompt
    workflow["30"]["inputs"]["seed"] = random.randint(1, 1000000000000)

    p = {"prompt": workflow}
    data = json.dumps(p).encode('utf-8')
    
    try:
        req = ub_request.Request("http://127.0.0.1:8188/prompt", data=data, method="POST")
        req.add_header('Content-Type', 'application/json')
        
        with ub_request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            print(f"Server response: {response_data}")
            
            response_json = json.loads(response_data)
            prompt_id = response_json.get('prompt_id')
            
            if prompt_id:
                print(f"Prompt ID: {prompt_id}")

                while True:
                    status_req = ub_request.Request(f"http://127.0.0.1:8188/history/{prompt_id}")
                    with ub_request.urlopen(status_req) as status_response:
                        status_data = json.loads(status_response.read().decode('utf-8'))
                        print(status_data)
                        if status_data != {} and status_data[prompt_id]['status']['completed'] == True:
                            print("Job completed!")
                            break

                    time.sleep(1)  # Wait for 1 second before checking again
                
                # Find the generated image
                output_dir = r"C:\Users\nikhi\Downloads\bhAIya-main\bhAIya-remastered\backend\static\imageGen"
                image_files = [f for f in os.listdir(output_dir) if f.startswith("ComfyUI_")]
                if image_files:
                    latest_image = max(image_files, key=lambda x: os.path.getctime(os.path.join(output_dir, x)))
                    image_path = os.path.join(output_dir, latest_image)
                    
                    # Convert image to base64
                    with Image.open(image_path) as img:
                        buffered = io.BytesIO()
                        img.save(buffered, format="PNG")
                        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    
                    # Delete the image file
                    os.remove(image_path)

                    compressed_base64, format_used = compress_image(img_base64)
                    
                    # Return the result
                    return {prompt: compressed_base64}
                else:
                    print("No image file found.")
                    return None
            else:
                print("No prompt ID received. The job may not have been queued properly.")
                return None
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/custom_image_gen', methods=['POST'])
def custom_image_gen():
    query = request.form.get("description")
    print(query)
    
    data = queue_prompt(query + "Product, cinematic lighting, hyper realistic, 4k, pedestal, highlight", steps=10)
    print(data)
    
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Or specify your frontend origin
    return response

if __name__ == '__main__':
    app.run(port=8189)