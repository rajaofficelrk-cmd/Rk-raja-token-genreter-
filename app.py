import os
import secrets
import requests

from flask import Flask, redirect, request, session, render_template_string

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

APP_ID = os.environ["META_APP_ID"]
APP_SECRET = os.environ["META_APP_SECRET"]
REDIRECT_URI = os.environ["META_REDIRECT_URI"]

PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RK RAJA XWD</title>
<style>
body {
 background:#090909;color:white;
 font-family:Arial;text-align:center;
 padding:35px 15px;
}
.box {
 max-width:400px;margin:auto;
 background:#171717;padding:25px;
 border:1px solid red;border-radius:15px;
}
h1 {color:#ff3030}
button {
 background:#1877f2;color:white;
 border:0;padding:15px;width:100%;
 border-radius:8px;font-weight:bold;
}
a {color:#ff5555}
</style>
</head>
<body>
<div class="box">
<h1>👑 RK RAJA XWD</h1>
<h3>FACEBOOK LOGIN</h3>
{% if user %}
<h2>Welcome {{user.name}}</h2>
<p>Facebook login successful.</p>
<a href="/logout">Logout</a>
{% else %}
<p>Continue with official Facebook authorization.</p>
<a href="/login"><button>Continue with Facebook</button></a>
{% endif %}
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE, user=session.get("user"))

@app.route("/login")
def login():
    from urllib.parse import urlencode
    state = secrets.token_urlsafe(32)
    session["state"] = state

    url = "https://www.facebook.com/v27.0/dialog/oauth?"
    params = {
        "client_id": APP_ID,
        "redirect_uri": REDIRECT_URI,
        "state": state,
        "scope": "public_profile",
        "response_type": "code"
    }
    return redirect(url + urlencode(params))

@app.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")

    if not code or not state:
        return "Login cancelled or failed", 400

    saved = session.pop("state", None)
    if not saved or not secrets.compare_digest(state, saved):
        return "Invalid state", 400

    try:
        response = requests.get(
            "https://graph.facebook.com/v27.0/oauth/access_token",
            params={
                "client_id": APP_ID,
                "client_secret": APP_SECRET,
                "redirect_uri": REDIRECT_URI,
                "code": code
            },
            timeout=15
        )
        response.raise_for_status()
        token = response.json()["access_token"]

        profile = requests.get(
            "https://graph.facebook.com/v27.0/me",
            params={
                "fields": "id,name",
                "access_token": token
            },
            timeout=15
        )
        profile.raise_for_status()

        session.clear()
        session["user"] = profile.json()
        return redirect("/")

    except requests.RequestException:
        return "Facebook authorization failed", 400

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
