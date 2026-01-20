# Q4-- API INTEGRATION---
# TASK 3.1: 
# # a) Fetch Product Details
import requests
import csv

def fetch_all_products(limit= 100):
    url= "https://dummyjson.com/products"

    try:
        response= requests.get(url)
        response.raise_for_status()  # raises exception for HTTP errors
        data= response.json()
        api_products= data.get("products", [])
        print(f"Successfully Fetched {len(api_products)} products.")
        return api_products
    except requests.RequestException as e:
        print(f"Error fetching products: {e}")
        return []
    

# b) Create Product mapping---
def create_product_mapping(api_products):
    product_mapping = {}
    for product in api_products:
        try:
            product_id= product.get("id")
            title= product.get("title", "").strip()
            category= product.get("category", "").strip()
            brand= product.get("brand", "").strip()
            rating= product.get("rating", 0.0)
        except AttributeError:
            continue
        if product_id is None or title is None:
            continue
    
        product_mapping[product_id]= {
        "title": title,
        "category": category,
        "brand": brand,
        "rating": rating
        }
    return product_mapping

# TASK 3.2 - Enrich Sales Data-----enriches transaction data with product details from API

import os
import re
def enrich_sales_data(transactions, product_mapping):
    
    enriched_data= []
    # output file path---
    output_dir= "data"
    output_file= os.path.join(output_dir, "enriched_sales_data.txt")
    os.makedirs(output_dir, exist_ok= True)

    # columns for output file-- pipe delimited--
    base_cols= [
        "TransactionID", "Date", "ProductID", "ProductName", "Quantity", "UnitPrice", "CustomerID", "Region"
    ]
    new_cols= ["API_category", "API_brand", "API_rating", "API_match"]
    header_cols= base_cols + new_cols
    
    def extract_numeric_id(product_id):    # P101--> 101, P5--> 5
        match= re.search(r'(\d+)', str(product_id))
        return int(match.group(1)) if match else None
    
    for txn in transactions:
        api_category= None
        api_brand= None
        api_rating= None
        api_match= False

        try:
            p_id_str= extract_numeric_id(txn.get("ProductID", ""))
            if p_id_str is not None and p_id_str in product_mapping:
                info= product_mapping[p_id_str]
                api_category= info["category"]
                api_brand= info["brand"]
                api_rating= info["rating"]
                api_match= True
                p_id= int(p_id_str)
        except Exception:
            pass
        enriched_txn= dict(txn)  # copy original transaction
        enriched_txn.update({
            "API_category": api_category,
            "API_brand": api_brand,
            "API_rating": api_rating,
            "API_match": api_match
        })
        enriched_data.append(enriched_txn)

    # write pipe delimited enriched data to output file
    try:
        with open(output_file, mode= "w", encoding= "utf-8", newline= "\n") as file:
            writer= csv.writer(file, delimiter="|")
            writer.writerow(header_cols)  # write header
            for txn in enriched_data:
                row= [
                    txn.get(col, "") for col in base_cols
                ] + [
                    txn.get("API_category", ""),
                    txn.get("API_brand", ""),
                    txn.get("API_rating", ""),
                    str(txn.get("API_match", False))
                ]
                writer.writerow(row)
        print(f"Enriched data written to {output_file}")
    except Exception as e:
        print(f"Error writing enriched data: {e}")
    return enriched_data

# Helper function--
def save_enriched_data(enriched_transactions, filename= "data/enriched_sales_data.txt"):
    try:
        with open(filename, mode= "w", encoding= "utf-8", newline= "\n") as file:
            writer= csv.writer(file, delimiter="|")
            # write header
            header_cols= [
                "TransactionID", "Date", "ProductID", "ProductName", 
                "Quantity", "UnitPrice", "CustomerID", "Region",
                "API_category", "API_brand", "API_rating", "API_match"
            ]
            writer.writerow(header_cols)
            for txn in enriched_transactions:
                row= [
                    txn.get(col, "") for col in header_cols
                ]
                writer.writerow(row)
    except Exception as e:
        print(f"Error saving enriched data: {e}")
        print(f"Enriched data saved to {filename}")

