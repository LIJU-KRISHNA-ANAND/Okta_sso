import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

OKTA_ISSUER = os.getenv("OKTA_ISSUER")
OKTA_CLIENT_ID = os.getenv("OKTA_CLIENT_ID")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    okta_id = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)

@app.route('/')
def home():
    return 'Okta Authentication with Flask Backend'

@app.route('/verify', methods=['POST'])
def verify_user():
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({"error": "Token is missing"}), 400
    
    token = token.split('Bearer ')[-1]
    is_valid, user_info = verify_okta_token(token)
    
    if is_valid:
        existing_user = User.query.filter_by(okta_id=user_info['sub']).first()
        
        if not existing_user:
            new_user = User(
                okta_id=user_info['sub'],
                email=user_info['sub']
            )
            db.session.add(new_user)
            db.session.commit()
        
        return jsonify({"message": "User verified and stored successfully", "user": user_info}), 200
    
    return jsonify({"error": "Invalid token"}), 401


def verify_okta_token(token):
    try:
        
        url = f"{OKTA_ISSUER}/v1/introspect"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'token': f"{token}",
            'client_id': f"{OKTA_CLIENT_ID}"
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            token_data = response.json()
            
            if token_data.get("active"):
                return True, {
                    "active": token_data["active"],   
                    "sub": token_data["sub"],
                    "name": token_data["username"],
                    "exp": token_data["exp"]
                }
        return False, None
    except Exception as e:
        print(f"Error validating token: {e}")
        return False, None

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

