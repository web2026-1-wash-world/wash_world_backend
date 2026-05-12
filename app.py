from flask import Flask, render_template, request, jsonify
import uuid
import time
import x
from flask_cors import CORS
from icecream import ic
ic.configureOutput(prefix=f"_____ | ", includeContext=True)

app = Flask(__name__)
CORS(app)  # allows everything

##############################
@app.get("/")
def index():
    return jsonify({"status":"ok", "message":"Connected"})


##############################
@app.route("/people")
def get_people():
    return jsonify({
        "people": [
            {"first_name":"A", "last_name":"Aa", "cpr":"1"},
            {"first_name":"B", "last_name":"Bb", "cpr":"2"},
            {"first_name":"C", "last_name":"Cc", "cpr":"3"},
        ]
    })  

##############################
@app.get("/sign-up")
def show_sign_up():
    return render_template("page_sign_up.html")

##############################
@app.post("/sign-up")
def sign_up():
    try:
        user_first_name = x.validate_user_first_name()
        email = x.validate_email( request.form.get("em", "" ))

        user_pk = uuid.uuid4().hex
        verification_key = uuid.uuid4().hex
        ic(verification_key)
        
        user_reset_password_key = uuid.uuid4().hex + uuid.uuid4().hex
        ic(user_reset_password_key)        

        db, cursor = x.db()
        q = "INSERT INTO users  VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(q, (user_pk, user_first_name, verification_key, 0, user_reset_password_key, email))
        db.commit()
       
        html = render_template("email_welcome.html", verification_key=verification_key)

        x.send_email("Activate your ccount", html)
        return "Please check your email maybe it arrived in the spam folder", 200
    except Exception as ex: 
        ic(ex)
        if "company_exception user_first_name" in str(ex):
            return f"user first {x.USER_FIRST_NAME_MIN} to {x.USER_FIRST_NAME_MAX} characters", 400
        if "company_exception email" in str(ex):
            return "invalid email", 400


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
@app.get("/forgot-password")
def show_forgot_password():
    return render_template("page_forgot_password.html")

##############################
@app.post("/forgot-password")
def forgot_password():
    try:
        email = x.validate_email( request.form.get("email", "") )
        db, cursor = x.db()
        q = "SELECT user_reset_password_key AS 'key' FROM users WHERE user_email = %s"
        cursor.execute(q, (email,))
        row = cursor.fetchone()
        
        if not row: return "Email not found", 400
        html = render_template("email_forgot_password.html", user_reset_password_key=row["key"])
        
        x.send_email("Reset your password", html)

        return "Check your email"

    except Exception as ex:
        ic(ex)

        if "company_exception email" in str(ex):
            return "invalid email", 400

        return str(ex), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()



##############################
@app.get("/reset-password/<key>")
def show_reset_password(key):
    try:
        key = x.validate_uuid4_paranoia(key)
        db, cursor = x.db()
        
        q = """SELECT user_reset_password_key FROM users WHERE user_reset_password_key = %s"""

        cursor.execute(q, (key,))
        row = cursor.fetchone()

        if not row: return "ups...", 400

        return render_template("page_reset_password.html", key=key)
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
@app.delete("/users/<user_pk>")
def delete_user(user_pk):
    try:
        user_pk = x.validate_uuid4(user_pk)
        db, cursor = x.db()
        q = "DELETE FROM users WHERE user_pk = %s"
        cursor.execute(q, (user_pk,))
        db.commit()
        if cursor.rowcount == 0:
            return "User not found", 404
        return "User deleted", 200
    except Exception as ex:
        ic(ex)
        if "company_exception uuid4 invalid" in str(ex):
            return "Invalid key", 400
        return str(ex), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.post("/api-login")
def api_login():
    try:
        user_email = x.validate_email()
        user_password = x.validate_user_password
        db, cursour = x.db()
        q = "SELECT * FROM users WHERE user_email; = %s"
        cursor.execute(q, (user_email, user_password))
        db.commit()
        user.pop("user_password")
        session["user"] = user
        return ("logged in")
    except Exception as ex:
        ic(ex)
        return str(ex), 500
    finally: 
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()
    



"""
##############################
@app.route("/forgot-password", methods=["GET", "POST"])
def show_forgot_password():
    try:
        if request.method == "GET":
            try:
                return render_template("page_forgot_password.html")
            except Exception as ex:
                ic(ex)
            finally:
                pass
        if request.method == "POST":
            try:
                # best case
                pass
            except Exception as ex:
                ic(ex)
                return str(ex), 400
            finally:
                # disconnect from db
                pass
    except Exception as ex:
        ic(ex)
    finally:
        pass   

"""



