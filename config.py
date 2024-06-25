from dotenv import dotenv_values


env = dotenv_values(".flaskenv")

print(env)

class Config:
    SECRET_KEY='secret_key123'


class DevelopmentConfig(Config):
    DEBUG = True    
    FLASKCONFIG="DEV"
    SQLALCHEMY_DATABASE_URI=f"postgresql://postgres:{env['DBPASSWORD']}@{env['DBHOST']}/{env['DBNAME']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER=env['UPLOADS_FOLDER']


class TestConfig(Config):
    DEBUG = False  
    FLASKCONFIG="TEST"  
    SQLALCHEMY_DATABASE_URI=f"postgresql://postgres:{env['DBPASSWORD']}@{env['DBHOST']}/{env['DBNAME']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADS_FOLDER=env['UPLOADS_FOLDER']


config_dict = {
    "development" : DevelopmentConfig,
    "test" : TestConfig
}

config = config_dict[env["CONFIG"]]