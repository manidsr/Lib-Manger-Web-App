from flask import Blueprint, request, jsonify
from utils.db import execute_query

books_bp = Blueprint('books', __name__)

@books_bp.route('/books', methods=['GET'])
def get_books():
    books = execute_query("SELECT * FROM books")
    return jsonify(books)

@books_bp.route('/books', methods=['POST'])
def add_book():
    data = request.json
    execute_query(
        "INSERT INTO books (title, author, published_year) VALUES (%s, %s, %s)",
        (data['title'], data['author'], data.get('published_year'))
    )
    return jsonify({"message": "Book added successfully"}), 201

@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    execute_query("DELETE FROM books WHERE id = %s", (book_id,))
    return jsonify({"message": "Book deleted successfully"})