from dotenv import dotenv_values


env = dotenv_values(".flaskenv")


class Config:
    SECRET_KEY='secret_key123'


class DevelopmentConfig(Config):
    DEBUG = True    
    FLASKCONFIG="DEV"
    SQLALCHEMY_DATABASE_URI="postgresql://postgres:524835@localhost/wdrive"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER='/home/fercho/Downloads/uploads'


class TestConfig(Config):
    DEBUG = False  
    FLASKCONFIG="TEST"  
    SQLALCHEMY_DATABASE_URI="postgresql://postgres:524835@localhost/wdrive_test"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADS_FOLDER="/home/fercho/Downloads/uploads"


config_dict = {
    "development" : DevelopmentConfig,
    "test" : TestConfig
}


config = config_dict[env["CONFIG"]]

