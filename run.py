from config import config

from app import create_app

app = create_app(config)

if __name__ == "__main__":
    app.run(port=5000)