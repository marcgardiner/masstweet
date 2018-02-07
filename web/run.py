#run.py

"""initiate flask app instance"""


import os

from app import create_app


CONFIG_NAME = os.getenv('environment')
APP = create_app(CONFIG_NAME)


if __name__ == '__main__':
    APP.run()
