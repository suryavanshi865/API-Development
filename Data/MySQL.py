import os
import json
import pymysql
from dotenv import load_dotenv

load_dotenv(r"D:\recipe-assessment\Parsing_Storing-Data\ENV\.env", override=True)

conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    charset="utf8mb4",
    autocommit=False   
)

cursor = conn.cursor()

with open("parsed_Data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

insert_query = """
INSERT INTO recipes
(cuisine, title, rating, ingredients, instructions,
 prep_time, cook_time, total_time, serves)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


try:
    for recipe in data:
        if not isinstance(recipe, dict):
            continue

        cursor.execute(insert_query, (
            recipe.get("cuisine"),
            recipe.get("title"),
            recipe.get("rating"), 
            recipe.get("ingredients"),
            recipe.get("instructions"),
            recipe.get("prep_time"),
            recipe.get("cook_time"),
            recipe.get("total_time"),
            recipe.get("serves")
        ))


    conn.commit()

except Exception as e:
    conn.rollback()

finally:
    cursor.close()
    conn.close()
    
