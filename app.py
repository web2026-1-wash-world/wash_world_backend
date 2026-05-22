from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import uuid
import time

from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

import x

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from icecream import ic
ic.configureOutput(prefix=f"_____ | ", includeContext=True)

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret-key"

jwt = JWTManager(app)

CORS(app)  # allows everything

##############################
@app.get("/")
def index():
    return jsonify({"status":"ok", "message":"Connected"})

##############################
@app.get("/sign-up")
def show_sign_up():
    return render_template("/page_sign_up.html")

##############################
@app.post("/sign-up")
def sign_up():
    try:
        user_pk = uuid.uuid4().hex
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email( request.form.get("user_email", "" ))
        user_password = x.validate_user_password()
        user_password_hashed = generate_password_hash(user_password)
        user_created_at = int(time.time())
        user_updated_at = int(time.time())
        ic(user_created_at)
        user_verification_key = uuid.uuid4().hex
        user_verified_at = 0
        user_reset_password_key = uuid.uuid4().hex + uuid.uuid4().hex

        db, cursor = x.db()
        q = "INSERT INTO users (user_pk, user_first_name, user_last_name, user_email, user_password_hashed, user_created_at, user_updated_at, user_verification_key, user_verified_at, user_reset_password_key) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(q, (user_pk, user_first_name, user_last_name, user_email, user_password_hashed, user_created_at, user_updated_at, user_verification_key, user_verified_at, user_reset_password_key))
        db.commit()

        activation_email = render_template("email_welcome.html", user_verification_key=user_verification_key)

        x.send_email("Activate your account", activation_email)

        return "We have sent a confirmation email to your account", 201
    except Exception as ex:
        ic(ex)
        if "company_exception user_first_name" in str(ex):
            return f"First name must be between {x.USER_FIRST_NAME_MIN} and {x.USER_FIRST_NAME_MAX} characters", 400
            
        if "company_exception user_last_name" in str(ex):
            return f"Last name must be between {x.USER_LAST_NAME_MIN} and {x.USER_LAST_NAME_MAX} characters", 400

        if "company_exception user_email" in str(ex):
            return "Invalid Email", 400

        if "company_exception user_password" in str(ex):
            return f"At least {x.USER_PASSWORD_MIN} characters", 400

        return str(ex), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.get("/verify/<key>")
def verify_account(key):
    try:
        key = x.validate_uuid4(key)
        db, cursor = x.db()
        user_verified_at = int(time.time())
        q = """
            UPDATE users
            SET user_verified_at = %s
            WHERE user_verification_key = %s AND user_verified_at = 0
        """
        cursor.execute(q, (user_verified_at, key))
        db.commit()
        if cursor.rowcount == 0:
            return "user already verified"

        return f"Welcome to the system, you are verified"
    except Exception as ex: 
        ic(ex)
        if "company_exception uuid4 invalid" in str(ex):
            return "Invalid key", 400

        return str(ex), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/login")
def show_login():
    return render_template("page_login.html")

##############################
@app.post("/login")
def login():
    try:
        user_email = x.validate_user_email( request.form.get("user_email", "") )
        user_password = x.validate_user_password()

        db, cursor = x.db()
        q = """
        SELECT
            user_first_name,
            user_last_name,
            user_email,
            user_password_hashed
        FROM users
        WHERE user_email = %s
        """
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        if not check_password_hash(
            user["user_password_hashed"],
            user_password
        ):
            return jsonify({"error": "Invalid credentials"}), 401
        
        user_first_name = user["user_first_name"]
        user_last_name = user["user_last_name"]
        user_email = user["user_email"]

        access_token = create_access_token(identity={
            "user_email": user_email,
        })

        return jsonify({
            "access_token": access_token,
            "user_first_name": user_first_name,
            "user_last_name": user_last_name,
            "user_email": user_email
        }), 200

    except Exception as ex:
        ic(ex)

        if "company_exception user_email" in str(ex):
            return jsonify({"error": "Invalid credentials"}), 401

        if "company_exception user_password" in str(ex):
            return jsonify({"error": "Invalid credentials"}), 401

        return jsonify({"error": "System under maintenance"}), 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()