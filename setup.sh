#!/bin/bash

# AI Game Development System - Setup Script
# Run this to set up your environment quickly

echo "======================================"
echo "🎮 AI Game Development System Setup"
echo "======================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo -e "${RED}❌ Python 3.10+ required. Current version: $python_version${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python $python_version found${NC}"
echo ""

# Create project directory structure
echo "📁 Creating directory structure..."
mkdir -p ai_game_dev/{agents,assets,builds,configs,logs,tests}
mkdir -p ai_game_dev/assets/{models,textures,audio,ui}
echo -e "${GREEN}✅ Directories created${NC}"
echo ""

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists. Skipping...${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi
echo ""

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✅ Pip upgraded${NC}"
echo ""

# Install requirements
echo "📥 Installing Python packages..."
echo "   This may take a few minutes..."
pip install -r requirements.txt > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ All packages installed successfully${NC}"
else
    echo -e "${RED}❌ Error installing packages. Check requirements.txt${NC}"
    exit 1
fi
echo ""

# Clone Unity MCP
echo "🎮 Cloning Unity MCP..."
if [ -d "unity-mcp" ]; then
    echo -e "${YELLOW}⚠️  unity-mcp already exists. Skipping clone...${NC}"
else
    git clone https://github.com/justinpbarnett/unity-mcp.git > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Unity MCP cloned${NC}"
    else
        echo -e "${RED}❌ Failed to clone Unity MCP${NC}"
    fi
fi
echo ""

# Install Unity MCP dependencies
if [ -d "unity-mcp" ]; then
    echo "📦 Installing Unity MCP dependencies..."
    cd unity-mcp
    pip install -r requirements.txt > /dev/null 2>&1
    cd ..
    echo -e "${GREEN}✅ Unity MCP dependencies installed${NC}"
    echo ""
fi

# Create .env template if it doesn't exist
echo "🔑 Setting up environment variables..."
if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file already exists. Skipping...${NC}"
else
    cat > .env << 'EOF'
# AI Game Development System - Environment Variables
# Fill in your API keys below

# AI APIs
ANTHROPIC_API_KEY=your-claude-api-key-here
GOOGLE_API_KEY=your-gemini-api-key-here

# Asset Generation APIs
MESHY_API_KEY=your-meshy-api-key-here
LEONARDO_API_KEY=your-leonardo-api-key-here
SUNO_API_KEY=your-suno-api-key-here
ELEVENLABS_API_KEY=your-elevenlabs-api-key-here
STABILITY_API_KEY=your-stability-api-key-here
POLYHIVE_API_KEY=your-polyhive-api-key-here

# Paths
UNITY_PROJECT_PATH=/home/user/Unity/Projects
UNITY_MCP_PATH=/home/user/Game-OS/unity-mcp
PROJECT_ROOT=/home/user/Game-OS

# Steam (optional)
STEAM_USERNAME=your-steam-username
STEAM_PASSWORD=your-steam-password
STEAM_APP_ID=your-app-id

# Development Settings
DEBUG=True
LOG_LEVEL=INFO
EOF
    echo -e "${GREEN}✅ .env template created${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env and add your API keys!${NC}"
fi
echo ""

# Create config file
echo "⚙️  Creating configuration file..."
cat > ai_game_dev/configs/config.yaml << 'EOF'
# AI Game Development System Configuration

project:
  name: "AI Game Dev System"
  version: "1.0.0"

agents:
  master:
    model: "claude-sonnet-4-5-20250929"
    max_tokens: 8000
    temperature: 0.7

  designer:
    model: "claude-sonnet-4-5-20250929"
    max_tokens: 16000
    temperature: 0.8

  builder:
    model: "gemini-2.0-flash-exp"
    max_tokens: 8000
    temperature: 0.6

  asset_generator:
    model: "claude-sonnet-4-5-20250929"
    max_tokens: 4000
    temperature: 0.9

unity:
  version: "2021.3"
  mcp_port: 3000
  project_template: "3D"

assets:
  3d_models:
    provider: "meshy"
    format: "fbx"
    resolution: 1024

  textures:
    provider: "polyhive"
    resolution: 2048

  audio:
    music_provider: "suno"
    voice_provider: "elevenlabs"

steam:
  enabled: false
  auto_upload: false

logging:
  level: "INFO"
  file: "logs/ai_game_dev.log"
EOF
echo -e "${GREEN}✅ Configuration file created${NC}"
echo ""

# Create a simple test script
echo "🧪 Creating test script..."
cat > test_setup.py << 'EOF'
#!/usr/bin/env python3
"""Test script to verify setup"""

import sys
import os

def test_imports():
    """Test that all required packages are installed"""
    print("🧪 Testing imports...")

    try:
        import anthropic
        print("✅ anthropic")
    except ImportError:
        print("❌ anthropic")
        return False

    try:
        import google.generativeai as genai
        print("✅ google-generativeai")
    except ImportError:
        print("❌ google-generativeai")
        return False

    try:
        import requests
        print("✅ requests")
    except ImportError:
        print("❌ requests")
        return False

    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv")
    except ImportError:
        print("❌ python-dotenv")
        return False

    try:
        import elevenlabs
        print("✅ elevenlabs")
    except ImportError:
        print("❌ elevenlabs")
        return False

    return True

def test_env():
    """Test environment variables"""
    print("\n🔑 Testing environment variables...")

    from dotenv import load_dotenv
    load_dotenv()

    keys = [
        'ANTHROPIC_API_KEY',
        'GOOGLE_API_KEY',
        'MESHY_API_KEY',
        'UNITY_PROJECT_PATH'
    ]

    all_set = True
    for key in keys:
        value = os.getenv(key)
        if value and value != f"your-{key.lower().replace('_', '-')}-here":
            print(f"✅ {key}")
        else:
            print(f"⚠️  {key} not set")
            all_set = False

    return all_set

def test_directories():
    """Test directory structure"""
    print("\n📁 Testing directories...")

    dirs = [
        'ai_game_dev',
        'ai_game_dev/agents',
        'ai_game_dev/assets',
        'ai_game_dev/configs'
    ]

    all_exist = True
    for dir in dirs:
        if os.path.exists(dir):
            print(f"✅ {dir}")
        else:
            print(f"❌ {dir}")
            all_exist = False

    return all_exist

if __name__ == "__main__":
    print("="*60)
    print("🎮 AI Game Development System - Setup Test")
    print("="*60)
    print()

    imports_ok = test_imports()
    env_ok = test_env()
    dirs_ok = test_directories()

    print()
    print("="*60)
    if imports_ok and env_ok and dirs_ok:
        print("✅ Setup is complete and working!")
        print()
        print("Next steps:")
        print("1. Edit .env file with your API keys")
        print("2. Run: python test_setup.py  (again to verify keys)")
        print("3. Follow QUICK_START_GUIDE.md")
    else:
        print("⚠️  Setup has issues. Please fix the errors above.")
        sys.exit(1)
    print("="*60)
EOF

chmod +x test_setup.py
echo -e "${GREEN}✅ Test script created${NC}"
echo ""

# Run test
echo "🧪 Running setup test..."
echo ""
python3 test_setup.py

echo ""
echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file: nano .env"
echo "2. Add your API keys"
echo "3. Run test: python test_setup.py"
echo "4. Follow QUICK_START_GUIDE.md"
echo ""
echo "To activate the virtual environment in future sessions:"
echo "  source venv/bin/activate"
echo ""
echo "Happy AI game development! 🎮"
