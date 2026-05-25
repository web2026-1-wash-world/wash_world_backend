from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
import uuid
import time

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

import x

from icecream import ic
ic.configureOutput(prefix=f"_____ | ", includeContext=True)

app = Flask(__name__)
app.json.ensure_ascii = False # Denne linje viser ÆØÅ i JSON svar, ellers bliver de til unicode

from flask_cors import CORS
CORS(app)

app.config["JWT_SECRET_KEY"] = "din-hemmelige-key"
jwt = JWTManager(app)


##########################################################
# MATEMATIK TIL AT BEREGNE AFSTAND TIL NÆRMESTE VASKEHAL #
##########################################################
from math import radians, sin, cos, sqrt, atan2

def distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c
##########################################################

##############################
@app.get("/sign-up")
def show_sign_up():
    return render_template("/page_sign_up.html")

##############################
@app.post("/sign-up")
def sign_up():
    try:
        user_pk = uuid.uuid4().hex
        user_first_name = x.validate_user_first_name(request.form.get("user_first_name", ""))
        user_last_name = x.validate_user_last_name(request.form.get("user_last_name", ""))
        user_email = x.validate_user_email(request.form.get("user_email", ""))
        user_password = x.validate_user_password(request.form.get("user_password", ""))
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
@app.post("/login")
def login():
    try:
        user_email = x.validate_user_email(request.form.get("user_email", "") )
        user_password = x.validate_user_password(request.form.get("user_password", ""))

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
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "user_first_name": user_first_name,
                "user_last_name": user_last_name,
                "user_email": user_email
            }
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
@app.get("/forgot-password")
def show_forgot_password():
    return render_template("/page_forgot_password.html")

##############################
@app.post("/forgot-password")
def forgot_password():
    try:
        user_email = x.validate_user_email(request.form.get("user_email", ""))
        db, cursor = x.db()
        q = "SELECT user_reset_password_key AS 'reset_key' FROM users WHERE user_email = %s"
        cursor.execute(q, (user_email,))
        row = cursor.fetchone()

        if not row:
            return "Email not found", 400

        html_forgot_password = render_template("/email_forgot_password.html", user_reset_password_key=row["reset_key"])

        x.send_email("Reset your password", html_forgot_password)

        return "Check your email"

    except Exception as ex:
        ic(ex)

        if "company_exception email" in str(ex):
            return "invalid email", 400
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.get("/reset-password/<reset_key>")
def show_reset_password(reset_key):
    try:
        reset_key = x.validate_uuid4_paranoia(reset_key)
        db, cursor = x.db()

        q = """SELECT user_reset_password_key FROM users WHERE user_reset_password_key = %s"""
        cursor.execute(q, (reset_key,))
        row = cursor.fetchone()

        if not row:
            return "ups...", 400

        return render_template("/page_reset_password.html", reset_key=reset_key)

    except Exception as ex: 
        ic(ex)
        if "company_exception uuid4 invalid" in str(ex):
            return "Invalid key", 400

        return str(ex), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.post("/reset-password")
def reset_password():
    try:
        password = x.validate_user_password( request.form.get("password", ""))
        confirm_password = request.form.get("confirm-password", "").strip()
        if confirm_password != password:
            return "Passwords do not match", 400

        key = x.validate_uuid4_paranoia( request.form.get("key", ""))
        user_hashed_password = generate_password_hash(password)
        new_reset_password_key = uuid.uuid4().hex + uuid.uuid4().hex

        db, cursor = x.db()
        q = """
            UPDATE users
            SET user_password_hashed = %s, user_reset_password_key = %s
            WHERE user_reset_password_key = %s
        """
        cursor.execute(q, (user_hashed_password, new_reset_password_key, key))
        db.commit()

        if cursor.rowcount == 0:
            return "Invalid key", 400

        return "Password changed, please login"

    except Exception as ex:
        ic(ex)

        if "company_exception user_password" in str(ex):
            return f"Password {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters", 400

        if "company_exception paranoia" in str(ex):
            return "Invalid key", 400

        return str(ex), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()




##############################
@app.get("/stations")
def get_stations():
    try:
        db, cursor = x.db()
        q = "SELECT name FROM stations"
        cursor.execute(q)
        stations = cursor.fetchall()

        return jsonify(stations), 200
    except Exception as ex:
        ic(ex)
        return str(ex), 500
    finally: 
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.get("/stations/<station_pk>")
def get_single_station(station_pk):
    try:
        db, cursor = x.db()
        q = "SELECT name, adress, latitude, longitude FROM stations WHERE station_pk = %s"
        cursor.execute(q, (station_pk,))
        station = cursor.fetchone()

        if not station:
            return "Station not found", 404
    
        return jsonify(station), 200

    except Exception as ex:
        ic(ex)
        return str(ex), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.get("/stations/nearby")
def get_nearby_stations():
    try:
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))

        db, cursor = x.db()
        q = """
        SELECT station_pk, name, adress, latitude, longitude
        FROM stations
        """
        cursor.execute(q)
        stations = cursor.fetchall()

        for station in stations:
            station["distance"] = distance(
                lat,
                lon,
                float(station["latitude"]),
                float(station["longitude"])
            )

        stations.sort(key=lambda s: s["distance"])

        nearest_3 = stations[:3]

        return jsonify(nearest_3), 200

    except Exception as ex:
        ic(ex)
        return str(ex), 500

    finally:
        if "cursor" in locals():
            cursor.close()

        if "db" in locals():
            db.close()

# ##############################
# @app.get("/stations/<station_pk>/availability") NICE TO HAVE - IKKE ET MUST?
