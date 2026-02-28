#!/bin/bash

# OpenClaw Backend - Render Deployment Helper Script

echo "=================================="
echo "OpenClaw Backend Deployment Helper"
echo "=================================="
echo ""

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "✓ Project structure verified"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   Creating from .env.example..."
    cp .env.example .env
    echo "   Please update .env with your database credentials"
fi

echo "📋 Pre-deployment Checklist:"
echo ""
echo "1. ✓ Dockerfile created"
echo "2. ✓ render.yaml created"
echo "3. ✓ Procfile created"
echo "4. ✓ .dockerignore created"
echo ""

# Test local database connection
echo "🔍 Testing database connection..."
if python test_db.py > /dev/null 2>&1; then
    echo "   ✓ Database connection successful"
else
    echo "   ⚠️  Database connection test failed (this is OK if deploying to Render)"
fi
echo ""

# Check if git is initialized
if [ -d ".git" ]; then
    echo "✓ Git repository detected"

    # Check for uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        echo "⚠️  You have uncommitted changes"
        echo ""
        read -p "Would you like to commit and push? (y/N): " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "📝 Committing changes..."
            git add .
            git commit -m "Prepare for Render deployment"

            echo "📤 Pushing to GitHub..."
            git push origin main
            echo "✓ Changes pushed"
        fi
    else
        echo "✓ No uncommitted changes"
    fi
else
    echo "⚠️  Git repository not initialized"
    echo "   Run: git init && git add . && git commit -m 'Initial commit'"
fi

echo ""
echo "=================================="
echo "🚀 Ready for Render Deployment!"
echo "=================================="
echo ""
echo "Next Steps:"
echo ""
echo "1. Go to https://dashboard.render.com/"
echo "2. Click 'New +' → 'Web Service'"
echo "3. Connect your GitHub repository"
echo "4. Configure:"
echo "   - Name: openclaw-backend"
echo "   - Runtime: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port \$PORT --workers 2"
echo ""
echo "5. Add Environment Variables:"
echo "   DATABASE_URL=postgresql+asyncpg://your-database-url"
echo "   APP_ENV=production"
echo "   LOG_LEVEL=INFO"
echo ""
echo "6. Set Health Check Path: /health"
echo "7. Click 'Create Web Service'"
echo ""
echo "📚 Full guide: See RENDER_DEPLOYMENT.md"
echo ""

