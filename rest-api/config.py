import os

CONFIG = {
    "DEBUG": os.environ.get('DEBUG', 'True'),
    "MONGO_URI": os.environ.get('MONGO_URI', 'mongodb://root:hoodyhu2@ds127624.mlab.com:27624/thymesis'),
    "USERNAME": os.environ.get('USERNAME', 'root'),
    "PASSWORD": os.environ.get('PASSWORD', 'hoodyhu2'),
}