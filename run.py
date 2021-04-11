import os

from app.config import ROOT_PATH
from app.main import create_app

if not os.path.exists(ROOT_PATH):
    os.makedirs(ROOT_PATH)

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
