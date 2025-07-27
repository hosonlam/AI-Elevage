from flask import Flask
from flask_cors import CORS
from api.routes import user_api

app = Flask(__name__)
app.register_blueprint(user_api)
CORS(app)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
 