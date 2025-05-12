🌱 Frontend Environment Setup
React supports multiple .env files automatically based on the command you use. This allows easy switching between local development and deployed production mode without touching code.

📁 Location
Place your environment files inside:

bash
Copy
Edit
Frontend/my-app/
🧾 Required Files
File	Purpose	When Used
.env.development	For local development testing	npm start
.env.production	For deployment	npm run build

🔧 .env.development (for local backend)
Create the file Frontend/my-app/.env.development with:

env
Copy
Edit
REACT_APP_API_BASE_URL=http://localhost:5000
This lets the frontend send requests to your local Flask backend running on port 5000.

🚀 .env.production (for deployment)
Create the file Frontend/my-app/.env.production with:

env
Copy
Edit
REACT_APP_API_BASE_URL=https://cse-108-final.onrender.com
This is the deployed Render backend URL. It will be used automatically when you build for production.

⚙️ How to Use
▶️ Run Locally

bash
Copy
Edit
# Start Flask backend
python run.py

# Start React frontend
cd Frontend/my-app
npm start
✅ React uses .env.development
✅ Requests go to http://localhost:5000

🚀 Deploy / Build for Production

bash
Copy
Edit
cd Frontend/my-app
npm run build
✅ React uses .env.production
✅ Requests go to https://cse-108-final.onrender.com

🧠 Code Usage
In your React code, always use:

js
Copy
Edit
const API_BASE = process.env.REACT_APP_API_BASE_URL;
React will inject the correct value based on the environment.