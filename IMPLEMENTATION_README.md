# 🎮 AI Game Development System - Implementation & Testing Guide
**Quick Start to Running & Testing the System**

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Clone & Setup
```bash
cd /home/user
git clone <your-repo-url> Game-OS
cd Game-OS
chmod +x setup.sh
./setup.sh
```

### Step 2: Configure
```bash
# Copy environment template
cp .env.example .env

# Edit and add your API keys
nano .env
```

**Minimum Required Keys:**
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
GOOGLE_API_KEY=your-gemini-key-here
```

### Step 3: Test
```bash
# Activate virtual environment
source venv/bin/activate

# Run validation
python test_setup.py

# Expected output: ✅ Setup is complete and working!
```

### Step 4: Run First Example
```bash
cd examples
python simple_football_manager.py
```

**Output Location:** `examples/output/football_manager/`

---

## 🧪 Testing Checklist

### ✅ Environment Tests
```bash
# 1. Python version
python --version
# Expected: Python 3.10.x or higher

# 2. Dependencies
pip list | grep anthropic
pip list | grep google-generativeai
# Expected: Both should be listed

# 3. Environment variables
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Claude:', os.getenv('ANTHROPIC_API_KEY')[:10] if os.getenv('ANTHROPIC_API_KEY') else 'NOT SET')"
# Expected: Claude: sk-ant-xxx

# 4. Directory structure
ls -la ai_game_dev/
# Expected: agents/, apis/, utils/, etc.
```

### ✅ API Connectivity Tests
```bash
# Test Claude API
python -c "
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
response = client.messages.create(
    model='claude-sonnet-4-5-20250929',
    max_tokens=100,
    messages=[{'role': 'user', 'content': 'Say hi'}]
)
print('✅ Claude API: Working')
print('Response:', response.content[0].text[:50])
"

# Test Gemini API (if configured)
python -c "
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')
response = model.generate_content('Say hi')
print('✅ Gemini API: Working')
print('Response:', response.text[:50])
"
```

### ✅ Functional Tests
```bash
# 1. Simple example (fast - 2 minutes)
cd examples
python simple_football_manager.py

# Verify output
ls -la output/football_manager/
# Expected files:
# - game_design_document.json
# - GameManager.cs
# - Player.cs
# - Team.cs
# - MatchSimulator.cs
# - TransferMarket.cs
# - UIManager.cs
# - ui_design.json
# - IMPLEMENTATION_GUIDE.md
```

### ✅ Unit Tests (if available)
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run unit tests
pytest tests/unit/ -v

# With coverage
pytest tests/unit/ --cov=ai_game_dev --cov-report=term
```

---

## 🚀 Running Different Components

### 1. Generate Game Design Only
```python
# test_design_only.py
from ai_game_dev.agents.designer_agent import DesignerAgent
import os
from dotenv import load_dotenv

load_dotenv()

agent = DesignerAgent(os.getenv('ANTHROPIC_API_KEY'))

concept = {
    "title": "My Test Game",
    "type": "simulation",
    "description": "A simple test game"
}

gdd = agent.create_gdd(concept)
print("✅ GDD Created:", gdd.get('title'))
```

Run:
```bash
python test_design_only.py
```

### 2. Generate Unity Scripts Only
```python
# test_unity_scripts.py
from ai_game_dev.agents.unity_builder_agent import UnityBuilderAgent
import os
from dotenv import load_dotenv

load_dotenv()

agent = UnityBuilderAgent(
    gemini_api_key=os.getenv('GOOGLE_API_KEY'),
    unity_mcp_path="/path/to/unity-mcp"
)

script_spec = {
    "name": "TestScript",
    "description": "A test script for player movement"
}

script_path = agent.generate_script(script_spec)
print(f"✅ Script generated: {script_path}")
```

### 3. Generate Assets (requires API keys)
```python
# test_assets.py
from ai_game_dev.agents.asset_generator_agent import AssetGeneratorAgent
import os
from dotenv import load_dotenv

load_dotenv()

api_keys = {
    'meshy': os.getenv('MESHY_API_KEY'),
    'suno': os.getenv('SUNO_API_KEY'),
    # ... other keys
}

agent = AssetGeneratorAgent(
    claude_api_key=os.getenv('ANTHROPIC_API_KEY'),
    api_keys=api_keys
)

# Test 3D model generation
spec = {
    'name': 'test_ball',
    'description': 'A simple football/soccer ball',
    'art_style': 'low-poly'
}

# Note: This will consume API credits
model_path = agent.generate_3d_model(spec)
print(f"✅ Model generated: {model_path}")
```

---

## 📊 Expected Outputs

### After Running `simple_football_manager.py`:

```
examples/output/football_manager/
├── game_design_document.json    # Complete GDD (~50-200 KB)
├── GameManager.cs                # Unity script (~5-10 KB)
├── Player.cs                     # Unity script (~3-5 KB)
├── Team.cs                       # Unity script (~3-5 KB)
├── MatchSimulator.cs             # Unity script (~5-10 KB)
├── TransferMarket.cs             # Unity script (~4-8 KB)
├── UIManager.cs                  # Unity script (~5-10 KB)
├── ui_design.json                # UI specifications (~20-50 KB)
└── IMPLEMENTATION_GUIDE.md       # Step-by-step guide (~10-20 KB)
```

### Content Verification

#### 1. Check GDD
```bash
cat examples/output/football_manager/game_design_document.json | jq .

# Should contain:
# - high_level_design
# - systems
# - asset_requirements
# - ui_design
# - development_roadmap
```

#### 2. Check C# Script
```bash
head -20 examples/output/football_manager/GameManager.cs

# Should start with:
# using UnityEngine;
# using System.Collections;
# ...
```

#### 3. Check Implementation Guide
```bash
head -50 examples/output/football_manager/IMPLEMENTATION_GUIDE.md

# Should contain:
# - Game Overview
# - Implementation Steps
# - Unity project setup
# - Asset requirements
```

---

## 🐛 Troubleshooting

### Issue: "Module not found: anthropic"
```bash
# Solution:
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "API Key not valid"
```bash
# Solution:
# 1. Check .env file
cat .env | grep ANTHROPIC_API_KEY

# 2. Verify key starts with 'sk-ant-'
# 3. Regenerate key at https://console.anthropic.com
```

### Issue: "No output files generated"
```bash
# Solution:
# 1. Check for errors in output
python simple_football_manager.py 2>&1 | tee output.log

# 2. Check API response
# 3. Verify write permissions
ls -la examples/output/
```

### Issue: "Unity MCP not connecting"
```bash
# Solution:
# 1. Check Unity MCP is running
cd unity-mcp
python server.py

# 2. Verify port 3000 is available
netstat -an | grep 3000

# 3. Check Unity Editor is open
ps aux | grep Unity
```

### Issue: "Too slow / timeout"
```bash
# Solution:
# 1. Reduce complexity in prompt
# 2. Use smaller max_tokens
# 3. Check internet connection
# 4. Verify API rate limits
```

---

## 📈 Performance Benchmarks

### Expected Timings (with good internet & APIs)

| Task | Time | API Calls |
|------|------|-----------|
| Game Design (GDD) | 30-60s | 1 Claude |
| Generate 6 Scripts | 2-4 min | 6 Gemini/Claude |
| UI Design | 20-40s | 1 Claude |
| Implementation Guide | 10-20s | 1 Claude |
| **Total Simple Example** | **3-6 min** | **~9 calls** |

With Asset Generation:
| Task | Time | API Calls |
|------|------|-----------|
| + 3D Models (3x) | 5-10 min | 3 Meshy |
| + Textures (5x) | 3-5 min | 5 Polyhive |
| + Music (2x) | 2-4 min | 2 Suno |
| + UI Assets (10x) | 5-8 min | 10 Stability |
| **Total with Assets** | **18-33 min** | **~29 calls** |

---

## 🔍 Monitoring & Logs

### View Logs in Real-time
```bash
# All logs
tail -f logs/ai_game_dev.log

# Errors only
tail -f logs/ai_game_dev.log | grep ERROR

# Specific agent
tail -f logs/master_agent.log
```

### Log Levels
```python
# In code:
import logging

logging.debug("Detailed debugging")
logging.info("General information")
logging.warning("Warning message")
logging.error("Error occurred")
```

### Performance Metrics
```bash
# Enable profiling in .env
ENABLE_PROFILING=true

# Run example
python examples/simple_football_manager.py

# Check metrics
cat logs/performance.log

# Should show:
# - API call times
# - File I/O times
# - Agent execution times
```

---

## 🎯 Test Scenarios

### Scenario 1: Complete Football Manager
```bash
cd examples
python simple_football_manager.py

# Verify:
# 1. All files created
# 2. Scripts compile (check syntax)
# 3. GDD is comprehensive
# 4. Implementation guide is clear
```

### Scenario 2: Simple Clicker Game (Fast)
```python
# quick_test.py
from examples.simple_football_manager import SimpleFootballManagerGame

game = SimpleFootballManagerGame()
game.game_concept = """
Simple clicker game:
- Click button to gain points
- Buy upgrades with points
- Simple UI with counter
"""
game.run()
```

### Scenario 3: Custom Game Concept
```bash
# Modify simple_football_manager.py:
# Change game_idea to your concept
# Example: "City builder game with resource management"

python simple_football_manager.py
```

---

## 📋 Pre-Production Checklist

Before using in production:

- [ ] All API keys configured
- [ ] Environment validated (`python test_setup.py`)
- [ ] Simple example runs successfully
- [ ] Output files verified (GDD, scripts, etc.)
- [ ] Unity installed (if using Unity features)
- [ ] Unity MCP tested (if using Unity automation)
- [ ] Logs directory created and writable
- [ ] Backup strategy in place
- [ ] API rate limits understood
- [ ] Cost monitoring enabled

---

## 🚀 Next Steps

### After Successful Testing:

1. **Try More Examples**
   ```bash
   # City builder
   # RPG quest system
   # Puzzle game
   ```

2. **Create Custom Game**
   ```bash
   # Modify example scripts
   # Add your game concept
   # Adjust complexity
   ```

3. **Setup Unity Integration**
   ```bash
   # Install Unity MCP
   # Test Unity automation
   # Build actual game
   ```

4. **Production Deployment**
   ```bash
   # Follow PROJECT_PLAN.md
   # Setup CI/CD
   # Configure monitoring
   ```

---

## 📞 Getting Help

### Resources
- **Main Documentation**: `README.md`
- **Master Plan**: `AI_GAME_DEVELOPMENT_MASTER_PLAN.md`
- **Quick Start**: `QUICK_START_GUIDE.md`
- **Project Plan**: `PROJECT_PLAN.md`

### Support Channels
- GitHub Issues: Report bugs
- GitHub Discussions: Ask questions
- Examples: Check `examples/README.md`

### Common Commands Reference
```bash
# Setup
./setup.sh

# Activate environment
source venv/bin/activate

# Run tests
pytest

# Run example
python examples/simple_football_manager.py

# View logs
tail -f logs/ai_game_dev.log

# Validate setup
python test_setup.py

# Clean cache
rm -rf .cache/*
```

---

## 📊 Success Indicators

### ✅ System is Working If:
1. `test_setup.py` shows all green checks
2. Simple example completes in 3-6 minutes
3. Output directory has 9+ files
4. GDD JSON is valid and comprehensive
5. C# scripts have valid Unity code
6. No errors in logs (warnings OK)

### ⚠️ Needs Attention If:
1. API calls timing out (>2 minutes each)
2. Output files missing
3. Scripts have syntax errors
4. Logs show repeated errors
5. Setup validation fails

### ❌ System Not Ready If:
1. API keys invalid
2. Python version < 3.10
3. Dependencies not installed
4. No output generated
5. Critical errors in logs

---

**🎮 Happy Game Development!**

*This is a living document. Update as system evolves.*
*Last Updated: 2025-11-21*
