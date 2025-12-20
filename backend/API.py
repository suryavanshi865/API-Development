from flask import Flask, jsonify, request, render_template
from database import get_connection
import json

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../Static"
)



@app.route("/api/recipes", methods=["GET"])
def get_recipes():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    offset = (page-1) * limit
    if limit < 10 or limit > 50:
        return jsonify({"error": "Limit must be between 10 and 50"}), 400

    offset = (page - 1) * limit

    conn = get_connection()
    cursor = conn.cursor()

    # total count
    cursor.execute("SELECT COUNT(*) AS total FROM recipes")
    total = cursor.fetchone()["total"]

    query = """
        SELECT *
        FROM recipes
        ORDER BY rating DESC
        LIMIT %s OFFSET %s
    """
    cursor.execute(query, (limit, offset))
    rows = cursor.fetchall()

    # convert nutrients JSON string → object
    for r in rows:
        r["nutrients"] = json.loads(r["nutrients"]) if r["nutrients"] else {}

    cursor.close()
    conn.close()

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "data": rows
    })


@app.route("/api/recipes/search", methods=["GET"])
def search_recipes():
    conditions = []
    values = []

    title = request.args.get("title")
    cuisine = request.args.get("cuisine")
    rating = request.args.get("rating")
    total_time = request.args.get("total_time")
    calories = request.args.get("calories")

    if title:
        conditions.append("title LIKE %s")
        values.append(f"%{title}%")

    if cuisine:
        conditions.append("cuisine LIKE %s")
        values.append(f"%{cuisine}%")

    if rating:
        op, val = rating[:2], rating[2:]
        conditions.append(f"rating {op} %s")
        values.append(val)

    if total_time:
        op, val = total_time[:2], total_time[2:]
        conditions.append(f"total_time {op} %s")
        values.append(val)

    if calories:
        op, val = calories[:2], calories[2:]
        conditions.append(
            "JSON_EXTRACT(nutrients, '$.calories') " + op + " %s"
        )
        values.append(val)

    where_clause = " AND ".join(conditions) if conditions else "1"

    query = f"SELECT * FROM recipes WHERE {where_clause}"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, values)
    rows = cursor.fetchall()

    for r in rows:
        r["nutrients"] = json.loads(r["nutrients"]) if r["nutrients"] else {}

    cursor.close()
    conn.close()

    return jsonify({"data": rows})



@app.route("/")
def home():
    return render_template("Recipe.html")



if __name__ == "__main__":
    app.run(debug=True)
