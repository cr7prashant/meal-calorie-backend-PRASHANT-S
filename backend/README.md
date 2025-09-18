### Backend README.md

```markdown
# Meal Calorie Counter - Backend

A FastAPI backend service for calculating meal calories using the USDA FoodData Central API.

## Setup Instructions

### Prerequisites
- Python 3.11 or 3.12 (recommended)
- pip package manager
- USDA API key from [FoodData Central](https://fdc.nal.usda.gov/api-key-signup.html)

### Installation

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create environment file:
   ```bash
   cp .env.example .env
   ```

6. Edit `.env` file and add your USDA API key:
   ```env
   USDA_API_KEY=your-usda-api-key-here
   ```

7. Start the development server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

8. Open [http://localhost:8000](http://localhost:8000) to verify the API is running
9. Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation

## Decisions & Trade-offs

### Technical Decisions:
1. **FastAPI Framework**: For async capabilities, automatic docs, and type safety
2. **SQLite Database**: For simplicity and easy development setup
3. **JWT Authentication**: Stateless authentication for scalability
4. **Pydantic Models**: For data validation and serialization
5. **Modular Architecture**: Separated routes, models, services, and schemas

### Trade-offs:
1. **SQLite over PostgreSQL**: Chose development simplicity over production features
2. **In-memory caching**: Instead of Redis for easier setup
3. **Basic rate limiting**: Simple implementation instead of complex solutions
4. **Fuzzy matching**: Basic algorithm instead of advanced NLP processing

## API Endpoints

### Authentication
- `POST /auth/register` - Create new user account
- `POST /auth/login` - User login and token generation
- `POST /auth/logout` - User logout (client-side token removal)

### Calorie Calculation
- `POST /api/v1/get-calories` - Calculate calories for a dish

### Sample Request:
```json
{
  "dish_name": "chicken biryani",
  "servings": 2
}
```

### Sample Response:
```json
{
  "dish_name": "chicken biryani",
  "servings": 2,
  "calories_per_serving": 280,
  "total_calories": 560,
  "source": "USDA FoodData Central"
}
```

## Features

- ✅ User authentication with JWT
- ✅ USDA API integration with fuzzy matching
- ✅ SQLite database with user management
- ✅ CORS enabled for frontend integration
- ✅ Input validation with Pydantic
- ✅ Error handling and logging
- ✅ Interactive API documentation

## Database Schema

The application uses SQLite with the following tables:
- `users` - User accounts and authentication
- Automatic schema creation on first run


## Environment Variables

See `.env.example` for required environment variables.
```

---

### Backend .env.example File:

**Update `backend/.env.example`:**

```env
# Database - SQLite (development)
DATABASE_URL=sqlite:///./meal_calorie.db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External API - REQUIRED
USDA_API_KEY=your-usda-api-key-goes-here

# CORS - Frontend URL
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Optional: Server settings
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

---

# Backend Deployment Guide

## Deployment Options

### 1. Railway (Recommended)
1. Connect GitHub repository to Railway
2. Add environment variables in Railway dashboard:
   - `DATABASE_URL` (Railway provides PostgreSQL)
   - `USDA_API_KEY`
   - `SECRET_KEY`
   - `BACKEND_CORS_ORIGINS` (your frontend URL)
3. Deploy automatically on git push

### 2. Render
1. Connect GitHub repository to Render
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables in Render dashboard

### 3. Heroku
1. Create `Procfile` with:
   ```
   web: uvicorn app.main:app --host=0.0.0.0 --port=$PORT
   ```
2. Add `runtime.txt` with Python version
3. Deploy via Git push

### 4. Local Production
```bash
# Install production dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=sqlite:///./meal_calorie.db
export USDA_API_KEY=your-key
export SECRET_KEY=your-secret-key

# Start production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Environment Variables for Production

### Required:
```env
USDA_API_KEY=your-usda-api-key
SECRET_KEY=complex-secret-key-for-production
```

### Optional (production):
```env
DATABASE_URL=postgresql://user:pass@host:port/dbname  # For PostgreSQL
BACKEND_CORS_ORIGINS=["https://your-frontend-domain.com"]
DEBUG=false
```

## Database Migration

For production with PostgreSQL:
1. Install PostgreSQL adapter: `pip install psycopg2-binary`
2. Update `DATABASE_URL` to PostgreSQL connection string
3. Tables will auto-create on first run

## Health Check

Verify deployment by visiting:
- `https://your-api-url/` - Basic API status
- `https://your-api-url/docs` - Interactive documentation
- `https://your-api-url/redoc` - Alternative documentation
```

---

### Additional Backend Files:

**Create `backend/.gitignore` if not exists:**
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environment
venv/
env/

# Database
*.db
*.sqlite3

# Environment files
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log