# How to Run MedAssist

We have combined the Frontend and Backend into a single launcher for convenience.

## Option 1: One-Click Launcher (Recommended)
1. Double-click the `run_medassist.bat` file in this folder.
2. It will:
   - Start the Backend Server (Port 6969)
   - Start the React Frontend (Port 5173) [Requires Node.js]
   - Automatically open your browser to the Dashboard.
3. To stop, simply press any key in the launcher window.

## Option 2: Manual Start
If you prefer running terminals manually:
1. Terminal 1 (Backend): `python app.py`
2. Terminal 2 (Frontend): `cd frontend` then `npm run dev`

## Access
- **Dashboard URL**: http://localhost:5173
