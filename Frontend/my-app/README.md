# 🌱 Frontend Environment Setup
React supports multiple .env files automatically based on the command you use. This allows easy switching between local development and deployed production mode without touching code.

# 📁 Location
Place your environment files inside:

Frontend/my-app/

🧾 Required Files
**File:** .env.development **Purpose:** For local development testing **How to use:** npm start__
**File:** .env.production **Purpose:** For deployment **How to use:** npm run build

🔧 .env.development (for local backend)__
Create the file: Frontend/my-app/.env.development with:

"REACT_APP_API_BASE_URL=http://localhost:5000"

This lets the frontend send requests to your local Flask backend running on port 5000.

🚀 .env.production (for deployment)__
Create the file: Frontend/my-app/.env.production with:

"REACT_APP_API_BASE_URL=https://cse-108-final.onrender.com"

This is the deployed Render backend URL. It will be used automatically when you build for production.

⚙️ How to Use__
▶️ Run Locally

# Start Flask backend
python run.py

# Start React frontend
cd Frontend/my-app__
npm start__
✅ React uses .env.development__
✅ Requests go to http://localhost:5000__

🚀 Deploy / Build for Production

cd Frontend/my-app__
✅ React uses .env.production__
✅ Requests go to https://cse-108-final.onrender.com__

🧠 Code Usage__
In your React code, always use:

const API_BASE = process.env.REACT_APP_API_BASE_URL;__
React will inject the correct value based on the environment.