# 🎮 Game Examples

Example games that demonstrate the AI Game Development System capabilities.

---

## 📋 Available Examples

### 1. Simple Football Manager (`simple_football_manager.py`)
**Difficulty:** Beginner
**Time:** ~5-10 minutes to generate
**Features:**
- ✅ Complete Game Design Document
- ✅ 6 Unity C# Scripts (GameManager, Player, Team, etc.)
- ✅ Full UI Design Specifications
- ✅ Step-by-step Implementation Guide

**How to run:**
```bash
cd examples
python simple_football_manager.py
```

**Output:**
```
examples/output/football_manager/
├── game_design_document.json
├── GameManager.cs
├── Player.cs
├── Team.cs
├── MatchSimulator.cs
├── TransferMarket.cs
├── UIManager.cs
├── ui_design.json
└── IMPLEMENTATION_GUIDE.md
```

---

## 🚀 Coming Soon

### 2. City Builder Basic
Simple city management game with resource mechanics.

### 3. RPG Quest System
Turn-based RPG with quest and inventory systems.

### 4. Puzzle Game Template
Match-3 style puzzle game with power-ups.

### 5. Tycoon Manager
Business simulation with financial management.

---

## 📖 How to Use Examples

### Step 1: Setup Environment
```bash
# Make sure you've run setup.sh first
cd /home/user/Game-OS
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Set API keys in .env
nano .env
```

### Step 2: Run Example
```bash
cd examples
python simple_football_manager.py
```

### Step 3: Implement in Unity
1. Check `output/<game-name>/IMPLEMENTATION_GUIDE.md`
2. Follow step-by-step instructions
3. Copy scripts to Unity project
4. Build UI based on specifications

---

## 🎯 Example Structure

Each example follows this structure:

```python
class GameExample:
    def create_game_design()       # GDD generation
    def generate_unity_scripts()   # C# scripts
    def generate_ui_design()       # UI specs
    def create_implementation_guide()  # How-to guide
```

---

## 🛠️ Customization

You can modify examples by:

1. **Changing Game Concept:**
   ```python
   game_concept = """
   Your custom game idea here
   """
   ```

2. **Adding More Scripts:**
   ```python
   script_specs.append({
       "name": "YourSystem",
       "description": "What it does"
   })
   ```

3. **Adjusting Complexity:**
   - Simple: 3-5 scripts
   - Medium: 6-10 scripts
   - Complex: 10+ scripts

---

## 📊 Example Comparison

| Example | Scripts | Complexity | Time | Unity Required |
|---------|---------|------------|------|----------------|
| Football Manager | 6 | Medium | 10min | Yes |
| City Builder | 8 | Medium | 15min | Yes |
| RPG Quest | 10 | High | 20min | Yes |
| Puzzle Game | 4 | Low | 5min | Yes |
| Tycoon Manager | 12 | High | 25min | Yes |

---

## 💡 Tips

1. **Start Simple:** Begin with simpler examples to understand the workflow
2. **Iterate:** Run examples multiple times with different prompts
3. **Customize:** Modify the generated code to fit your needs
4. **Learn:** Study the generated scripts to learn Unity patterns

---

## 🐛 Troubleshooting

### Example Fails to Run
```bash
# Check API keys
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Claude:', os.getenv('ANTHROPIC_API_KEY')[:10])"

# Verify dependencies
pip install -r ../requirements.txt
```

### Generated Code Has Errors
- AI-generated code may need minor adjustments
- Check Unity version compatibility
- Review and modify as needed

### Output Directory Issues
```bash
# Create output directory manually
mkdir -p examples/output
```

---

## 📚 Learning Resources

After running examples, learn more:
- Unity Manual: https://docs.unity3d.com/Manual/
- C# Basics: https://learn.microsoft.com/en-us/dotnet/csharp/
- Game Design: ../AI_GAME_DEVELOPMENT_MASTER_PLAN.md

---

## 🤝 Contributing Examples

Want to add your own example? Great!

1. Copy `simple_football_manager.py` as template
2. Modify game concept and specs
3. Test thoroughly
4. Submit PR with:
   - Example script
   - README entry
   - Sample output (if possible)

---

## 📄 License

All examples are MIT Licensed - feel free to use and modify!

---

*Happy Game Creating!* 🎮
