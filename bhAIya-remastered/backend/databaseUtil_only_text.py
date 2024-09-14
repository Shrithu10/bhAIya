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

    # @suppress_stdout
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
        if os.path.exists(r"C:\Users\nikhi\Downloads\bhAIya-main\bhAIya-remastered\backend\new_datasets_text_only\amazon_text_only_complete_latest_prompt.json"):
            with open(r"C:\Users\nikhi\Downloads\bhAIya-main\bhAIya-remastered\backend\new_datasets_text_only\amazon_text_only_complete_latest_prompt.json", "r") as infile:
                textResult = json.load(infile)
                print("TextResult JSON Found")
        else:
            tdc = TextDatabaseCreator(
                self.data, self.idColumn, self.columnsToAccept, self.priceColumn
            )
            textResult = tdc.create_database()
            with open(r"C:\Users\nikhi\Downloads\bhAIya-main\bhAIya-remastered\backend\new_datasets_text_only\amazon_text_only_complete_latest_prompt.json", "w") as outfile:
                json.dump(textResult, outfile)
                print("Saved textResultClothes.json")




if __name__ == "__main__":
    # This is the Only Clothes Dataset CSV with 2907 Rows
    # DATASET_PATH = r"C:\Users\nikhi\Downloads\bhAIya dataset\clothes dataset\data\fashion.csv"

    # This is the Amazon Dataset CSV with 1939 Rows
    DATASET_PATH = r"C:\Users\nikhi\Downloads\bhAIya dataset\amazon dataset\amazon_description.csv"

    
    # Clothes DataSet Columns
    # columnsToAccept = [
    #     "ProductId",
    #     "Gender",
    #     "Category",
    #     "SubCategory",
    #     "ProductType",
    #     "Colour",
    #     "Usage",
    #     "ProductTitle",
    #     "Price",
    # ]

    # Amazon DataSet Columns
    columnsToAccept=[
        "id",
        "product_description",
        "price"
    ]

    idColumn = "id"
    priceColumn = "price"

    print("Loading and preprocessing data...")
    data = pd.read_csv(DATASET_PATH, on_bad_lines="skip")

    IMAGES_PATH = r"C:\Users\nikhi\Downloads\bhAIya dataset\clothes dataset\data\images"

    dc = DatabaseCreator(data, idColumn, columnsToAccept, priceColumn, IMAGES_PATH)
    dc.create_database()

    print("\nProcessing complete!")