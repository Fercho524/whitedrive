from config import config

from create_app import create_app

app = create_app(config)

if __name__ == "__main__":
    app.run()