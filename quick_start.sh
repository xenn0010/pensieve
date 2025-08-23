#!/bin/bash

# 🚀 Pensieve + Runway Navigator Quick Start Script
# This script automates the initial setup for the integration

echo "🚀 Starting Pensieve + Runway Navigator Integration Setup..."
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "   (where package.json and requirements.txt are located)"
    exit 1
fi

# Step 1: Check Prerequisites
echo "🔍 Checking Prerequisites..."
echo "----------------------------"

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Error: Python not found. Please install Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo "✅ Python: $PYTHON_VERSION"

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js: $NODE_VERSION"
else
    echo "❌ Error: Node.js not found. Please install Node.js 18+"
    exit 1
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "✅ npm: $NPM_VERSION"
else
    echo "❌ Error: npm not found. Please install npm"
    exit 1
fi

# Check Redis
if command -v redis-server &> /dev/null; then
    echo "✅ Redis: Found"
else
    echo "⚠️  Warning: Redis not found. You'll need to install Redis or use cloud Redis"
fi

echo ""

# Step 2: Install Python Dependencies
echo "🐍 Installing Python Dependencies..."
echo "-----------------------------------"
$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Error: Failed to install Python dependencies"
    exit 1
fi

echo ""

# Step 3: Install Node Dependencies
echo "📦 Installing Node Dependencies..."
echo "----------------------------------"
npm install

if [ $? -eq 0 ]; then
    echo "✅ Node dependencies installed successfully"
else
    echo "❌ Error: Failed to install Node dependencies"
    exit 1
fi

echo ""

# Step 4: Environment Setup
echo "⚙️  Setting up Environment..."
echo "-----------------------------"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file template..."
    cat > .env << EOF
# Core Configuration
APP_NAME=Pensieve_CIO
DEBUG=true

# API Keys (REQUIRED)
GEMINI_API_KEY=your_gemini_api_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
REDIS_URL=redis://localhost:6379

# Optional External APIs
BREX_API_KEY=your_brex_api_key_here
SIXTYFOUR_API_KEY=your_sixtyfour_api_key_here
MIXRANK_API_KEY=your_mixrank_api_key_here

# Demo Mode (for testing)
USE_MOCK_DATA=true
DEMO_FINANCIAL_PROFILE=healthy_saas
EOF
    echo "✅ Created .env file template"
    echo "⚠️  IMPORTANT: Please edit .env file with your actual API keys"
else
    echo "✅ .env file already exists"
fi

echo ""

# Step 5: Create API Configuration
echo "🔧 Creating Frontend API Configuration..."
echo "----------------------------------------"

# Create src/config directory if it doesn't exist
mkdir -p src/config

# Create api.ts file
cat > src/config/api.ts << 'EOF'
export const API_CONFIG = {
  BASE_URL: 'http://localhost:8001',
  ENDPOINTS: {
    HEALTH: '/health',
    DASHBOARD: '/dashboard/overview',
    COMPANY_RESEARCH: '/research/company',
    AGENT_QUERY: '/agent/query',
    INTELLIGENCE: '/intelligence/signals',
    ACTIONS: '/actions/recent'
  },
  WEBSOCKET_URL: 'ws://localhost:8001/ws'
};
EOF

echo "✅ Created API configuration file"

echo ""

# Step 6: Health Check
echo "🏥 Running Health Check..."
echo "---------------------------"

# Check if backend can start
echo "Testing backend startup..."
$PYTHON_CMD -c "
import sys
try:
    import fastapi
    import uvicorn
    import pydantic
    print('✅ Backend dependencies: OK')
except ImportError as e:
    print(f'❌ Backend dependency missing: {e}')
    sys.exit(1)
"

# Check if frontend can start
echo "Testing frontend startup..."
npm run build --silent > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Frontend build: OK"
else
    echo "❌ Frontend build failed"
fi

echo ""

# Step 7: Final Instructions
echo "🎯 Setup Complete! Next Steps:"
echo "==============================="
echo ""
echo "1. 🔑 Edit .env file with your API keys:"
echo "   - GEMINI_API_KEY (Google AI)"
echo "   - SUPABASE_URL and SUPABASE_KEY"
echo "   - REDIS_URL"
echo ""
echo "2. 🚀 Start Backend:"
echo "   python frontend_api.py"
echo ""
echo "3. 🌐 Start Frontend:"
echo "   npm run dev"
echo ""
echo "4. 🔍 Test Integration:"
echo "   - Backend: http://localhost:8001/health"
echo "   - Frontend: http://localhost:3000"
echo ""
echo "5. 📚 Read INTEGRATION_GUIDE.md for detailed steps"
echo ""
echo "🎉 Happy coding! Your Pensieve + Runway Navigator integration is ready!"
echo ""
echo "For help, check:"
echo "  - INTEGRATION_GUIDE.md (comprehensive guide)"
echo "  - API_DOCUMENTATION.md (API reference)"
echo "  - Troubleshooting section in the guide"
