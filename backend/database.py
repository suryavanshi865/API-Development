import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="recipes_user",
        password="Password@123",
        database="recipe",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

