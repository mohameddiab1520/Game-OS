#!/bin/bash

# Coplay Development Environment Setup Script
# Sets up everything needed to contribute to Coplay

echo "========================================="
echo "🚀 Coplay Development Setup"
echo "========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get GitHub username
echo -e "${BLUE}📝 Enter your GitHub username:${NC}"
read GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo -e "${RED}❌ GitHub username required${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Using GitHub username: $GITHUB_USERNAME${NC}"
echo ""

# Create development directory
DEV_DIR="/home/user/coplay-dev"
echo -e "${BLUE}📁 Creating development directory: $DEV_DIR${NC}"
mkdir -p $DEV_DIR
cd $DEV_DIR

# Check if repositories already exist
if [ -d "coplay-unity-plugin" ] || [ -d "unity-mcp" ]; then
    echo -e "${YELLOW}⚠️  Coplay repositories already exist${NC}"
    echo -e "${YELLOW}Do you want to remove and re-clone? (y/n)${NC}"
    read RECLONE

    if [ "$RECLONE" = "y" ]; then
        rm -rf coplay-unity-plugin unity-mcp
        echo -e "${GREEN}✅ Removed existing repositories${NC}"
    else
        echo -e "${YELLOW}⚠️  Keeping existing repositories${NC}"
        exit 0
    fi
fi

echo ""
echo "========================================="
echo "📥 Step 1: Cloning Repositories"
echo "========================================="
echo ""

# Clone Unity Plugin
echo -e "${BLUE}1/2: Cloning coplay-unity-plugin...${NC}"
git clone https://github.com/$GITHUB_USERNAME/coplay-unity-plugin.git

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Fork not found. Cloning from original...${NC}"
    git clone https://github.com/CoplayDev/coplay-unity-plugin.git

    echo ""
    echo -e "${YELLOW}⚠️  You need to fork this repository on GitHub:${NC}"
    echo -e "${YELLOW}   https://github.com/CoplayDev/coplay-unity-plugin${NC}"
    echo ""
fi

cd coplay-unity-plugin

# Add upstream remote
echo -e "${BLUE}Adding upstream remote...${NC}"
git remote add upstream https://github.com/CoplayDev/coplay-unity-plugin.git 2>/dev/null || echo "Upstream already exists"

# Set your fork as origin
git remote set-url origin https://github.com/$GITHUB_USERNAME/coplay-unity-plugin.git 2>/dev/null

echo -e "${GREEN}✅ coplay-unity-plugin setup complete${NC}"
echo ""

cd ..

# Clone Unity MCP
echo -e "${BLUE}2/2: Cloning unity-mcp...${NC}"
git clone https://github.com/$GITHUB_USERNAME/unity-mcp.git

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Fork not found. Cloning from original...${NC}"
    git clone https://github.com/CoplayDev/unity-mcp.git

    echo ""
    echo -e "${YELLOW}⚠️  You need to fork this repository on GitHub:${NC}"
    echo -e "${YELLOW}   https://github.com/CoplayDev/unity-mcp${NC}"
    echo ""
fi

cd unity-mcp

# Add upstream remote
echo -e "${BLUE}Adding upstream remote...${NC}"
git remote add upstream https://github.com/CoplayDev/unity-mcp.git 2>/dev/null || echo "Upstream already exists"

# Set your fork as origin
git remote set-url origin https://github.com/$GITHUB_USERNAME/unity-mcp.git 2>/dev/null

echo -e "${GREEN}✅ unity-mcp setup complete${NC}"
echo ""

cd ..

# Verify remotes
echo ""
echo "========================================="
echo "🔍 Step 2: Verifying Git Configuration"
echo "========================================="
echo ""

echo -e "${BLUE}coplay-unity-plugin remotes:${NC}"
cd coplay-unity-plugin
git remote -v
echo ""

echo -e "${BLUE}unity-mcp remotes:${NC}"
cd ../unity-mcp
git remote -v
echo ""

cd ..

# Setup Python environment for MCP
echo ""
echo "========================================="
echo "🐍 Step 3: Setting up Python Environment"
echo "========================================="
echo ""

cd unity-mcp

echo -e "${BLUE}Creating virtual environment...${NC}"
python3 -m venv venv

echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

echo -e "${BLUE}Installing dependencies...${NC}"
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
fi

echo ""

cd ..

# Create development scripts
echo ""
echo "========================================="
echo "🛠️  Step 4: Creating Development Scripts"
echo "========================================="
echo ""

# Script to sync with upstream
cat > sync_upstream.sh << 'SYNCEOF'
#!/bin/bash
# Sync with upstream Coplay repositories

echo "🔄 Syncing with upstream..."

cd coplay-unity-plugin
echo "📦 Syncing coplay-unity-plugin..."
git fetch upstream
git checkout main
git merge upstream/main
echo "✅ coplay-unity-plugin synced"
echo ""

cd ../unity-mcp
echo "📦 Syncing unity-mcp..."
git fetch upstream
git checkout main
git merge upstream/main
echo "✅ unity-mcp synced"
echo ""

echo "🎉 All repositories synced with upstream!"
SYNCEOF

chmod +x sync_upstream.sh
echo -e "${GREEN}✅ Created sync_upstream.sh${NC}"

# Script to create feature branch
cat > new_feature.sh << 'FEATUREEOF'
#!/bin/bash
# Create new feature branch in both repos

if [ -z "$1" ]; then
    echo "Usage: ./new_feature.sh feature-name"
    echo "Example: ./new_feature.sh add-claude-opus"
    exit 1
fi

FEATURE_NAME=$1
BRANCH_NAME="feature/$FEATURE_NAME"

echo "🌿 Creating feature branch: $BRANCH_NAME"
echo ""

cd coplay-unity-plugin
git checkout main
git pull origin main
git checkout -b $BRANCH_NAME
echo "✅ Branch created in coplay-unity-plugin"
echo ""

cd ../unity-mcp
git checkout main
git pull origin main
git checkout -b $BRANCH_NAME
echo "✅ Branch created in unity-mcp"
echo ""

echo "🎉 Feature branch '$BRANCH_NAME' created in both repos!"
echo ""
echo "Next steps:"
echo "1. Make your changes"
echo "2. git add & git commit"
echo "3. ./push_feature.sh $FEATURE_NAME"
FEATUREEOF

chmod +x new_feature.sh
echo -e "${GREEN}✅ Created new_feature.sh${NC}"

# Script to push feature branch
cat > push_feature.sh << 'PUSHEOF'
#!/bin/bash
# Push feature branch to your fork

if [ -z "$1" ]; then
    echo "Usage: ./push_feature.sh feature-name"
    exit 1
fi

FEATURE_NAME=$1
BRANCH_NAME="feature/$FEATURE_NAME"

echo "🚀 Pushing feature branch: $BRANCH_NAME"
echo ""

cd coplay-unity-plugin
CURRENT_BRANCH=$(git branch --show-current)

if [ "$CURRENT_BRANCH" = "$BRANCH_NAME" ]; then
    git push origin $BRANCH_NAME
    echo "✅ Pushed coplay-unity-plugin"
    echo ""
    echo "📝 Create PR at:"
    echo "   https://github.com/CoplayDev/coplay-unity-plugin/compare/$BRANCH_NAME"
else
    echo "⚠️  Not on branch $BRANCH_NAME in coplay-unity-plugin"
fi

echo ""

cd ../unity-mcp
CURRENT_BRANCH=$(git branch --show-current)

if [ "$CURRENT_BRANCH" = "$BRANCH_NAME" ]; then
    git push origin $BRANCH_NAME
    echo "✅ Pushed unity-mcp"
    echo ""
    echo "📝 Create PR at:"
    echo "   https://github.com/CoplayDev/unity-mcp/compare/$BRANCH_NAME"
else
    echo "⚠️  Not on branch $BRANCH_NAME in unity-mcp"
fi

echo ""
echo "🎉 Feature branch pushed!"
PUSHEOF

chmod +x push_feature.sh
echo -e "${GREEN}✅ Created push_feature.sh${NC}"

# Script to run tests
cat > run_tests.sh << 'TESTEOF'
#!/bin/bash
# Run all tests

echo "🧪 Running tests..."
echo ""

cd unity-mcp
source venv/bin/activate

echo "🐍 Running Python tests..."
pytest tests/ -v

if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed"
    exit 1
fi
TESTEOF

chmod +x run_tests.sh
echo -e "${GREEN}✅ Created run_tests.sh${NC}"

echo ""

# Create contribution tracker
echo ""
echo "========================================="
echo "📊 Step 5: Creating Contribution Tracker"
echo "========================================="
echo ""

cat > CONTRIBUTIONS.md << 'CONTRIBEOF'
# My Coplay Contributions

## Personal Information
- GitHub: @USERNAME
- Started Contributing: 2025-11-21

---

## Pull Requests

### Submitted
- [ ] #? - Feature Name - Status: In Review

### Merged
- [x] #? - Feature Name - Merged: YYYY-MM-DD

---

## Issues Created
- #? - Issue title

---

## Statistics
- PRs Submitted: 0
- PRs Merged: 0
- Issues Created: 0
- Lines Added: 0
- Lines Removed: 0

---

## Goals
- [ ] First PR merged
- [ ] 5 PRs merged
- [ ] 10 PRs merged
- [ ] Become regular contributor
- [ ] Become core contributor

---

## Learning Log

### YYYY-MM-DD
- Learned: ...
- Challenges: ...
- Solutions: ...
CONTRIBEOF

# Replace USERNAME
sed -i "s/USERNAME/$GITHUB_USERNAME/g" CONTRIBUTIONS.md

echo -e "${GREEN}✅ Created CONTRIBUTIONS.md${NC}"

# Create .env template for development
echo ""
echo "========================================="
echo "🔑 Step 6: Creating .env Template"
echo "========================================="
echo ""

cat > .env.dev << 'ENVEOF'
# Coplay Development Environment Variables

# AI API Keys (for testing)
ANTHROPIC_API_KEY=your-claude-api-key-here
GOOGLE_API_KEY=your-gemini-api-key-here
OPENAI_API_KEY=your-openai-api-key-here

# Asset Generation APIs (for testing new integrations)
MESHY_API_KEY=your-meshy-api-key-here
SUNO_API_KEY=your-suno-api-key-here
ELEVENLABS_API_KEY=your-elevenlabs-api-key-here
LEONARDO_API_KEY=your-leonardo-api-key-here
STABILITY_API_KEY=your-stability-api-key-here

# Development Settings
DEBUG=True
LOG_LEVEL=DEBUG
UNITY_MCP_PORT=3000

# GitHub (for automated PR creation - optional)
GITHUB_TOKEN=your-github-token-here
ENVEOF

echo -e "${GREEN}✅ Created .env.dev template${NC}"

# Summary
echo ""
echo "========================================="
echo "✅ Setup Complete!"
echo "========================================="
echo ""

echo -e "${GREEN}Development environment ready at: $DEV_DIR${NC}"
echo ""

echo "📁 Directory structure:"
echo "  coplay-dev/"
echo "  ├── coplay-unity-plugin/    (Unity C# plugin)"
echo "  ├── unity-mcp/              (Python MCP server)"
echo "  ├── sync_upstream.sh        (Sync with upstream)"
echo "  ├── new_feature.sh          (Create feature branch)"
echo "  ├── push_feature.sh         (Push to GitHub)"
echo "  ├── run_tests.sh            (Run all tests)"
echo "  ├── CONTRIBUTIONS.md        (Track your contributions)"
echo "  └── .env.dev                (Development environment vars)"
echo ""

echo "🚀 Next Steps:"
echo ""
echo "1. Fork repositories on GitHub (if not done):"
echo "   https://github.com/CoplayDev/coplay-unity-plugin"
echo "   https://github.com/CoplayDev/unity-mcp"
echo ""
echo "2. Edit .env.dev with your API keys:"
echo "   nano .env.dev"
echo ""
echo "3. Start your first contribution:"
echo "   cd $DEV_DIR"
echo "   ./new_feature.sh add-claude-opus"
echo ""
echo "4. Read contribution guide:"
echo "   cat ~/Game-OS/CONTRIBUTING_TO_COPLAY.md"
echo ""
echo "5. Join the community:"
echo "   - GitHub Discussions"
echo "   - Discord (if available)"
echo ""

echo "📚 Helpful Commands:"
echo "  cd $DEV_DIR                    # Go to dev directory"
echo "  ./sync_upstream.sh             # Sync with upstream"
echo "  ./new_feature.sh <name>        # Create new feature"
echo "  ./push_feature.sh <name>       # Push feature to GitHub"
echo "  ./run_tests.sh                 # Run all tests"
echo ""

echo -e "${GREEN}Happy Contributing! 🎉${NC}"
