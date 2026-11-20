# Solomons-Borenstein Telegraph System

The browser app connects two clients using a small WebSocket signaling server and a WebRTC data channel. The server forwards only connection setup details; messages are sent directly between the two browsers.

## Run locally

```powershell
python -m pip install -r requirements.txt
python server.py
```

Open `http://localhost:8080` in both browsers. In the first browser, choose **Create room** and share the displayed room code. In the second, enter that code and choose **Join room**.

## Deploy online with Render

Render is one option for hosting this as a Python web service. It supports the WebSocket signaling endpoint. The folder must be in a Git repository connected to your Render account.

### 1. Push the project to GitHub

Create an empty GitHub repository, then run these commands in PowerShell:

```powershell
cd C:\Telegraph
git init -b main
git add README.md index.html server.py requirements.txt test_server.py
git commit -m "Add telegraph web app"
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the GitHub URL with your repository's URL. GitHub may ask you to authenticate through your browser.

### 2. Create the Render service

1. Sign in to [Render](https://dashboard.render.com/) and choose **New > Web Service**.
2. Connect GitHub if prompted, then select the repository you just pushed.
3. Configure the service:
   - **Language:** Python 3
   - **Root Directory:** leave blank if the files are at the repository root
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python server.py`
   - **Instance count:** one
4. Choose a plan and click **Create Web Service**. Render sets `PORT` automatically; the server already uses it.
5. When the deploy finishes, open the HTTPS URL Render gives you.

### 3. Connect the two clients

Open the same HTTPS URL in both browsers. In the first, choose **Create room** and share the displayed room code. In the second, enter the code and choose **Join room**.

The room list is kept in server memory, so use one service instance. Free Render services can sleep after 15 minutes without traffic and may take about a minute to wake up. This app uses STUN for direct WebRTC connections; some restrictive networks also require a TURN relay.

See Render's [Web Services guide](https://render.com/docs/web-services) and [free instance limitations](https://render.com/docs/free#free-web-services) for current hosting details.
