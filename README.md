# Simple Flask Upload Server

This is a small Python/Flask-based file upload server. It stores uploaded files in a local folder and returns a public URL. A simple token-based authentication mechanism is included.

## 🔧 Setup Instructions

1. Clone the repository
2. Create and activate a Python virtual environment
3. Install dependencies

```bash
pip install flask python-dotenv
```

## ⚙️ Configuration

Create a `.env` file in the same directory as `app.py` with the following content:

```
UPLOAD_TOKEN=abcde1234
PUBLIC_URL_BASE=https://yourdomain.net:port
UPLOAD_FOLDER=/home/youruser/shared-uploads
```

Make sure the upload folder exists and is writable by the user running the app:

```bash
mkdir -p /home/youruser/shared-uploads
chmod 755 /home/youruser/shared-uploads
```

## 🚀 Run the Server

Activate your virtual environment:

```bash
source venv/bin/activate
```

Then run the app:

```bash
python app.py
```

The server will listen on `http://0.0.0.0:5011`.

## 🔐 Uploading a File (with Auth Token)

Use the following `curl` command to upload a file:

```bash
curl -k -X POST \
  -H "X-Auth-Token: abcde1234" \
  -F "file=@/path/to/your/file.mp4" \
  https://yourdomain.net:5011/upload
```

If the token is valid, you’ll receive a response like:

```json
{"public_url": "https://yourdomain.net:port/uuid-filename.mp4"}
```

## 📂 Serving Uploaded Files

This server does not serve the uploaded files directly on port 6011. You must run a separate file server (like Python's built-in HTTP server, Apache, nginx, or Caddy) to expose the folder defined in `UPLOAD_FOLDER`.

Example using Python’s built-in HTTP server:

```bash
cd /home/youruser/shared-uploads
python3 -m http.server 6011
```

Make sure this port is accessible and served over HTTPS, if needed.

## 🛡️ Security Notes

* Authentication uses a static token passed via the `X-Auth-Token` header.
* Do not expose this service directly to the internet without:

  * HTTPS
  * Firewall rules
  * Possibly IP whitelisting or rate limiting
* For production, consider stronger authentication mechanisms (e.g. API keys, OAuth, or JWT).

## ✅ To-Do

* Add expiration/cleanup for old uploads
* Add file size/type restrictions
* Add logging or rate limiting
* Dockerize the application
* Systemd service integration for persistence
