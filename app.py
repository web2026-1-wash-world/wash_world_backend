from flask import Flask, render_template, request, jsonify, redirect
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
import uuid
import time

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

import x

from icecream import ic
ic.configureOutput(prefix=f"___ | ", includeContext=True)

app = Flask(__name__)
app.json.ensure_ascii = False # Denne linje viser ÆØÅ i JSON svar, ellers bliver de til unicode

from flask_cors import CORS
CORS(app)

app.config["JWT_SECRET_KEY"] = "super-secret-key"
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

##############################
@app.post("/sign-up")
def sign_up():
    try:
        data = request.form
        
        user_pk = uuid.uuid4().hex
        user_first_name = x.validate_user_first_name(data.get("user_first_name", ""))
        user_last_name = x.validate_user_last_name(data.get("user_last_name", ""))
        user_email = x.validate_user_email(data.get("user_email", ""))
        user_password = x.validate_user_password(data.get("user_password", ""))
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

        x.send_email("Verificer din profil", activation_email)

        return jsonify({"message": "Vi har sendt en verificerings-email"}), 201
    except Exception as ex:
        ic(ex)
        if "company_exception user_first_name" in str(ex):
            return jsonify({
                "field" : "user_first_name",
                "error": f"Fornavn skal være mellem {x.USER_FIRST_NAME_MIN} og {x.USER_FIRST_NAME_MAX} tegn"
                }), 400
            
        if "company_exception user_last_name" in str(ex):
            return jsonify({
                "field" : "user_last_name",
                "error": f"Efternavn skal være mellem {x.USER_LAST_NAME_MIN} og {x.USER_LAST_NAME_MAX} tegn"
                }), 400

        if "company_exception user_email" in str(ex):
            return jsonify({
                "field" : "user_email",
                "error":"Ugyldig email"
                }), 400

        if "company_exception user_password" in str(ex):
            return jsonify({
                "field" : "user_password",
                "error" : f"Adgangskoden skal minimum være {x.USER_PASSWORD_MIN} tegn"
                }), 400

        return str(ex), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################

@app.post("/login")
def login():
    try:
        data = request.form

        user_email = x.validate_user_email(data.get("user_email", "") )
        user_password = x.validate_user_password(data.get("user_password", ""))

        db, cursor = x.db()
        q = """
        SELECT
            user_pk,
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
        
        user_pk = user["user_pk"]
        user_first_name = user["user_first_name"]
        user_last_name = user["user_last_name"]
        user_email = user["user_email"]

        access_token = create_access_token(identity=user_email)

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "user_pk": user_pk,
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
@app.get("/profile")
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({"user": current_user}), 200

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

        return redirect(f"http://localhost:3000/login")
    except Exception as ex: 
        ic(ex)
        if "company_exception uuid4 invalid" in str(ex):
            return "Invalid key", 400

        return str(ex), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.post("/logout")
@jwt_required()
def logout():
    return jsonify({"message": "Logout successful"}), 200

##############################
@app.delete("/delete-user/<user_pk>")
@jwt_required()
def delete_account(user_pk):
    try:
        db, cursor = x.db()
        user_email = get_jwt_identity()
        q = "DELETE FROM users WHERE user_pk = %s"
        cursor.execute(q, (user_pk,))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"message":"User not found"}), 404

        return jsonify({"message":"Din bruger blev slettet"}), 200

    except Exception as ex:
        ic(ex)
        return str(ex), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.post("/forgot-password")
def forgot_password():
    try:
        data = request.form

        user_email = x.validate_user_email(data.get("user_email", ""))

        db, cursor = x.db()

        q = "SELECT user_reset_password_key AS reset_key FROM users WHERE user_email = %s"
        cursor.execute(q, (user_email,))
        row = cursor.fetchone()

        if not row:
            return jsonify({
                "field" : "user_email",
                "error": "Email not found"
                }), 400

        html_forgot_password = render_template(
            "email_forgot_password.html",
            user_reset_password_key=row["reset_key"]
        )

        x.send_email("Reset your password", html_forgot_password)

        return jsonify({"message": "Check your email"}), 200

    except Exception as ex:
        ic(ex)

        if "company_exception user_email" in str(ex):
            return jsonify({
                "field" : "user_email",
                "error": "invalid email"
                }), 400

        return {"error": "server error"}, 500

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

        return redirect(f"http://localhost:3000/reset-password/{reset_key}")

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
        data = request.form

        password = x.validate_user_password( data.get("user_password", ""))
        confirm_password = x.validate_user_password(data.get("confirm_password", ""))
        if confirm_password != password:
            return jsonify({
                "field" : "confirm_password",
                "error" : "Passwords do not match"
                }), 400

        key = x.validate_uuid4_paranoia( data.get("reset_key", ""))
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
            return jsonify({"Invalid key"}), 400

        return redirect(f"http://localhost:3000/login")

    except Exception as ex:
        ic(ex)

        if "company_exception user_password" in str(ex):
            return jsonify({
                "field" : "user_password",
                "error": f"Password {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters"
                }), 400

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
        q = "SELECT station_pk, name, latitude, longitude FROM stations"
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

##############################
@app.get("/memberships")
def get_memberships():
    try:
        
        db, cursor = x.db()
        q = "SELECT membership_pk, name, price_per_month FROM memberships"
        cursor.execute(q)
        memberships = cursor.fetchall()

        return jsonify(memberships), 200

    except Exception as ex:
        ic(ex)
        return str(ex), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.post("/subscribe")
@jwt_required()
def subscribe_membership():
    try:
        
        data = request.form
        membership_id = data.get("membership_id")

        if not membership_id:
            return "membership_id is required", 400
        
        user_email = get_jwt_identity()

        db, cursor = x.db()
        q = "SELECT user_pk FROM users WHERE user_email = %s"
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()

        if not user:
            return "User not found", 404

        # Check if user already has an active membership
        q = """
            SELECT user_membership_pk
            FROM user_memberships
            WHERE user_id = %s
            AND status = 'active'
            LIMIT 1
        """
        cursor.execute(q, (user["user_pk"],))
        existing_membership = cursor.fetchone()

        if existing_membership:

            # Update existing membership
            q = """
                UPDATE user_memberships
                SET membership_id = %s
                WHERE user_membership_pk = %s
            """
            cursor.execute(
                q,
                (
                    membership_id,
                    existing_membership["user_membership_pk"]
                )
            )

            message = "Membership updated"

        else:

            # Create new membership
            user_membership_pk = uuid.uuid4().hex
            start_date = int(time.time())

            q = """
                INSERT INTO user_memberships
                (
                    user_membership_pk,
                    user_id,
                    membership_id,
                    start_date,
                    end_date,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                q,
                (
                    user_membership_pk,
                    user["user_pk"],
                    membership_id,
                    start_date,
                    None,
                    "active"
                )
            )

            message = "Subscription successful"

        db.commit()

        return jsonify({"message": message}), 200

    except Exception as ex:
        ic(ex)
        return str(ex), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

###############################
@app.get("/users/membership")
@jwt_required()
def get_user_subscription():
    try:
        
        user_email = get_jwt_identity()

        db, cursor = x.db()
        q = """
        SELECT
            memberships.membership_pk,
            memberships.name,
            memberships.price_per_month,
            user_memberships.status
        FROM users
        JOIN user_memberships
            ON users.user_pk = user_memberships.user_id
        JOIN memberships
            ON memberships.membership_pk = user_memberships.membership_id
        WHERE users.user_email = %s
        AND user_memberships.status = 'active'
        LIMIT 1
        """

        cursor.execute(q, (user_email,))
        membership = cursor.fetchone()

        if not membership:
            return jsonify(None), 200

        return jsonify(membership), 200

    except Exception as ex:
        ic(ex)
        return str(ex), 500
    finally:
        if "cursor" in locals():cursor.close()
        if "db" in locals(): db.close()

###############################
@app.patch("/user-membership")
@jwt_required()
def cancel_membership():
    try:
        
        user_email = get_jwt_identity()

        db, cursor = x.db()

        q = "SELECT user_pk FROM users WHERE user_email = %s"
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()

        if not user:
            return "User not found", 404

        q = """UPDATE user_memberships SET status = 'cancelled', end_date = %s WHERE user_id = %s AND status = 'active'"""

        cursor.execute(q, (int(time.time()), user["user_pk"]))

        db.commit()

        if cursor.rowcount == 0:
            return "No active subscription found", 404

        return jsonify({"message": "Subscription cancelled"}), 200

    except Exception as ex:
        ic(ex)
        return str(ex), 500
    finally:
        if "cursor" in locals():cursor.close()
        if "db" in locals(): db.close()

##############################
@app.post("/cars")
@jwt_required()
def api_create_cars():
    try:
        user_email = get_jwt_identity()
        # data = request.form
        car_pk = uuid.uuid4().hex
        car_license_plate = x.validate_car_license_plate(request.form.get("car_license_plate", ""))
        car_brand = x.validate_car_brand(request.form.get("car_brand", ""))
        car_model = x.validate_car_model(request.form.get("car_model", ""))
        user_created_at = int(time.time())
        user_updated_at = int(time.time()) 

        db, cursor = x.db()
        cursor.execute("SELECT user_pk FROM users WHERE user_email = %s", (user_email,))
        user = cursor.fetchone()
        if not user: 
            return jsonify({"error": "User not found"}), 404                                                            
        q = "INSERT INTO cars (car_pk, user_id, car_license_plate, car_brand, car_model, car_created_at, car_updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"                                                       
        cursor.execute(q, (car_pk, user["user_pk"], car_license_plate, car_brand, car_model, user_created_at, user_updated_at))  
        db.commit()                                                                                        
        return jsonify({"car_pk": car_pk}), 201  
    except Exception as ex: 
        ic(ex)                                                                                             
        if "company_exception car_license_plate" in str(ex):
            return jsonify({
                "field": "car_license_plate",
                "error": f"Nummerplade skal være mellem {x.CAR_LICENSE_PLATE_MIN} og {x.CAR_LICENSE_PLATE_MAX} tegn"
            }), 400
        if "company_exception car_brand" in str(ex):
            return jsonify({
                "field": "car_brand",
                "error": f"Mærke skal være mellem {x.CAR_BRAND_MIN} og {x.CAR_BRAND_MAX} tegn"
            }), 400
        if "company_exception car_model" in str(ex):
            return jsonify({
                "field": "car_model",
                "error": f"Model skal være mellem {x.CAR_MODEL_MIN} og {x.CAR_MODEL_MAX} tegn"
            }), 400
        return str(ex), 500                                                                                
    finally:                                                                                             
        if "cursor" in locals(): cursor.close()                                                            
        if "db" in locals(): db.close()


##############################
@app.get("/cars")
@jwt_required()
def get_cars():
    try:
        user_email = get_jwt_identity()
        db, cursor = x.db()
        cursor.execute("SELECT user_pk FROM users WHERE user_email = %s", (user_email,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        q = "SELECT * FROM cars WHERE user_id = %s"
        cursor.execute(q, (user["user_pk"],))
        cars = cursor.fetchall()
        return jsonify(cars), 200
    except Exception as ex:
        ic(ex)
        return jsonify({"error": "System under maintenance"}), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.get("/cars/<car_pk>")
@jwt_required()
def get_car(car_pk):
  try:
      user_email = get_jwt_identity()
      db, cursor = x.db()
      cursor.execute("SELECT user_pk FROM users WHERE user_email = %s", (user_email,))
      user = cursor.fetchone()
      if not user:
          return jsonify({"error": "User not found"}), 404
      cursor.execute("SELECT * FROM cars WHERE car_pk = %s AND user_id = %s", (car_pk, user["user_pk"]))
      car = cursor.fetchone()
      if not car:
          return jsonify({"error": "Car not found"}), 404
      return jsonify(car), 200
  except Exception as ex:
      ic(ex)
      return jsonify({"error": "System under maintenance"}), 500
  finally:
      if "cursor" in locals(): cursor.close()
      if "db" in locals(): db.close()

##############################
@app.patch("/cars/<car_pk>")
@jwt_required()
def update_car(car_pk):
    try:
        parts = []
        values = []

        car_license_plate = request.form.get("car_license_plate", "").strip()
        if car_license_plate:
            parts.append("car_license_plate = %s")
            values.append(x.validate_car_license_plate(car_license_plate))

        car_brand = request.form.get("car_brand", "").strip()
        if car_brand:
            parts.append("car_brand = %s")
            values.append(x.validate_car_brand(car_brand))

        car_model = request.form.get("car_model", "").strip()
        if car_model:
            parts.append("car_model = %s")
            values.append(x.validate_car_model(car_model))

        if not parts:
            return jsonify({"error": "No fields to update"}), 400

        partial_query = ", ".join(parts)
        values.append(car_pk)

        db, cursor = x.db()
        q = f"UPDATE cars SET {partial_query} WHERE car_pk = %s"
        cursor.execute(q, values)
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Car not found"}), 404
        return jsonify({"message": "Car updated"}), 200
    except Exception as ex:
        ic(ex)
        if "company_exception car_license_plate" in str(ex):
            return f"License plate must be {x.CAR_LICENSE_PLATE_MIN}-{x.CAR_LICENSE_PLATE_MAX} characters", 400
        if "company_exception car_brand" in str(ex):
            return f"Brand must be {x.CAR_BRAND_MIN}-{x.CAR_BRAND_MAX} characters", 400
        if "company_exception car_model" in str(ex):
            return f"Model must be {x.CAR_MODEL_MIN}-{x.CAR_MODEL_MAX} characters", 400
        return jsonify({"error": "System under maintenance"}), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.delete("/cars/<car_pk>")
@jwt_required()
def delete_car(car_pk):
    try:
        user_email = get_jwt_identity()
        db, cursor = x.db()
        cursor.execute("SELECT user_pk FROM users WHERE user_email = %s", (user_email,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        q = "DELETE FROM cars WHERE car_pk = %s AND user_id = %s"
        cursor.execute(q, (car_pk, user["user_pk"]))
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Car not found"}), 404
        return "", 204
    except Exception as ex:
        ic(ex)
        return jsonify({"error": "System under maintenance"}), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()