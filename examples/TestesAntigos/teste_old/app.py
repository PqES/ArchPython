import os
from flask import Flask
from userRoute import app_user
from carroRoute import app_route
from animalRoute import app_animal


views_folder = os.path.abspath('.')

app = Flask(__name__, template_folder=views_folder)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI', 'sqlite:///db.sqlite3')

if __name__ == "__main__":
    port = os.getenv('PORT', 8001)


    app.register_blueprint(app_user)
    app.register_blueprint(app_route)
    app.register_blueprint(app_animal)


    app.run(host='0.0.0.0', port=port, debug=True)
