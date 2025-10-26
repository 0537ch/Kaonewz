# 🌍 Kaonz – Country Analytics Dashboard

A modern web application that visualizes country statistics and news in an interactive 3D interface. Built with FastAPI, React, and Three.js.

## ✨ Features

### 🌐 Global Country Data
- Interactive 3D globe visualization
- Country statistics (population, area, density)
- Regional comparisons and rankings
- Responsive design for all devices

### 📰 Integrated News
- Latest headlines by country
- Category-based filtering (business, tech, sports, etc.)
- Search functionality across global news
- Clean, readable article previews

### 🛠️ Technical Highlights
- **Frontend**: React 19 + Vite + Three.js
- **Backend**: FastAPI + Pandas
- **Styling**: TailwindCSS + GSAP animations
- **3D Visualization**: React Three Fiber
- **Data Sources**: REST Countries API, NewsAPI

## 🚀 Quick Start

1. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   # Windows: venv\Scripts\activate
   # macOS/Linux: source venv/bin/activate
   pip install -r requirements.txt
   # Add your NewsAPI key to backend/.env
   uvicorn main:app --reload
   ```

2. **Start the frontend**
   ```bash
   cd ../kaon
   npm install
   npm run dev
   ```

3. Open `http://localhost:5173` in your browser

## 📁 Project Structure
```
Kaonz/
├── backend/         # FastAPI application
│   ├── main.py      # API routes
│   └── services/    # Business logic
└── kaon/           # React frontend
    ├── src/        # Components and pages
    └── public/     # Static assets
```

## 🌟 Key Technologies

### Frontend
- **React 19** - UI components
- **Vite** - Build tooling
- **Three.js** - 3D visualizations
- **TailwindCSS** - Styling
- **GSAP** - Animations

### Backend
- **FastAPI** - REST API
- **Pandas** - Data processing
- **Python-dotenv** - Environment management

## 📚 API Documentation
Access the interactive API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📝 License
MIT License - feel free to use this project for any purpose.
