#!/usr/bin/env python3
"""
Simple Football Manager Game - Coplay Orchestrator Mode
Creates a complete football management simulation game using Coplay AI

This version uses:
- Coplay Orchestrator Mode (GDD → Complete Game)
- Multi-Model AI (Claude for GDD, Gemini for scripts)
- Built-in Meshy for 3D assets
- Action Pipelines for reusable workflows

Time: ~15-25 minutes (vs 30-60 minutes with manual approach)
"""

import os
import sys
import json
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
import anthropic

from ai_game_dev.integrations import (
    CoplayOrchestratorClient,
    CoplayConfig,
    AIModel,
    create_game_from_gdd_sync
)

# Load environment variables
load_dotenv()


class FootballManagerGameCoplay:
    """
    Creates a football manager game using Coplay Orchestrator Mode

    Features:
    - Automated GDD creation with Claude
    - Orchestrator Mode execution (GDD → Complete Game)
    - Multi-model AI (Claude + Gemini)
    - Built-in Meshy 3D generation
    - ~95% automation
    """

    def __init__(self):
        self.claude_key = os.getenv('ANTHROPIC_API_KEY')
        self.gemini_key = os.getenv('GOOGLE_API_KEY')
        self.meshy_key = os.getenv('MESHY_API_KEY')
        self.unity_project_path = os.getenv('UNITY_PROJECT_PATH', '/home/user/Unity/Projects/FootballManager')

        if not self.claude_key or self.claude_key.startswith('your-'):
            raise ValueError("Please set ANTHROPIC_API_KEY in .env file")

        if not self.gemini_key or self.gemini_key.startswith('your-'):
            print("⚠️  Warning: GOOGLE_API_KEY not set. Multi-model features disabled.")
            self.gemini_key = None

        self.claude_client = anthropic.Anthropic(api_key=self.claude_key)
        self.output_dir = Path(__file__).parent / "output" / "football_manager"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_game_design(self):
        """Step 1: Create Game Design Document with Claude"""

        print("\n" + "="*70)
        print("🎮 FOOTBALL MANAGER GAME - COPLAY ORCHESTRATOR MODE")
        print("="*70)
        print("\n📋 Step 1/3: Generating Game Design Document with Claude...")

        game_concept = """
        Create a simple Football Manager game with these features:

        CORE MECHANICS:
        - Manage a football team (players, tactics, training)
        - Play matches (simplified simulation)
        - Transfer market (buy/sell players)
        - Budget management
        - League table and standings

        SCOPE:
        - Single player only
        - 1 league with 10 teams
        - Simple 2D UI
        - Turn-based (week by week)
        - Basic player stats (Speed, Shooting, Defense, Overall Rating)

        TARGET:
        - Desktop (Windows/Mac/Linux)
        - Unity 2021.3 LTS
        - Low-poly art style
        - Development time: 1 day with Coplay Orchestrator

        SYSTEMS NEEDED:
        1. Team Management System
        2. Match Simulation System
        3. Player Database System
        4. Transfer Market System
        5. UI/UX System
        6. Save/Load System
        """

        prompt = f"""{game_concept}

Create a comprehensive Game Design Document in JSON format with:

1. **high_level_design**
   - game_overview (string)
   - core_loop (string)
   - target_audience (string)
   - unique_selling_points (array)

2. **systems** (array of objects)
   Each system should have:
   - name (string)
   - description (string)
   - requirements (object with details)

3. **technical_requirements** (object)
   - scripts (array of objects with name, description, requirements)
   - scenes (array of objects with name, description)
   - prefabs (array of objects with name, description, components)
   - project_settings (object)

4. **asset_requirements** (object)
   - 3d_models (array with name, description, art_style)
   - textures (array)
   - audio (array with music and sfx)
   - ui (array)

5. **development_roadmap** (array of phases)

Output ONLY valid JSON, no markdown formatting."""

        response = self.claude_client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=8000,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )

        gdd_text = response.content[0].text

        # Parse JSON
        try:
            if "```json" in gdd_text:
                json_start = gdd_text.find("```json") + 7
                json_end = gdd_text.find("```", json_start)
                gdd_text = gdd_text[json_start:json_end].strip()

            gdd = json.loads(gdd_text)
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON parsing error: {e}")
            print("Saving as raw content...")
            gdd = {
                "title": "Football Manager",
                "raw_content": gdd_text,
                "high_level_design": {"game_overview": "Football management simulation"},
                "systems": [],
                "technical_requirements": {
                    "scripts": [
                        {"name": "GameManager", "description": "Main game controller"},
                        {"name": "PlayerController", "description": "Player data model"},
                        {"name": "TeamManager", "description": "Team management logic"},
                        {"name": "MatchSimulator", "description": "Match simulation engine"},
                        {"name": "TransferMarket", "description": "Transfer market system"},
                        {"name": "UIManager", "description": "UI controller"}
                    ],
                    "scenes": [
                        {"name": "MainMenu", "description": "Main menu scene"},
                        {"name": "TeamManagement", "description": "Team management screen"},
                        {"name": "MatchDay", "description": "Match simulation screen"}
                    ],
                    "prefabs": []
                },
                "asset_requirements": {
                    "3d_models": [
                        {"name": "Stadium", "description": "Football stadium model", "art_style": "low-poly"},
                        {"name": "Player", "description": "Player character model", "art_style": "low-poly"},
                        {"name": "Ball", "description": "Football/soccer ball", "art_style": "low-poly"}
                    ]
                }
            }

        # Save GDD
        gdd_path = self.output_dir / "game_design_document.json"
        with open(gdd_path, 'w', encoding='utf-8') as f:
            json.dump(gdd, f, indent=2, ensure_ascii=False)

        print(f"✅ Game Design Document created: {gdd_path}")
        print(f"   Title: {gdd.get('title', 'Football Manager')}")
        print(f"   Systems: {len(gdd.get('systems', []))}")
        print(f"   Scripts: {len(gdd.get('technical_requirements', {}).get('scripts', []))}")

        return gdd

    async def execute_orchestrator_mode(self, gdd):
        """Step 2: Execute Coplay Orchestrator Mode (GDD → Complete Game)"""

        print("\n🚀 Step 2/3: Executing Coplay Orchestrator Mode...")
        print("   This will create the complete Unity project automatically!")
        print()

        # Configure Coplay
        config = CoplayConfig(
            unity_project_path=self.unity_project_path,
            mcp_server_url="http://localhost:3000",
            claude_api_key=self.claude_key,
            gemini_api_key=self.gemini_key,
            meshy_api_key=self.meshy_key,
            default_model=AIModel.GEMINI_2_5_PRO,  # Use Gemini for bulk generation
            enable_orchestrator=True,
            enable_action_recorder=True,
            auto_validate_scripts=True,
            validation_level="standard"
        )

        # Create orchestrator client
        orchestrator = CoplayOrchestratorClient(config)

        try:
            # Connect to Unity MCP
            print("🔌 Connecting to Unity MCP Server...")
            connected = await orchestrator.connect_to_unity_mcp()
            if not connected:
                print("❌ Failed to connect to Unity MCP Server")
                print("   Make sure Unity MCP is running: python unity-mcp/server.py")
                return None

            # Load Unity project
            print(f"📂 Loading Unity project: {self.unity_project_path}")
            loaded = await orchestrator.load_unity_project()
            if not loaded:
                print("⚠️  Unity project not loaded, continuing anyway...")

            # Execute Orchestrator Mode
            print("\n🎬 Starting Orchestrator Mode...")
            print("   Expected time: 15-25 minutes")
            print()

            enable_assets = self.meshy_key is not None
            if not enable_assets:
                print("   ⚠️  Meshy API key not set - skipping 3D asset generation")

            result = await orchestrator.orchestrator_mode(
                gdd=gdd,
                model=AIModel.GEMINI_2_5_PRO,
                enable_asset_generation=enable_assets
            )

            return result

        finally:
            await orchestrator.close()

    def create_implementation_guide(self, gdd, orchestrator_result):
        """Step 3: Create implementation guide based on orchestrator results"""

        print("\n📝 Step 3/3: Creating Implementation Guide...")

        if not orchestrator_result or not orchestrator_result.get('success'):
            print("⚠️  Orchestrator did not complete successfully")
            guide_content = f"""# Football Manager Game - Implementation Guide

## ⚠️ Orchestrator Mode Issue

The Coplay Orchestrator did not complete successfully.

### Troubleshooting Steps:

1. **Check Unity MCP Server**
   ```bash
   cd unity-mcp
   python server.py
   ```

2. **Verify Unity Editor is Open**
   - Open Unity Hub
   - Open project: {self.unity_project_path}

3. **Check Coplay Plugin Installed**
   - Unity → Window → Coplay
   - If not found, install from Package Manager

4. **Review Errors**
   ```python
   # Check orchestrator result:
   {json.dumps(orchestrator_result, indent=2)}
   ```

5. **Manual Fallback**
   Run the original example:
   ```bash
   python examples/simple_football_manager.py
   ```

### Next Steps:

Once issues are resolved, re-run:
```bash
python examples/simple_football_manager_coplay.py
```
"""
        else:
            execution_time = orchestrator_result['execution_time_seconds']
            scripts_count = len([f for f in orchestrator_result['files_generated'] if f.endswith('.cs')])
            assets_count = len(orchestrator_result['assets_generated'])
            scenes_count = len([f for f in orchestrator_result['files_generated'] if f.endswith('.unity')])

            guide_content = f"""# Football Manager Game - Implementation Guide
**Generated with Coplay Orchestrator Mode**

---

## 🎉 Generation Complete!

**Execution Time:** {execution_time:.1f} seconds ({execution_time/60:.1f} minutes)

**Generated Files:**
- 📄 C# Scripts: {scripts_count}
- 🎨 3D Assets: {assets_count}
- 🎬 Unity Scenes: {scenes_count}
- 🧩 Prefabs: {len([f for f in orchestrator_result['files_generated'] if f.endswith('.prefab')])}

---

## 📁 Project Location

```
{self.unity_project_path}/
├── Assets/
│   ├── Scripts/        ({scripts_count} files)
│   ├── Scenes/         ({scenes_count} files)
│   ├── Models/         ({assets_count} files)
│   ├── Prefabs/
│   └── UI/
```

---

## 📄 Generated Scripts

"""
            for file in orchestrator_result['files_generated']:
                if file.endswith('.cs'):
                    guide_content += f"- `{file}`\n"

            guide_content += f"""
---

## 🎨 Generated Assets

"""
            for asset in orchestrator_result['assets_generated']:
                guide_content += f"- `{asset}`\n"

            guide_content += f"""
---

## 🎬 Generated Scenes

"""
            for file in orchestrator_result['files_generated']:
                if file.endswith('.unity'):
                    guide_content += f"- `{file}`\n"

            guide_content += f"""
---

## ✅ Next Steps

### 1. Open in Unity

```bash
# If not already open
unity-hub --projectPath "{self.unity_project_path}"
```

### 2. Verify Compilation

1. Open Unity Editor
2. Check Console for errors
3. All scripts should compile successfully

### 3. Test the Game

1. Open scene: `Assets/Scenes/MainMenu.unity`
2. Click Play button
3. Test core features:
   - Main menu navigation
   - Team management screen
   - Match simulation
   - Transfer market

### 4. Customize

All generated code can be customized:
- Tweak player stats in `PlayerController.cs`
- Adjust match simulation in `MatchSimulator.cs`
- Modify UI in `UIManager.cs`

### 5. Build for Distribution

```bash
# Build from Unity
File → Build Settings → Build

# Or use command line
unity -quit -batchmode -projectPath "{self.unity_project_path}" -buildWindows64Player "Builds/FootballManager.exe"
```

---

## 🔄 Reusable Pipelines

Action Pipelines were recorded during generation. You can replay them:

```python
from ai_game_dev.integrations import CoplayOrchestratorClient, CoplayConfig

async def replay():
    config = CoplayConfig(unity_project_path="{self.unity_project_path}")
    client = CoplayOrchestratorClient(config)
    await client.connect_to_unity_mcp()

    # Replay character creation pipeline
    await client.replay_action_pipeline(
        pipeline_name="create_player_character",
        parameters={{"name": "NewPlayer", "rating": 85}}
    )
```

---

## 📊 Performance Stats

| Metric | Value |
|--------|-------|
| Total Time | {execution_time:.1f}s ({execution_time/60:.1f} min) |
| Scripts Generated | {scripts_count} |
| Assets Generated | {assets_count} |
| Automation Level | 95%+ |

**Comparison with Manual Development:**
- Manual coding: ~2-4 hours
- Coplay Orchestrator: {execution_time/60:.1f} minutes
- **Time saved: ~{((180 - execution_time/60) / 180 * 100):.0f}%**

---

## 🐛 Troubleshooting

### Scripts Not Compiling

```bash
# Check validation results
# Most issues auto-fixed by Coplay during generation
# If issues persist, regenerate specific script:

# In Unity → Coplay → Regenerate Script
```

### Missing Assets

```bash
# If 3D models missing (Meshy quota exceeded)
# Use placeholder models temporarily:
# Unity → GameObject → 3D Object → Cube (as placeholder)
```

### Performance Issues

```bash
# Optimize generated code:
# Unity → Coplay → Ask AI
# Prompt: "Optimize PlayerController.cs for better performance"
```

---

## 🚀 Advanced Features

### Add Multiplayer

```bash
# Use Coplay to add multiplayer:
# Unity → Coplay → Orchestrator Mode
# Prompt: "Add Unity Netcode multiplayer to existing game"
```

### Add Achievements

```bash
# Unity → Coplay → Generate Script
# Prompt: "Create AchievementSystem.cs with Steam integration"
```

### Polish & Effects

```bash
# Unity → Coplay → Action Recorder
# Record: Adding particle effects to goals
# Replay: Apply to all goal scenarios
```

---

## 📚 Resources

- **Coplay Docs**: https://docs.coplay.dev
- **Our Integration Guide**: `COPLAY_INTEGRATION.md`
- **Full Analysis**: `COPLAY_COMPLETE_ANALYSIS.md`

---

**Generated by AI Game Development System + Coplay**
*Time to create: {execution_time/60:.1f} minutes* ⚡
"""

        guide_path = self.output_dir / "IMPLEMENTATION_GUIDE.md"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)

        print(f"✅ Implementation Guide created: {guide_path}")

        return guide_path

    def run_sync(self):
        """Run the complete game creation process (synchronous wrapper)"""

        try:
            # Step 1: Design with Claude
            gdd = self.create_game_design()

            # Step 2: Orchestrator Mode (async)
            print("\n💡 TIP: Make sure Unity MCP Server is running:")
            print("   cd unity-mcp && python server.py")
            print()

            try:
                orchestrator_result = asyncio.run(self.execute_orchestrator_mode(gdd))
            except Exception as e:
                print(f"\n⚠️  Orchestrator Mode failed: {e}")
                print("   Continuing with guide generation...")
                orchestrator_result = {"success": False, "error": str(e)}

            # Step 3: Implementation Guide
            guide = self.create_implementation_guide(gdd, orchestrator_result)

            # Summary
            print("\n" + "="*70)
            if orchestrator_result and orchestrator_result.get('success'):
                print("🎉 GAME CREATION COMPLETE!")
            else:
                print("⚠️  GAME CREATION INCOMPLETE")
            print("="*70)
            print(f"\n📁 All files saved to: {self.output_dir}")
            print(f"\n📄 Files created:")
            print(f"   - game_design_document.json")
            if orchestrator_result and orchestrator_result.get('success'):
                scripts_count = len([f for f in orchestrator_result['files_generated'] if f.endswith('.cs')])
                print(f"   - {scripts_count} C# scripts (in Unity project)")
                print(f"   - {len(orchestrator_result['assets_generated'])} 3D assets (in Unity project)")
            print(f"   - IMPLEMENTATION_GUIDE.md")
            print(f"\n📖 Next: Read {guide} for implementation steps")

            if orchestrator_result and orchestrator_result.get('success'):
                print(f"\n⏱️  Total time: {orchestrator_result['execution_time_seconds']/60:.1f} minutes")
                print(f"🚀 Unity project ready at: {self.unity_project_path}")

            print("="*70)

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    print("="*70)
    print("🎮 FOOTBALL MANAGER GAME - COPLAY ORCHESTRATOR MODE")
    print("="*70)
    print("\nThis will create a complete game using Coplay automation:")
    print("  1. Generate GDD with Claude (30-60 seconds)")
    print("  2. Execute Orchestrator Mode (15-25 minutes)")
    print("  3. Create implementation guide (10 seconds)")
    print()
    print("Total time: ~15-30 minutes")
    print()
    print("Requirements:")
    print("  ✅ Unity MCP Server running (python unity-mcp/server.py)")
    print("  ✅ Unity Editor open")
    print("  ✅ Coplay Plugin installed in Unity")
    print("  ✅ API keys configured in .env")
    print()

    response = input("Ready to start? (y/n): ")

    if response.lower() == 'y':
        game = FootballManagerGameCoplay()
        game.run_sync()
    else:
        print("Cancelled.")
