# 🎮 Coplay Integration Guide
## Complete Setup & Usage for AI Game Development System

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage Examples](#usage-examples)
5. [Orchestrator Mode](#orchestrator-mode)
6. [Action Recorder & Pipelines](#action-recorder--pipelines)
7. [Multi-Model AI Strategy](#multi-model-ai-strategy)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

---

## 🎯 Overview

### What is Coplay?

**Coplay** is an AI-powered Unity Editor copilot that enables:
- **Orchestrator Mode**: GDD → Complete Game (95%+ automation)
- **Multi-Model AI**: Switch between 4 AI models (GPT-4, Gemini 2.5, Claude 4, Grok 3)
- **Action Recorder**: Record and replay Unity workflows
- **Unity MCP Integration**: 14 core tools for complete Unity control
- **Built-in Meshy**: Generate 3D models directly in Unity

### Why Coplay for Our Project?

| Feature | Without Coplay | With Coplay |
|---------|---------------|-------------|
| Automation Level | 60-70% | 95-98% |
| GDD → Game Time | 2-4 hours | 15-45 minutes |
| Script Generation | Manual prompts | Orchestrator Mode |
| 3D Asset Generation | External API → Import | Built-in Meshy |
| Reusable Workflows | Manual repetition | Action Pipelines |
| AI Model Flexibility | Single model | 4 models, switchable |

---

## 📦 Installation

### Prerequisites

- ✅ Unity 2021.3 LTS or newer
- ✅ Python 3.10+
- ✅ Node.js 16+
- ✅ Git
- ✅ API Keys (Claude, Gemini, Meshy, etc.)

### Step 1: Install Unity MCP Server

```bash
# Clone the Unity MCP Server (maintained by Coplay)
git clone https://github.com/CoplayDev/unity-mcp.git
cd unity-mcp

# Install dependencies
pip install -r requirements.txt

# Start server (keep this running)
python server.py

# Expected output:
# 🚀 Unity MCP Server started on port 3000
# ✅ Ready to receive connections
```

### Step 2: Install Coplay Unity Plugin

#### Method 1: Auto-Setup (Recommended)

1. Open Unity Editor
2. Download Coplay plugin from: https://github.com/CoplayDev/coplay-unity-plugin
3. Open Unity → `Window → Coplay → Setup Wizard`
4. Click `Next → Install`
5. Wait for installation to complete

#### Method 2: Git URL (Manual)

1. Open Unity Editor
2. Go to `Window → Package Manager`
3. Click `+ → Add package from git URL`
4. Enter: `https://github.com/CoplayDev/coplay-unity-plugin.git#beta`
5. Click `Add`

#### Method 3: OpenUPM

```bash
# Install OpenUPM CLI
npm install -g openupm-cli

# Add Coplay package
openupm add ai.coplay.unity
```

### Step 3: Install Python Integration Layer

```bash
cd /home/user/Game-OS

# Activate virtual environment
source venv/bin/activate

# Install our Coplay integration
# (Already included in requirements.txt)
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# Test Unity MCP connection
python -c "
from ai_game_dev.integrations import CoplayOrchestratorClient, CoplayConfig
import asyncio

async def test():
    config = CoplayConfig(
        unity_project_path='/path/to/test/project',
        mcp_server_url='http://localhost:3000'
    )
    client = CoplayOrchestratorClient(config)
    result = await client.connect_to_unity_mcp()
    print('✅ Coplay integration working!' if result else '❌ Connection failed')

asyncio.run(test())
"
```

---

## ⚙️ Configuration

### 1. Environment Variables

Create/update `.env` file:

```bash
# AI API Keys
ANTHROPIC_API_KEY=sk-ant-your-key-here
GOOGLE_API_KEY=your-gemini-key-here
OPENAI_API_KEY=your-openai-key-here  # For GPT-4
MESHY_API_KEY=your-meshy-key-here

# Unity Configuration
UNITY_PROJECT_PATH=/home/user/Unity/Projects/MyGame
UNITY_MCP_SERVER_URL=http://localhost:3000

# Coplay Settings
COPLAY_DEFAULT_MODEL=claude-sonnet-4-5-20250929
COPLAY_ENABLE_ORCHESTRATOR=true
COPLAY_ENABLE_ACTION_RECORDER=true
COPLAY_VALIDATION_LEVEL=standard  # basic, standard, or strict
```

### 2. Python Configuration

```python
from ai_game_dev.integrations import CoplayConfig, AIModel

config = CoplayConfig(
    # Unity paths
    unity_project_path="/path/to/your/project",
    mcp_server_url="http://localhost:3000",

    # API keys
    claude_api_key=os.getenv('ANTHROPIC_API_KEY'),
    gemini_api_key=os.getenv('GOOGLE_API_KEY'),
    openai_api_key=os.getenv('OPENAI_API_KEY'),
    meshy_api_key=os.getenv('MESHY_API_KEY'),

    # Settings
    default_model=AIModel.CLAUDE_SONNET_4_5,
    enable_orchestrator=True,
    enable_action_recorder=True,
    auto_validate_scripts=True,
    validation_level="standard"
)
```

### 3. Unity Editor Configuration

1. Open Unity → `Window → Coplay → Settings`
2. Configure:
   - **MCP Server URL**: `http://localhost:3000`
   - **Default AI Model**: Claude Sonnet 4.5 (or preferred)
   - **Auto-validate Scripts**: ✅ Enabled
   - **Meshy API Key**: Your Meshy key

---

## 🚀 Usage Examples

### Example 1: Simple Script Generation

```python
import asyncio
import os
from ai_game_dev.integrations import CoplayOrchestratorClient, CoplayConfig, AIModel

async def generate_player_script():
    config = CoplayConfig(
        unity_project_path="/path/to/project",
        claude_api_key=os.getenv('ANTHROPIC_API_KEY')
    )

    client = CoplayOrchestratorClient(config)

    # Connect to Unity
    await client.connect_to_unity_mcp()
    await client.load_unity_project()

    # Generate script
    script_spec = {
        "name": "PlayerController",
        "description": "Player movement with WASD, jump, and camera control",
        "requirements": {
            "movement_speed": 5.0,
            "jump_force": 10.0,
            "camera_sensitivity": 2.0
        }
    }

    script_content = await client._generate_script_with_ai(
        spec=script_spec,
        model=AIModel.CLAUDE_SONNET_4_5
    )

    print(f"✅ Script generated:\n{script_content}")

    await client.close()

# Run
asyncio.run(generate_player_script())
```

### Example 2: Complete Game from GDD

```python
import asyncio
import json
from ai_game_dev.integrations import create_game_from_gdd, CoplayConfig

async def create_football_manager():
    # Load GDD
    with open('examples/output/football_manager/game_design_document.json') as f:
        gdd = json.load(f)

    # Configure
    config = CoplayConfig(
        unity_project_path="/path/to/FootballManager",
        claude_api_key=os.getenv('ANTHROPIC_API_KEY'),
        gemini_api_key=os.getenv('GOOGLE_API_KEY'),
        meshy_api_key=os.getenv('MESHY_API_KEY'),
        default_model=AIModel.GEMINI_2_5_PRO
    )

    # Create game (Orchestrator Mode)
    result = await create_game_from_gdd(gdd, config)

    print(f"""
🎉 Game created successfully!

⏱️  Time: {result['execution_time_seconds']:.1f} seconds
📄 Scripts: {len([f for f in result['files_generated'] if f.endswith('.cs')])}
🎨 Assets: {len(result['assets_generated'])}
🎬 Scenes: {len([f for f in result['files_generated'] if f.endswith('.unity')])}
    """)

# Run
asyncio.run(create_football_manager())
```

### Example 3: Multi-Model Usage

```python
async def multi_model_development():
    config = CoplayConfig(
        unity_project_path="/path/to/project",
        claude_api_key=os.getenv('ANTHROPIC_API_KEY'),
        gemini_api_key=os.getenv('GOOGLE_API_KEY')
    )

    client = CoplayOrchestratorClient(config)
    await client.connect_to_unity_mcp()

    # Use Gemini for bulk script generation (fast)
    await client.switch_ai_model(AIModel.GEMINI_2_0_FLASH)
    scripts = await client._generate_all_scripts(gdd, AIModel.GEMINI_2_0_FLASH)

    # Switch to Claude for precise editing (quality)
    await client.switch_ai_model(AIModel.CLAUDE_SONNET_4_5)
    # ... refine scripts ...

    # Use GPT-4 for complex algorithms (specialized)
    await client.switch_ai_model(AIModel.GPT_4)
    # ... generate AI opponent logic ...

    await client.close()
```

---

## 🎬 Orchestrator Mode

### What is Orchestrator Mode?

Orchestrator Mode executes a **complete multi-step workflow** from Game Design Document to finished game.

### Workflow Steps (Automated)

1. **Project Structure** (2-3 min): Create folders, configure settings
2. **Script Generation** (8-15 min): Generate all C# scripts with multi-model AI
3. **Asset Generation** (5-10 min): Generate 3D models via Meshy
4. **Scene Building** (3-5 min): Create and populate scenes
5. **Prefab Creation** (2-4 min): Convert GameObjects to prefabs
6. **Configuration** (1-2 min): Apply project settings
7. **Validation** (1-3 min): Validate all scripts, compile

**Total Time:** 15-45 minutes (vs 2-4 hours manually)

### Usage Example

```python
async def orchestrator_example():
    config = CoplayConfig(
        unity_project_path="/path/to/project",
        claude_api_key=os.getenv('ANTHROPIC_API_KEY'),
        gemini_api_key=os.getenv('GOOGLE_API_KEY'),
        meshy_api_key=os.getenv('MESHY_API_KEY')
    )

    orchestrator = CoplayOrchestratorClient(config)
    await orchestrator.connect_to_unity_mcp()
    await orchestrator.load_unity_project()

    # Execute Orchestrator Mode
    result = await orchestrator.orchestrator_mode(
        gdd=your_game_design_document,
        model=AIModel.GEMINI_2_5_PRO,
        enable_asset_generation=True
    )

    print(f"✅ Orchestrator completed in {result['execution_time_seconds']:.1f}s")
    print(f"📄 Generated {len(result['files_generated'])} files")
    print(f"🎨 Generated {len(result['assets_generated'])} assets")

    await orchestrator.close()
```

### Orchestrator Mode Output

```json
{
  "success": true,
  "game_title": "Football Manager Pro",
  "steps_completed": [
    "project_structure",
    "script_generation",
    "asset_generation",
    "scene_building",
    "prefab_creation",
    "configuration",
    "validation"
  ],
  "files_generated": [
    "Assets/Scripts/GameManager.cs",
    "Assets/Scripts/PlayerController.cs",
    "Assets/Scripts/TeamManager.cs",
    "Assets/Scenes/MainMenu.unity",
    "Assets/Scenes/Gameplay.unity",
    "Assets/Prefabs/Player.prefab"
  ],
  "assets_generated": [
    "Assets/Models/Stadium.fbx",
    "Assets/Models/Player.fbx",
    "Assets/Models/Ball.fbx"
  ],
  "errors": [],
  "execution_time_seconds": 892.4
}
```

---

## 🎥 Action Recorder & Pipelines

### What are Action Pipelines?

Action Pipelines let you **record Unity workflows** and **replay them** with different parameters.

### Use Cases

- Creating multiple similar characters
- Building UI screens with consistent styling
- Generating terrain variations
- Setting up scene templates

### Recording a Pipeline

```python
async def record_character_pipeline():
    orchestrator = CoplayOrchestratorClient(config)
    await orchestrator.connect_to_unity_mcp()

    # Start recording
    await orchestrator.record_action_pipeline(
        pipeline_name="create_character",
        description="Create character with rigidbody, collider, animator, and stats"
    )

    print("🎬 Recording started - perform actions in Unity Editor...")
    print("   1. Create GameObject")
    print("   2. Add Rigidbody component")
    print("   3. Add Box Collider")
    print("   4. Add Animator")
    print("   5. Create Stats script")
    print("   6. Stop recording in Coplay UI")

    # Recording stops when you click "Stop" in Coplay UI
    # Pipeline is saved automatically
```

### Replaying a Pipeline

```python
async def replay_character_pipeline():
    orchestrator = CoplayOrchestratorClient(config)
    await orchestrator.connect_to_unity_mcp()

    # Replay with different parameters
    characters = [
        {"name": "Warrior", "max_health": 150, "speed": 4.0},
        {"name": "Mage", "max_health": 80, "speed": 3.0},
        {"name": "Rogue", "max_health": 100, "speed": 6.0}
    ]

    for char in characters:
        result = await orchestrator.replay_action_pipeline(
            pipeline_name="create_character",
            parameters={
                "character_name": char["name"],
                "max_health": char["max_health"],
                "movement_speed": char["speed"]
            }
        )

        print(f"✅ Created character: {char['name']}")

    await orchestrator.close()
```

### Pipeline Storage

Pipelines are stored in:
```
YourUnityProject/
└── CoplayPipelines/
    └── create_character.json
```

---

## 🧠 Multi-Model AI Strategy

### When to Use Each Model

| Model | Best For | Speed | Cost | Quality |
|-------|----------|-------|------|---------|
| **GPT-4.1 Turbo** | Complex algorithms, AI opponents | Medium | High | Excellent |
| **Gemini 2.5 Pro** | Bulk script generation, large files | Fast | Medium | Very Good |
| **Claude 4-Sonnet** | Precise editing, debugging, docs | Medium | Medium | Excellent |
| **Grok 3** | Experimental features, creative ideas | Fast | Low | Good |

### Strategy Examples

#### 1. Large Project Strategy

```python
# Phase 1: Project structure with Gemini (fast)
await client.switch_ai_model(AIModel.GEMINI_2_0_FLASH)
await client._create_project_structure(gdd)

# Phase 2: Bulk scripts with Gemini 2.5 Pro
await client.switch_ai_model(AIModel.GEMINI_2_5_PRO)
scripts = await client._generate_all_scripts(gdd, AIModel.GEMINI_2_5_PRO)

# Phase 3: Complex systems with GPT-4
await client.switch_ai_model(AIModel.GPT_4)
ai_script = await client._generate_script_with_ai(ai_opponent_spec, AIModel.GPT_4)

# Phase 4: Refinement with Claude
await client.switch_ai_model(AIModel.CLAUDE_SONNET_4_5)
# ... precise edits and optimizations ...
```

#### 2. Quality-First Strategy

```python
# Use Claude for everything (slower but highest quality)
config = CoplayConfig(
    default_model=AIModel.CLAUDE_SONNET_4_5,
    # ...
)

result = await orchestrator.orchestrator_mode(
    gdd=gdd,
    model=AIModel.CLAUDE_SONNET_4_5
)
```

#### 3. Speed-First Strategy

```python
# Use Gemini 2.0 Flash for everything (fastest)
config = CoplayConfig(
    default_model=AIModel.GEMINI_2_0_FLASH,
    # ...
)

result = await orchestrator.orchestrator_mode(
    gdd=gdd,
    model=AIModel.GEMINI_2_0_FLASH
)
```

---

## 🐛 Troubleshooting

### Issue 1: MCP Server Not Connecting

**Symptoms:**
```
❌ Failed to connect to Unity MCP: Connection refused
```

**Solutions:**
```bash
# 1. Check if server is running
ps aux | grep "python server.py"

# 2. Start server if not running
cd unity-mcp
python server.py

# 3. Check port availability
netstat -an | grep 3000

# 4. Test connection
curl http://localhost:3000/health
```

### Issue 2: Coplay Plugin Not Visible in Unity

**Solutions:**
1. Check Unity version (must be 2021.3+)
2. Reinstall plugin:
   ```
   Unity → Window → Package Manager → Coplay → Remove
   Unity → Package Manager → + → Add from git URL
   ```
3. Check Unity Console for errors
4. Clear Unity cache:
   ```bash
   rm -rf Library/
   # Reopen Unity
   ```

### Issue 3: Script Validation Failing

**Symptoms:**
```
⚠️  PlayerController.cs (validation warnings)
```

**Solutions:**
```python
# 1. Use stricter validation during generation
config = CoplayConfig(
    auto_validate_scripts=True,
    validation_level="strict"  # Changed from "standard"
)

# 2. Check specific validation errors
result = await client.execute_mcp_tool(
    "validate_script",
    {
        "file_path": "Assets/Scripts/PlayerController.cs",
        "validation_level": "strict"
    }
)
print(result)

# 3. Regenerate script with Claude (better quality)
await client.switch_ai_model(AIModel.CLAUDE_SONNET_4_5)
# ... regenerate ...
```

### Issue 4: Orchestrator Mode Timeout

**Symptoms:**
```
⏱️  Orchestrator taking longer than expected...
```

**Solutions:**
```python
# 1. Reduce GDD complexity
# 2. Disable asset generation temporarily
result = await orchestrator.orchestrator_mode(
    gdd=simplified_gdd,
    enable_asset_generation=False  # Skip 3D models
)

# 3. Use faster AI model
await client.switch_ai_model(AIModel.GEMINI_2_0_FLASH)

# 4. Run in smaller batches
# Generate scripts first, then assets separately
```

### Issue 5: Meshy API Quota Exceeded

**Symptoms:**
```
❌ Meshy API error: Quota exceeded
```

**Solutions:**
```python
# 1. Check Meshy quota
# Visit: https://www.meshy.ai/dashboard

# 2. Disable Meshy temporarily
config = CoplayConfig(
    meshy_api_key=None,  # Disable
    # ...
)

# 3. Use placeholder models
# Generate with Meshy later when quota resets
```

---

## ✅ Best Practices

### 1. Project Organization

```
MyUnityProject/
├── Assets/
│   ├── Scripts/          # All C# scripts
│   ├── Scenes/           # Unity scenes
│   ├── Prefabs/          # Reusable prefabs
│   ├── Models/           # 3D models (Meshy)
│   ├── Materials/        # Materials and textures
│   ├── Audio/            # Music and SFX
│   └── UI/               # UI assets
├── CoplayPipelines/      # Saved action pipelines
└── Logs/                 # Coplay logs
```

### 2. GDD Structure

Ensure your GDD includes:
```json
{
  "title": "Game Title",
  "high_level_design": {
    "game_overview": "...",
    "core_mechanics": ["..."],
    "target_audience": "..."
  },
  "systems": [
    {
      "name": "PlayerMovement",
      "description": "...",
      "requirements": {...}
    }
  ],
  "technical_requirements": {
    "scripts": [...],
    "scenes": [...],
    "prefabs": [...],
    "project_settings": {...}
  },
  "asset_requirements": {
    "3d_models": [...],
    "textures": [...],
    "audio": [...]
  }
}
```

### 3. Validation Levels

- **basic**: Fast validation, syntax only
- **standard**: Moderate validation, common errors (recommended)
- **strict**: Full validation, all warnings treated as errors

### 4. Model Selection Guide

```python
# For your specific task:

# Simple CRUD scripts → Gemini 2.0 Flash
# Complex game systems → GPT-4 or Claude Sonnet
# Debugging/optimization → Claude Sonnet
# Creative/experimental → Grok 3
# Bulk generation → Gemini 2.5 Pro
```

### 5. Cost Optimization

```python
# Strategy: Use cheaper models for bulk, expensive for quality

# 1. Project structure (free - MCP only)
# 2. Bulk scripts → Gemini 2.0 Flash (cheap)
# 3. Complex logic → GPT-4 (expensive but worth it)
# 4. Refinement → Claude Sonnet (medium cost)
# 5. Validation (free - Unity compiler)
```

### 6. Iterative Development

```python
# Don't generate everything at once
# Use iterative approach:

# Iteration 1: Core systems only
gdd_core = extract_core_systems(full_gdd)
result = await orchestrator.orchestrator_mode(gdd_core)

# Iteration 2: Add gameplay features
# Iteration 3: Add UI/UX
# Iteration 4: Add polish and assets
```

---

## 📚 Additional Resources

### Documentation
- **Coplay Docs**: https://docs.coplay.dev
- **Unity MCP Docs**: https://github.com/CoplayDev/unity-mcp/wiki
- **Our Complete Analysis**: `COPLAY_COMPLETE_ANALYSIS.md`

### Community
- **Coplay Discord**: https://discord.gg/coplay
- **GitHub Issues**: https://github.com/CoplayDev/coplay-unity-plugin/issues

### API References
- **Claude API**: https://docs.anthropic.com/
- **Gemini API**: https://ai.google.dev/docs
- **Meshy API**: https://docs.meshy.ai/

---

## 📝 Summary

Coplay integration provides:
- ✅ **95%+ automation** (up from 60-70%)
- ✅ **15-45 minute** game creation (vs 2-4 hours)
- ✅ **Multi-model AI** flexibility
- ✅ **Action Pipelines** for reusability
- ✅ **Built-in Meshy** for 3D assets
- ✅ **Complete Unity control** via MCP

**Next Steps:**
1. Complete installation following this guide
2. Run example: `python examples/simple_football_manager.py`
3. Create your first game with Orchestrator Mode
4. Experiment with Action Pipelines
5. Build production-ready games!

---

**Happy Game Creating with Coplay! 🎮🚀**

*Last Updated: 2025-11-21*
