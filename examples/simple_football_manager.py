#!/usr/bin/env python3
"""
Simple Football Manager Game - Example
Creates a basic football management simulation game using AI agents
"""

import os
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()

class SimpleFootballManagerGame:
    """
    Creates a simple football manager game using Claude AI
    """

    def __init__(self):
        self.claude_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.claude_key or self.claude_key.startswith('your-'):
            raise ValueError("Please set ANTHROPIC_API_KEY in .env file")

        self.client = anthropic.Anthropic(api_key=self.claude_key)
        self.output_dir = Path(__file__).parent / "output" / "football_manager"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_game_design(self):
        """Step 1: Create Game Design Document"""

        print("\n" + "="*60)
        print("🎮 CREATING FOOTBALL MANAGER GAME")
        print("="*60)
        print("\n📋 Step 1: Generating Game Design Document...")

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
        - Development time: 1-2 weeks with AI

        SYSTEMS NEEDED:
        1. Team Management System
        2. Match Simulation System
        3. Player Database System
        4. Transfer Market System
        5. UI/UX System
        6. Save/Load System
        """

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=8000,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": f"""{game_concept}

Create a comprehensive Game Design Document with:

1. **High-Level Design**
   - Game Overview
   - Target Audience
   - Core Loop
   - Unique Selling Points

2. **Game Systems** (detailed)
   - Team Management
   - Match Simulation
   - Player Stats & Growth
   - Transfer Market
   - Financial System

3. **Technical Requirements**
   - Unity Components needed
   - C# Scripts list (with descriptions)
   - Database structure
   - UI screens layout

4. **Asset Requirements**
   - 3D Models (if any)
   - 2D Sprites/UI
   - Audio (Music + SFX)
   - Fonts & Icons

5. **Development Roadmap**
   - Phase breakdown
   - Estimated timeline

Output in detailed JSON format."""
            }]
        )

        gdd_text = response.content[0].text

        # Try to parse JSON
        try:
            # Extract JSON from markdown if present
            if "```json" in gdd_text:
                json_start = gdd_text.find("```json") + 7
                json_end = gdd_text.find("```", json_start)
                gdd_text = gdd_text[json_start:json_end].strip()

            gdd = json.loads(gdd_text)
        except json.JSONDecodeError:
            print("⚠️  Could not parse as JSON, saving as text...")
            gdd = {"raw_content": gdd_text}

        # Save GDD
        gdd_path = self.output_dir / "game_design_document.json"
        with open(gdd_path, 'w', encoding='utf-8') as f:
            json.dump(gdd, f, indent=2, ensure_ascii=False)

        print(f"✅ Game Design Document created: {gdd_path}")

        return gdd

    def generate_unity_scripts(self, gdd):
        """Step 2: Generate Unity C# Scripts"""

        print("\n💻 Step 2: Generating Unity C# Scripts...")

        scripts = []

        # List of scripts to generate
        script_specs = [
            {
                "name": "GameManager",
                "description": "Main game manager, handles game state, week progression, save/load"
            },
            {
                "name": "Player",
                "description": "Player data model with stats (Speed, Shooting, Defense, Overall)"
            },
            {
                "name": "Team",
                "description": "Team class with player list, tactics, budget"
            },
            {
                "name": "MatchSimulator",
                "description": "Simulates match based on team stats and tactics"
            },
            {
                "name": "TransferMarket",
                "description": "Handles buying/selling players, price calculation"
            },
            {
                "name": "UIManager",
                "description": "Manages UI screens, button clicks, data display"
            }
        ]

        for spec in script_specs:
            print(f"   Generating {spec['name']}.cs...")

            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=4000,
                temperature=0.6,
                messages=[{
                    "role": "user",
                    "content": f"""Generate a complete Unity C# script for:

**Name:** {spec['name']}
**Purpose:** {spec['description']}

**Requirements:**
- Follow Unity best practices
- Include XML documentation comments
- Use proper naming conventions
- Include basic error handling
- Make it production-ready

**Game Context:**
Simple Football Manager game - {gdd.get('high_level_design', {}).get('game_overview', 'Team management simulation')}

Output ONLY the C# code, no markdown formatting."""
                }]
            )

            script_content = response.content[0].text

            # Remove markdown code blocks if present
            if "```csharp" in script_content:
                script_content = script_content.split("```csharp")[1].split("```")[0].strip()
            elif "```" in script_content:
                script_content = script_content.split("```")[1].split("```")[0].strip()

            # Save script
            script_path = self.output_dir / f"{spec['name']}.cs"
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)

            scripts.append({
                "name": spec['name'],
                "path": str(script_path),
                "description": spec['description']
            })

            print(f"   ✅ {spec['name']}.cs created")

        print(f"\n✅ Generated {len(scripts)} C# scripts!")

        return scripts

    def generate_ui_design(self, gdd):
        """Step 3: Generate UI Design Specifications"""

        print("\n🎨 Step 3: Generating UI Design...")

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            temperature=0.8,
            messages=[{
                "role": "user",
                "content": f"""Design the UI for this Football Manager game:

{json.dumps(gdd.get('high_level_design', {}), indent=2)}

Create specifications for these screens:

1. **Main Menu**
   - New Game button
   - Load Game button
   - Settings button
   - Quit button

2. **Team Management Screen**
   - Player list (scrollable)
   - Player stats display
   - Tactics selector
   - Training button

3. **Match Day Screen**
   - Opponent info
   - Your team display
   - Play Match button
   - Result display

4. **Transfer Market Screen**
   - Available players list
   - Buy/Sell buttons
   - Budget display
   - Player search/filter

5. **League Table Screen**
   - Team rankings
   - Points, goals, etc.
   - Your team highlighted

For each screen, specify:
- Layout (grid positions)
- UI elements (buttons, text, panels)
- Colors (hex codes)
- Fonts
- Interactions

Output in detailed JSON format."""
            }]
        )

        ui_text = response.content[0].text

        try:
            if "```json" in ui_text:
                json_start = ui_text.find("```json") + 7
                json_end = ui_text.find("```", json_start)
                ui_text = ui_text[json_start:json_end].strip()

            ui_design = json.loads(ui_text)
        except json.JSONDecodeError:
            ui_design = {"raw_content": ui_text}

        # Save UI design
        ui_path = self.output_dir / "ui_design.json"
        with open(ui_path, 'w', encoding='utf-8') as f:
            json.dump(ui_design, f, indent=2, ensure_ascii=False)

        print(f"✅ UI Design created: {ui_path}")

        return ui_design

    def create_implementation_guide(self, gdd, scripts, ui_design):
        """Step 4: Create step-by-step implementation guide"""

        print("\n📝 Step 4: Creating Implementation Guide...")

        guide_content = f"""# Football Manager Game - Implementation Guide

## 🎮 Game Overview

{gdd.get('high_level_design', {}).get('game_overview', 'Simple Football Manager simulation')}

## 📁 Generated Files

### Game Design
- `game_design_document.json` - Full GDD

### Scripts ({len(scripts)} files)
"""

        for script in scripts:
            guide_content += f"- `{script['name']}.cs` - {script['description']}\n"

        guide_content += """
### UI Design
- `ui_design.json` - Complete UI specifications

## 🚀 Implementation Steps

### Step 1: Create Unity Project
1. Open Unity Hub
2. Create New Project:
   - Name: "FootballManagerAI"
   - Template: 3D
   - Version: Unity 2021.3 LTS
3. Create folder structure:
   ```
   Assets/
   ├── Scripts/
   ├── Scenes/
   ├── UI/
   ├── Data/
   └── Resources/
   ```

### Step 2: Import Scripts
1. Copy all `.cs` files to `Assets/Scripts/`
2. Wait for Unity to compile
3. Check Console for errors

### Step 3: Create UI
Follow `ui_design.json` to create:
1. Main Menu scene
2. Game screens (Team Management, Match, etc.)
3. Apply colors and layout

### Step 4: Setup Game Manager
1. Create empty GameObject: "GameManager"
2. Attach `GameManager.cs` script
3. Configure inspector properties

### Step 5: Create Sample Data
1. Create ScriptableObjects for Players
2. Add initial teams
3. Setup league structure

### Step 6: Connect UI to Logic
1. Wire up button onClick events
2. Connect UI elements to UIManager
3. Test each screen

### Step 7: Test & Iterate
1. Play test basic flow
2. Fix bugs
3. Balance gameplay
4. Polish UI

## 🎯 Next Steps

To complete the game:
1. Generate player portraits (use Stability AI API)
2. Add sound effects (use ElevenLabs API)
3. Add background music (use Suno AI API)
4. Create team logos (use Stability AI API)
5. Build for target platform
6. Upload to Steam (optional)

## 📦 Required Unity Packages
- TextMeshPro (for better text)
- Unity UI (included)
- JSON .NET (for save/load)

## 🐛 Common Issues

### Scripts not compiling
- Check for missing namespaces
- Verify Unity version compatibility
- Check Console for specific errors

### UI not displaying
- Check Canvas render mode
- Verify EventSystem exists
- Check Z-ordering

## 🎨 Art Assets Needed

See `game_design_document.json` -> `asset_requirements` for full list.

Can be generated using:
- 3D Models: Meshy AI
- 2D UI: Stability AI
- Icons: Leonardo AI
- Music: Suno AI
- SFX: ElevenLabs

---

**Generated by AI Game Development System**
*Happy Coding!* 🚀
"""

        guide_path = self.output_dir / "IMPLEMENTATION_GUIDE.md"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)

        print(f"✅ Implementation Guide created: {guide_path}")

        return guide_path

    def run(self):
        """Run the complete game creation process"""

        try:
            # Step 1: Design
            gdd = self.create_game_design()

            # Step 2: Generate Scripts
            scripts = self.generate_unity_scripts(gdd)

            # Step 3: Design UI
            ui_design = self.generate_ui_design(gdd)

            # Step 4: Implementation Guide
            guide = self.create_implementation_guide(gdd, scripts, ui_design)

            # Summary
            print("\n" + "="*60)
            print("🎉 GAME CREATION COMPLETE!")
            print("="*60)
            print(f"\n📁 All files saved to: {self.output_dir}")
            print(f"\n📄 Files created:")
            print(f"   - game_design_document.json")
            print(f"   - {len(scripts)} C# scripts")
            print(f"   - ui_design.json")
            print(f"   - IMPLEMENTATION_GUIDE.md")
            print(f"\n📖 Next: Read {guide} for implementation steps")
            print("="*60)

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    print("="*60)
    print("🎮 SIMPLE FOOTBALL MANAGER GAME GENERATOR")
    print("="*60)
    print("\nThis will create a complete game design + Unity scripts")
    print("using Claude AI.\n")

    input("Press Enter to start...")

    game = SimpleFootballManagerGame()
    game.run()
