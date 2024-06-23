from app import create_app, db
from flask_migrate import Migrate
from config import config

app = create_app(config["development"])
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)