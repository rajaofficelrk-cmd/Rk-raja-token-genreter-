
import os
import secrets
import requests

from flask import (
    Flask, redirect, request, session,
    render_template, url_for
)

app = Flask(__name__)

app.secret_key = os.environ["FLASK_SECRET_KEY"]

APP_ID = os.environ["META_APP_ID"]
APP_SECRET = os.environ["META_APP_SECRET"]
REDIRECT_URI = os.environ["META_REDIRECT_URI"]
GRAPH_VERSION = os.environ.get("META_GRAPH_VERSION", "v27.0")

AUTH_URL = "https://www.facebook.com/" + GRAPH_VERSION + "/dialog/oauth"
TOKEN_URL = "https://graph.facebook.com/" + GRAPH_VERSION + "/oauth/access_token"

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="Lax"
)


@app.route("/")
def home():
    return render_template(
        "index.html",
        user=session.get("user")
    )


@app.route("/login")
def login():
    state = secrets.token_urlsafe(32)
    session["oauth_state"] = state

    params = {
        "client_id": APP_ID,
        "redirect_uri": REDIRECT_URI,
        "state": state,
        "response_type": "code",
        "scope": "public_profile"
    }

    from urllib.parse import urlencode
    return redirect(AUTH_URL + "?" + urlencode(params))


@app.route("/callback")
def callback():
    error = request.args.get("error")
    if error:
        return "Facebook login cancelled or denied.", 400

    code = request.args.get("code")
    state = request.args.get("state")

    if not code or not state:
        return "Missing authorization response.", 400

    saved_state = session.pop("oauth_state", None)

    if not saved_state or not secrets.compare_digest(
        state, saved_state
    ):
        return "Invalid login state.", 400

    try:
        response = requests.get(
            TOKEN_URL,
            params={
                "client_id": APP_ID,
                "client_secret": APP_SECRET,
                "redirect_uri": REDIRECT_URI,
                "code": code
            },
            timeout=15
        )
        response.raise_for_status()
        short_token = response.json()["access_token"]

        # Use token only to fetch the authorized basic profile.
        # Do not save or display the access token.
        profile = requests.get(
            f"https://graph.facebook.com/{GRAPH_VERSION}/me",
            params={
                "fields": "id,name",
                "access_token": short_token
            },
            timeout=15
        )
        profile.raise_for_status()

        session.clear()
        session["user"] = profile.json()

        return redirect(url_for("home"))

    except (requests.RequestException, KeyError, ValueError):
        return "Facebook authentication failed.", 400


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/privacy")
def privacy():
    return """
    <h1>Privacy Policy - RK RAJA XWD</h1>
    <p>We use Facebook Login for authentication.</p>
    <p>We do not sell or publicly share login credentials.</p>
    <p>Users can log out and request account data deletion.</p>
    """


@app.route("/data-deletion")
def data_deletion():
    return """
    <h1>Data Deletion</h1>
    <p>Contact the website administrator to request deletion
    of data associated with your login.</p>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
