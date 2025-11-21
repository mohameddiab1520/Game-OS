# 🚀 دليل البدء السريع - AI Game Development System

## ⚡ ابدأ في 30 دقيقة!

---

## ✅ المتطلبات الأساسية

### 1. Software
- [ ] Python 3.10 أو أحدث
- [ ] Unity Hub + Unity 2021.3 LTS
- [ ] Git
- [ ] Node.js 16+ (لـ Unity MCP)

### 2. API Keys (سجل في هذه المواقع)
- [ ] Claude API: https://console.anthropic.com
- [ ] Gemini API: https://aistudio.google.com/app/apikey
- [ ] Meshy AI: https://www.meshy.ai
- [ ] Suno AI: https://sunoapi.org
- [ ] ElevenLabs: https://elevenlabs.io
- [ ] Stability AI: https://platform.stability.ai

---

## 📦 خطوة 1: التثبيت (10 دقائق)

### 1.1 Clone المشروع
```bash
cd /home/user
git clone https://github.com/justinpbarnett/unity-mcp.git
cd unity-mcp
```

### 1.2 تثبيت Python Dependencies
```bash
# إنشاء Virtual Environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate  # Windows

# تثبيت المكتبات
pip install anthropic google-generativeai requests python-dotenv
pip install elevenlabs
pip install -r requirements.txt  # من unity-mcp
```

### 1.3 إعداد Unity
```bash
# تحميل Unity Hub
# Linux
wget https://public-cdn.cloud.unity3d.com/hub/prod/UnityHub.AppImage
chmod +x UnityHub.AppImage
./UnityHub.AppImage

# أو من الموقع: https://unity.com/download

# تثبيت Unity 2021.3 LTS من Unity Hub
```

---

## 🔑 خطوة 2: إعداد API Keys (5 دقائق)

### 2.1 إنشاء ملف .env
```bash
cd /home/user/Game-OS
touch .env
```

### 2.2 إضافة API Keys
```bash
# .env file
ANTHROPIC_API_KEY=sk-ant-your-key-here
GOOGLE_API_KEY=your-gemini-key-here
MESHY_API_KEY=your-meshy-key-here
SUNO_API_KEY=your-suno-key-here
ELEVENLABS_API_KEY=your-elevenlabs-key-here
STABILITY_API_KEY=your-stability-key-here
POLYHIVE_API_KEY=your-polyhive-key-here

# Unity paths
UNITY_PROJECT_PATH=/home/user/Unity/Projects
UNITY_MCP_PATH=/home/user/unity-mcp

# Steam (optional for now)
STEAM_USERNAME=your-steam-username
STEAM_PASSWORD=your-steam-password
```

---

## 🎮 خطوة 3: Test Run - لعبة بسيطة! (15 دقائق)

### 3.1 إنشاء Test Script
```bash
cd /home/user/Game-OS
nano test_simple_game.py
```

```python
# test_simple_game.py
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def create_simple_game_concept():
    """اختبار بسيط - إنشاء مفهوم لعبة"""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": """أنا أريد لعبة بسيطة للاختبار:

النوع: Clicker Game بسيط
الفكرة: لعبة إدارة نادي كرة قدم مبسطة
المميزات:
- زر لتدريب اللاعبين (يزيد النقاط)
- زر لشراء لاعبين جدد
- عداد للنقاط
- UI بسيط

قم بإنشاء:
1. Game Design Document مختصر
2. قائمة بالـ Scripts المطلوبة (C#)
3. قائمة بالـ UI Elements
4. قائمة بالـ Assets المطلوبة

Output in JSON format."""
        }]
    )

    print("="*60)
    print("🎮 SIMPLE GAME CONCEPT")
    print("="*60)
    print(response.content[0].text)
    print("="*60)

    return response.content[0].text

if __name__ == "__main__":
    concept = create_simple_game_concept()
```

### 3.2 تشغيل الاختبار
```bash
python test_simple_game.py
```

---

## 🏗️ خطوة 4: إعداد Unity MCP

### 4.1 تشغيل Unity MCP Server
```bash
cd /home/user/unity-mcp
python server.py
```

يجب أن ترى:
```
🚀 Unity MCP Server running on port 3000
✅ Waiting for Unity Editor connection...
```

### 4.2 فتح Unity وتوصيل MCP
```bash
# في نافذة جديدة
# افتح Unity Hub
# اص نع مشروع جديد: "TestAIGame"
# من Unity Editor:
# Window -> Package Manager
# Add package from git URL: <unity-mcp-package-url>
```

---

## 🎯 خطوة 5: إنشاء أول لعبة! (Automated)

### 5.1 إنشاء Master Script
```bash
cd /home/user/Game-OS
mkdir -p ai_game_dev/agents
cd ai_game_dev
```

### 5.2 إنشاء Simple Master Agent
```python
# simple_master.py
import anthropic
import os
from dotenv import load_dotenv
import json

load_dotenv()

class SimpleGameDev:
    def __init__(self):
        self.claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    def create_game(self, game_idea: str):
        """إنشاء لعبة بسيطة"""

        print("🎮 Starting AI Game Development...")
        print(f"📝 Idea: {game_idea}\n")

        # Step 1: Design
        print("📋 Step 1: Designing game...")
        gdd = self.design_game(game_idea)
        print("✅ Game Design Complete!\n")

        # Step 2: Generate Scripts
        print("💻 Step 2: Generating C# scripts...")
        scripts = self.generate_scripts(gdd)
        print(f"✅ Generated {len(scripts)} scripts!\n")

        # Step 3: Generate UI Design
        print("🎨 Step 3: Designing UI...")
        ui_design = self.design_ui(gdd)
        print("✅ UI Design Complete!\n")

        print("="*60)
        print("🎉 GAME READY FOR UNITY IMPLEMENTATION!")
        print("="*60)

        return {
            'gdd': gdd,
            'scripts': scripts,
            'ui_design': ui_design
        }

    def design_game(self, game_idea: str) -> dict:
        """تصميم اللعبة"""

        response = self.claude.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=6000,
            messages=[{
                "role": "user",
                "content": f"""Design a simple Unity game based on this idea:

{game_idea}

Create a Game Design Document with:
1. Core Mechanics (very simple)
2. Game Flow
3. Required Scripts (list with descriptions)
4. UI Elements needed
5. Simple art style description

Keep it VERY SIMPLE for a prototype.

Output JSON format."""
            }]
        )

        try:
            gdd = json.loads(response.content[0].text)
        except:
            # If not valid JSON, wrap it
            gdd = {"raw_design": response.content[0].text}

        # Save GDD
        with open('game_design.json', 'w', encoding='utf-8') as f:
            json.dump(gdd, f, indent=2, ensure_ascii=False)

        return gdd

    def generate_scripts(self, gdd: dict) -> list:
        """توليد C# Scripts"""

        scripts = []

        # Example: Generate GameManager script
        script_prompt = f"""Generate a complete Unity C# script for a GameManager based on this design:

{json.dumps(gdd, indent=2)}

Requirements:
- Simple and clean code
- Comments explaining each section
- Unity best practices
- Ready to use

Name it: GameManager.cs"""

        response = self.claude.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            messages=[{"role": "user", "content": script_prompt}]
        )

        script_content = response.content[0].text

        # Save script
        with open('GameManager.cs', 'w') as f:
            f.write(script_content)

        scripts.append({'name': 'GameManager.cs', 'content': script_content})

        return scripts

    def design_ui(self, gdd: dict) -> dict:
        """تصميم الـ UI"""

        response = self.claude.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=3000,
            messages=[{
                "role": "user",
                "content": f"""Design a simple UI layout for this game:

{json.dumps(gdd, indent=2)}

Specify:
1. UI Elements (buttons, text, panels)
2. Layout (positions)
3. Color scheme
4. Font suggestions

Output JSON format."""
            }]
        )

        try:
            ui = json.loads(response.content[0].text)
        except:
            ui = {"raw_ui": response.content[0].text}

        with open('ui_design.json', 'w', encoding='utf-8') as f:
            json.dump(ui, f, indent=2, ensure_ascii=False)

        return ui

# Usage
if __name__ == "__main__":
    dev = SimpleGameDev()

    game_idea = """
    Simple Football Manager Clicker:
    - Click to train players (gain XP)
    - Buy new players with XP
    - Each player increases XP per click
    - Simple progress bar showing team strength
    - Minimal UI with cartoon style
    """

    result = dev.create_game(game_idea)

    print("\n📁 Files created:")
    print("- game_design.json")
    print("- GameManager.cs")
    print("- ui_design.json")
```

### 5.3 تشغيل!
```bash
python simple_master.py
```

---

## 📊 التحقق من النتائج

بعد التشغيل، يجب أن يكون لديك:

```
ai_game_dev/
├── game_design.json      # Game Design Document
├── GameManager.cs        # Unity C# script
├── ui_design.json        # UI specifications
└── simple_master.py      # The agent
```

---

## 🎨 خطوة 6: Implementation في Unity (Manual - لحد ما نكمل automation)

### 6.1 فتح Unity Project
```bash
# افتح Unity Hub
# Create New Project -> 3D
# Name: "AIFootballManager"
```

### 6.2 إضافة الـ Script
1. في Unity: `Assets -> Create -> C# Script`
2. سمه: `GameManager`
3. انسخ محتوى `GameManager.cs` اللي تم توليده
4. الصق في Unity script

### 6.3 إنشاء UI
1. `GameObject -> UI -> Canvas`
2. أضف UI elements حسب `ui_design.json`
3. اربط الـ script بالـ Canvas

### 6.4 Test!
اضغط Play في Unity وشوف لعبتك! 🎮

---

## 🚀 الخطوات القادمة

### المرحلة التالية: Full Automation

الآن بعد ما جربت النظام الأساسي، يمكنك:

1. **إضافة Asset Generation:**
   - دمج Meshy AI لتوليد 3D models
   - دمج Suno AI للموسيقى

2. **Unity MCP Integration الكامل:**
   - أتمتة إنشاء UI في Unity
   - أتمتة إضافة Scripts

3. **Computer Use Integration:**
   - استخدام Claude Computer Use لأتمتة Unity workflow

4. **Steam Upload:**
   - إعداد SteamCMD
   - أتمتة Build & Upload

راجع `AI_GAME_DEVELOPMENT_MASTER_PLAN.md` للخطة الكاملة!

---

## 🐛 Troubleshooting

### مشكلة: API Key لا يعمل
```bash
# تحقق من الـ .env
cat .env
# تأكد من وجود المفاتيح بدون spaces
```

### مشكلة: Unity MCP لا يتصل
```bash
# تأكد من تشغيل server
cd /home/user/unity-mcp
python server.py

# تحقق من port 3000
netstat -an | grep 3000
```

### مشكلة: Python modules not found
```bash
# تأكد من virtual environment active
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📞 المساعدة

إذا واجهت أي مشاكل:
1. راجع `AI_GAME_DEVELOPMENT_MASTER_PLAN.md`
2. GitHub Issues: unity-mcp repository
3. Discord: Unity ML-Agents community

---

## ✅ Checklist للنجاح

- [ ] Python 3.10+ installed
- [ ] Unity 2021.3 LTS installed
- [ ] All API keys obtained
- [ ] .env file created
- [ ] unity-mcp cloned
- [ ] Test script ran successfully
- [ ] First game concept generated
- [ ] Unity project created
- [ ] Script tested in Unity

---

**🎉 Congratulations! You're ready to build AI-powered games!**

---

*Next: Read the full Master Plan for advanced features!*
