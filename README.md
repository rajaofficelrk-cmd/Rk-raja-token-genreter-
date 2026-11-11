
# 👑 RK RAJA XWD – Facebook Login

A secure Facebook OAuth login website built with Python Flask and deployed on Render.

## 🚀 Features

- Official Facebook OAuth Login
- Secure OAuth State Verification
- Basic Facebook Profile
- Secure Session Management
- Logout System
- Privacy Policy Page
- Data Deletion Page
- Render Deployment Support
- Black & Red Neon UI

## 📁 Project Structure

```text
RK-RAJA-FB-TOKEN/
├── app.py
├── requirements.txt
├── render.yaml
└── templates/
    └── index.html
```

## 🛠️ Requirements

- Python 3
- Meta Developer Account
- Facebook App ID
- Facebook App Secret
- Render Account
- GitHub Repository

## ⚙️ Environment Variables

Configure these variables in Render:

```env
FLASK_SECRET_KEY=your_random_secret
META_APP_ID=your_app_id
META_APP_SECRET=your_app_secret
META_REDIRECT_URI=https://your-site.onrender.com/callback
META_GRAPH_VERSION=v27.0
```

Never publish your App Secret.

## 🌐 Deployment

1. Upload project files to GitHub.
2. Open Render.
3. Select New Web Service.
4. Connect your GitHub repository.
5. Set the environment variables.
6. Deploy the service.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn app:app
```

## 🔐 Facebook OAuth Setup

1. Open Meta Developers.
2. Create a Meta App.
3. Configure Facebook Login.
4. Add your website URL.
5. Add the OAuth callback URL:

```text
https://your-site.onrender.com/callback
```

6. Configure Privacy Policy and Data Deletion URLs.
7. Complete applicable Meta App Review requirements.

## 🔒 Security

- Facebook passwords are entered only on Facebook.
- App Secret stays on the server.
- OAuth state verification is enabled.
- Tokens are not publicly displayed or collected.

## 👑 Credits

**RK RAJA XWD**

Official Facebook Login Integration.

Made with ❤️ by RK RAJA
