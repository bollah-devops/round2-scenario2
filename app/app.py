from flask import Flask, jsonify, request

app = Flask(__name__)

posts = [
    {
        "id":1,
        "title": "My First Blog Post",
        "content": "Welcome to my Blog"
    },
    {
        "id":2,
        "title": "Learning Flask",
        "content": "Flask is a lightweight Python web framework."
    }
]

comments = []

# GET /
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Flask Blog API!"
    })


# GET /posts
@app.route("/posts", methods=["GET"])
def get_posts():
    return jsonify({"count": len(posts), "posts": posts})

# GET /posts/<id>
@app.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)

    if post:
        return jsonify(post)

    return jsonify({
        "error": "Post not found"
    }), 404

# POST /comments
@app.route("/comments", methods=["POST"])
def add_comment():
    data = request.get_json()
    
    if not data:
        return jsonify({
            "error": "Request body must be JSON"
        }), 400
        
    post_id = data.get("post_id")    
    comment_text = data.get("comment")
    
    # Verify post exists
    post = next((p for p in posts if p["id"] == post_id), None)

    if not post:
        return jsonify({
            "error": "Post not found"
        }), 404

    comment = {
        "id": len(comments) + 1,
        "post_id": post_id,
        "comment": comment_text
    }

    comments.append(comment)

    return jsonify({
        "message": "Comment added successfully",
        "comment": comment
    }), 201

    # GET /health
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)