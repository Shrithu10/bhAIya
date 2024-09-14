import os
import sys
import pandas as pd
from utils import getcategoriesFromImage, getCategoriesFromText, encodedimage
import json
from tqdm import tqdm
import io
from contextlib import redirect_stdout
import requests
import numpy as np


def random_price():
    return np.random.randint(2000, 12000)


def suppress_stdout(func):
    def wrapper(*args, **kwargs):
        with io.StringIO() as buf, redirect_stdout(buf):
            result = func(*args, **kwargs)
        return result

    return wrapper


class TextDatabaseCreator:
    def __init__(self, data, idColumn, columnsToAccept, priceColumn):
        self.data = data
        self.columnsToAccept = columnsToAccept
        self.idColumn = idColumn
        self.priceColumn = priceColumn

    @suppress_stdout
    def create_database(self):
        dataWithNeededColumns = self.data[self.columnsToAccept]
        results = {}
        total_rows = len(dataWithNeededColumns)

        pbar = tqdm(
            total=total_rows, desc="Processing text data", position=0, leave=True
        )
        session = requests.Session()
        try:
            for index, row in dataWithNeededColumns.iterrows():
                id = row[self.idColumn]
                description = " ".join(
                    str(row[column]) for column in self.columnsToAccept
                )
                res1 = getCategoriesFromText(
                    "mistral:latest",
                    description,
                    ollama=True,
                    session=session,
                    use_pycurl=True,
                )
                if res1 is None:
                    pbar.update(1)
                    continue
                results[id] = res1["categories"]
                results[id][0]["price"] = row[self.priceColumn]

                # Comment out the below line to remove product title, this is only for the clothes dataset
                # This will not work for any other dataset
                # Rachit this is for you, mereko math bol ki kaam nahi karra

                # results[id][0]['Name'] = self.data['ProductTitle'][index]
                pbar.update(1)
        except Exception as e:
            print(f"An error occured while processing text data: {e}")
        finally:
            session.close()
        pbar.close()

        return results


class ImageDatabaseCreator:
    def __init__(self, imgfoldername):
        self.imgfolderpath = imgfoldername

    @suppress_stdout
    def create_database(self):
        BASE_PATH = f"{self.imgfolderpath}"
        results = {}
        image_files = os.listdir(BASE_PATH)

        pbar = tqdm(
            total=len(image_files[860:]),
            desc="Processing image data",
            position=0,
            leave=True,
        )
        session = requests.Session()
        count = 0
        for filename in image_files[860:]:
            # file_id = int(filename[:filename.index(".")])
            file_id = filename[: filename.index(".")]
            image_path = f"{BASE_PATH}\{filename}"
            try:
                results[file_id] = getcategoriesFromImage(
                    "llava-phi3",
                    image_path,
                    ollama=True,
                    session=session,
                    use_pycurl=True,
                )["categories"]
                results[file_id][0]["image"] = encodedimage(image_path)
            except Exception as e:
                print(f"An error occured while processing image data: {e}")
                continue
            pbar.update(1)
        session.close()
        pbar.close()

        return results


class DatabaseCreator:
    def __init__(self, data, idColumn, columnsToAccept, priceColumn, imgfoldername):
        self.data = data
        self.columnsToAccept = columnsToAccept
        self.idColumn = idColumn
        self.imgfoldername = imgfoldername
        self.priceColumn = priceColumn
        self.finalResults = {}
        self.imageResults = []

    def create_database(self):
        finalResults = []
        imageResults = []

        print("Processing text data...")
        if os.path.exists(f"{os.getcwd()}/textResultClothes.json"):
            with open(f"{os.getcwd()}/textResultClothes.json", "r") as infile:
                textResult = json.load(infile)
                print("TextResult JSON Found")
        else:
            tdc = TextDatabaseCreator(
                self.data, self.idColumn, self.columnsToAccept, self.priceColumn
            )
            textResult = tdc.create_database()
            with open(f"{os.getcwd()}/textResultClothes.json", "w") as outfile:
                json.dump(textResult, outfile)
                print("Saved textResultClothes.json")

        print("\nProcessing image data...")
        if os.path.exists(f"{os.getcwd()}/compressed_imageClothesResult.json"):
            with open(
                f"{os.getcwd()}/compressed_imageClothesResult.json", "r"
            ) as infile:
                imageResult = json.load(infile)
                print("ImageResult JSON Found")
        else:
            print(self.imgfoldername)
            idc = ImageDatabaseCreator(self.imgfoldername)
            imageResult = idc.create_database()
            with open(f"{os.getcwd()}/imageClothesResult.json", "w") as outfile:
                json.dump(imageResult, outfile)
                print("Saved imageAmazonResult.json")

        # MAPPING_PATH=r"C:\Users\nikhi\Downloads\bhAIya dataset\amazon dataset\mapping.csv"

        # mapper = pd.read_csv(MAPPING_PATH)

        # index_map ={}

        # for index, row in mapper.iterrows():
        #     index_map[row['image_id']] = row['path'].split('/')[-1].split('.')[0]

        print("\nMerging text and image results...")
        total_keys = len(textResult.keys())
        pbar = tqdm(total=total_keys, desc="Merging results", position=0, leave=True)
        for key in textResult.keys():
            inter = {}
            inter1 = {}
            for k in ["Main category", "Sub categories", "Additional details"]:
                try:
                    inter[k] = list(
                        set(
                            textResult.get(key, [{k: []}])[0].get(k, [])
                            + imageResult.get(key, [{k: []}])[0].get(k, [])
                        )
                    )
                except Exception as e:
                    print(f"Error processing key {key}: {e}")
                    continue
            inter["id"] = key
            inter["price"] = textResult[key][0]["price"]
            try:
                inter1["image"] = str(imageResult[key][0]["image"])
                # inter1["image"] = str(imageResult[index_map[key]][0]["image"])
                inter1["id"] = key
            except Exception as e:
                print(f"Image not found for key {key}: {e}")
                inter1["image"] = ""
                inter1["id"] = key
            finalResults.append(inter)
            imageResults.append(inter1)
            pbar.update(1)
        pbar.close()

        self.finalResults = finalResults
        self.imageResults = imageResults
        return finalResults

    def createJSONDatabase(self):
        print("\nSaving results to JSON files...")
        with open(f"{os.getcwd()}/database_only_clothes.json", "w") as outfile:
            json.dump(self.finalResults, outfile)
        print("Saved database_clothes.json")

        with open(f"{os.getcwd()}/imageDatabase_only_clothes.json", "w") as outfile:
            json.dump(self.imageResults, outfile)
        print("Saved imageDatabase_clothes.json")


if __name__ == "__main__":
    # DATASET_PATH = r"C:\Users\nikhi\Downloads\bhAIya dataset\with_price\with_price.csv"
    DATASET_PATH = r"C:\Users\nikhi\Downloads\bhAIya-main\bhAIya-remastered\backend\clothes_data.csv"
    # DATASET_PATH=r"C:\Users\nikhi\Downloads\bhAIya dataset\amazon dataset\amazon_description.csv"
    # columnsToAccept = [
    #     "id", "gender", "masterCategory", "subCategory", "articleType",
    #     "baseColour", "season", "year", "usage", "productDisplayName", "price"
    # ]

    columnsToAccept = [
        "ProductId",
        "Gender",
        "Category",
        "SubCategory",
        "ProductType",
        "Colour",
        "Usage",
        "ProductTitle",
        "Price",
    ]

    # columnsToAccept=['id', 'price', 'product_description']

    idColumn = "ProductId"
    priceColumn = "Price"
    # top_n_rows = 500

    print("Loading and preprocessing data...")
    data = pd.read_csv(DATASET_PATH, on_bad_lines="skip")
    # data = data.head(top_n_rows)

    # IMAGES_PATH = r"C:\Users\nikhi\Downloads\bhAIya dataset\selected_images"
    # IMAGES_PATH = r"C:\Users\nikhi\Downloads\bhAIya dataset\amazon dataset\betterImages\betterImages"
    IMAGES_PATH = r"C:\Users\nikhi\Downloads\bhAIya dataset\clothes dataset\data\images"

    dc = DatabaseCreator(data, idColumn, columnsToAccept, priceColumn, IMAGES_PATH)
    dc.create_database()
    dc.createJSONDatabase()

    print("\nProcessing complete!")
