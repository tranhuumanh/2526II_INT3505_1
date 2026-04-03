from flask import Flask
from controllers.user_controller import user_bp
from controllers.book_controller import book_bp
from controllers.loan_controller import loan_bp

app = Flask(__name__)

app.register_blueprint(user_bp)
app.register_blueprint(book_bp)
app.register_blueprint(loan_bp)

if __name__ == "__main__":
    port = 5000
    print(f"Server running at http://localhost:{port}")
    app.run(port=port)
