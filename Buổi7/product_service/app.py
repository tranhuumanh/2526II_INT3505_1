import connexion
from flask_pymongo import PyMongo

# Khởi tạo Connexion App
# specification_dir trỏ vào thư mục chứa file yaml
connexion_app = connexion.FlaskApp(__name__, specification_dir='swagger/')

# Cấu hình MongoDB
app = connexion_app.app
app.config["MONGO_URI"] = "mongodb://localhost:27017/product_db"
mongo = PyMongo(app)

# Nạp file thiết kế
connexion_app.add_api('openapi.yaml')

if __name__ == '__main__':
    print("Swagger UI: http://localhost:8080/ui")
    connexion_app.run(port=8080)