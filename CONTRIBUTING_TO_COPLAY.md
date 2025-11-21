# 🤝 دليل المساهمة في Coplay - خطوات عملية للبدء
## Contributing to Coplay Open Source Project

---

## 🎯 البدء السريع

### الخطوة 1: Fork المشروع (5 دقائق)

```bash
# 1. Fork على GitHub
# اذهب إلى: https://github.com/CoplayDev/coplay-unity-plugin
# اضغط Fork في أعلى اليمين

# 2. Clone fork الخاص بك
cd /home/user
git clone https://github.com/YOUR-USERNAME/coplay-unity-plugin.git
cd coplay-unity-plugin

# 3. Add upstream remote
git remote add upstream https://github.com/CoplayDev/coplay-unity-plugin.git

# 4. Verify remotes
git remote -v
# Output should show:
# origin    https://github.com/YOUR-USERNAME/coplay-unity-plugin.git (fetch)
# origin    https://github.com/YOUR-USERNAME/coplay-unity-plugin.git (push)
# upstream  https://github.com/CoplayDev/coplay-unity-plugin.git (fetch)
# upstream  https://github.com/CoplayDev/coplay-unity-plugin.git (push)

# 5. Clone Unity MCP as well
cd ..
git clone https://github.com/YOUR-USERNAME/unity-mcp.git
cd unity-mcp
git remote add upstream https://github.com/CoplayDev/unity-mcp.git
```

---

## 📂 هيكل المشروع

### Coplay Unity Plugin (C#)

```
coplay-unity-plugin/
├── Editor/
│   ├── CoplayWindow.cs           # نافذة Coplay الرئيسية
│   ├── OrchestratorMode.cs       # منطق Orchestrator
│   ├── ActionRecorder.cs         # تسجيل Pipelines
│   ├── AIModelSwitcher.cs        # التبديل بين AI models
│   ├── MeshyIntegration.cs       # تكامل Meshy
│   └── Settings/
│       └── CoplaySettings.cs     # الإعدادات
├── Runtime/
│   ├── CoplayAPI.cs              # API client
│   ├── MCPClient.cs              # اتصال MCP
│   └── Models/
│       ├── GDD.cs                # Game Design Document model
│       └── OrchestratorResult.cs
├── Tests/
│   ├── Editor/
│   └── Runtime/
├── Documentation~/
├── package.json
└── README.md
```

### Unity MCP Server (Python)

```
unity-mcp/
├── server.py                      # MCP server الرئيسي
├── tools/                         # 14 MCP tools
│   ├── execute_menu_item.py
│   ├── manage_asset.py
│   ├── manage_gameobject.py
│   ├── manage_scene.py
│   ├── manage_prefabs.py
│   ├── apply_text_edits.py
│   ├── script_apply_edits.py
│   ├── validate_script.py
│   ├── search_and_replace.py
│   ├── batch_operations.py
│   ├── ai_code_generation.py     # ← سنضيف models هنا
│   └── meshy_generate_3d.py      # ← سنضيف APIs هنا
├── resources/                     # موارد read-only
├── tests/
├── requirements.txt
└── README.md
```

---

## 🚀 أول مساهمة: إضافة Claude Opus

دعنا نبدأ بإضافة Claude Opus model كأول مساهمة!

### Step 1: Create Feature Branch

```bash
cd /home/user/coplay-unity-plugin
git checkout -b feature/add-claude-opus

cd /home/user/unity-mcp
git checkout -b feature/add-claude-opus
```

### Step 2: Update Unity Plugin (C#)

**File:** `Editor/AIModelSwitcher.cs`

```csharp
// Add to enum
public enum AIModel {
    GPT4Turbo,
    Gemini25Pro,
    ClaudeSonnet45,
    Grok3,
    ClaudeOpus  // ← NEW
}

// Add to model info dictionary
private static readonly Dictionary<AIModel, ModelInfo> ModelInfos = new() {
    { AIModel.GPT4Turbo, new ModelInfo {
        DisplayName = "GPT-4 Turbo",
        Provider = "OpenAI",
        MaxTokens = 128000,
        CostPer1KTokens = 0.01f,
        Description = "Best for complex algorithms"
    }},

    { AIModel.Gemini25Pro, new ModelInfo {
        DisplayName = "Gemini 2.5 Pro",
        Provider = "Google",
        MaxTokens = 2000000,
        CostPer1KTokens = 0.00125f,
        Description = "Best for bulk generation"
    }},

    { AIModel.ClaudeSonnet45, new ModelInfo {
        DisplayName = "Claude Sonnet 4.5",
        Provider = "Anthropic",
        MaxTokens = 200000,
        CostPer1KTokens = 0.003f,
        Description = "Best for precise editing"
    }},

    { AIModel.Grok3, new ModelInfo {
        DisplayName = "Grok 3",
        Provider = "xAI",
        MaxTokens = 128000,
        CostPer1KTokens = 0.002f,
        Description = "Best for experimental features"
    }},

    // NEW MODEL
    { AIModel.ClaudeOpus, new ModelInfo {
        DisplayName = "Claude Opus",
        Provider = "Anthropic",
        MaxTokens = 200000,
        CostPer1KTokens = 0.015f,
        Description = "Highest quality, best for critical code"
    }}
};
```

### Step 3: Update MCP Server (Python)

**File:** `unity-mcp/tools/ai_code_generation.py`

```python
SUPPORTED_MODELS = {
    'gpt-4-turbo': {
        'provider': 'openai',
        'model_id': 'gpt-4-turbo-preview',
        'max_tokens': 128000
    },
    'gemini-2.5-pro': {
        'provider': 'google',
        'model_id': 'gemini-2.5-pro',
        'max_tokens': 2000000
    },
    'claude-sonnet-4-5': {
        'provider': 'anthropic',
        'model_id': 'claude-sonnet-4-5-20250929',
        'max_tokens': 200000
    },
    'grok-3': {
        'provider': 'xai',
        'model_id': 'grok-3',
        'max_tokens': 128000
    },

    # NEW MODEL
    'claude-opus': {
        'provider': 'anthropic',
        'model_id': 'claude-3-5-opus-20241022',
        'max_tokens': 200000
    }
}

class AnthropicProvider:
    def __init__(self, model_id: str, max_tokens: int, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model_id = model_id
        self.max_tokens = max_tokens

    async def generate(self, prompt: str, temperature: float = 0.7) -> str:
        response = self.client.messages.create(
            model=self.model_id,
            max_tokens=self.max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text
```

### Step 4: Add Tests

**File:** `unity-mcp/tests/test_claude_opus.py`

```python
import pytest
from tools.ai_code_generation import generate_code

@pytest.mark.asyncio
async def test_claude_opus_generation():
    """Test Claude Opus model can generate code"""

    prompt = """
    Generate a simple C# Unity script for player movement:
    - WASD movement
    - Jump with Space
    - Speed: 5.0
    """

    result = await generate_code(
        prompt=prompt,
        model='claude-opus',
        language='csharp'
    )

    assert result is not None
    assert 'class' in result
    assert 'void Update()' in result
    assert 'Rigidbody' in result or 'Transform' in result

@pytest.mark.asyncio
async def test_claude_opus_quality():
    """Test Claude Opus produces high quality code"""

    prompt = "Generate a pathfinding algorithm for Unity NavMesh"

    result = await generate_code(
        prompt=prompt,
        model='claude-opus'
    )

    # Check for quality indicators
    assert '///' in result  # XML documentation
    assert 'try' in result or 'if' in result  # Error handling
    assert len(result) > 200  # Sufficient detail
```

### Step 5: Update Documentation

**File:** `Documentation~/Models.md`

```markdown
# Supported AI Models

## Claude Opus (NEW!)

**Provider:** Anthropic
**Model ID:** claude-3-5-opus-20241022
**Max Tokens:** 200,000
**Cost:** $0.015 per 1K tokens

### Best For:
- ✅ Critical game logic requiring highest quality
- ✅ Complex algorithms (pathfinding, AI opponents)
- ✅ Architecture-level decisions
- ✅ Code that needs to be production-ready first time

### When to Use:
Use Claude Opus when you need the absolute best quality and cost is not a concern.
It's slower and more expensive than other models, but produces the highest quality code.

### Example:
```csharp
// Unity Plugin
var orchestrator = new OrchestratorMode();
orchestrator.SwitchModel(AIModel.ClaudeOpus);

// For critical game manager
var gameManager = await orchestrator.GenerateScript(new ScriptSpec {
    Name = "GameManager",
    Description = "Core game state management with save/load"
});
```

### Comparison:

| Feature | Claude Opus | Claude Sonnet | Gemini Pro | GPT-4 |
|---------|-------------|---------------|------------|-------|
| Quality | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Speed | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Cost | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
```

### Step 6: Commit Changes

```bash
# Unity Plugin
cd /home/user/coplay-unity-plugin
git add Editor/AIModelSwitcher.cs
git add Documentation~/Models.md
git commit -m "feat: Add Claude Opus model support

- Add ClaudeOpus enum value
- Add model info with pricing and capabilities
- Update documentation with usage guide
- Add comparison with other models"

# MCP Server
cd /home/user/unity-mcp
git add tools/ai_code_generation.py
git add tests/test_claude_opus.py
git commit -m "feat: Add Claude Opus provider

- Add claude-opus to supported models
- Update AnthropicProvider to handle Opus
- Add comprehensive tests
- Document API usage"
```

### Step 7: Push & Create PR

```bash
# Unity Plugin
cd /home/user/coplay-unity-plugin
git push origin feature/add-claude-opus

# Go to GitHub and create PR
# Title: feat: Add Claude Opus model support
# Description:
"""
## Description
Adds support for Claude Opus, Anthropic's highest quality model.

## Changes
- Added ClaudeOpus to AIModel enum
- Added model info with pricing ($0.015/1K tokens)
- Updated documentation with usage guide
- Added comparison table

## Testing
- Tested code generation with Claude Opus
- Verified model switching works
- Confirmed API key handling

## Type of Change
- [x] New feature
- [ ] Bug fix
- [ ] Breaking change
- [x] Documentation update

## Screenshots
(Add screenshot of Claude Opus in model selector)
"""

# Repeat for MCP Server
cd /home/user/unity-mcp
git push origin feature/add-claude-opus
# Create PR on GitHub
```

---

## 🎯 مساهمات أخرى مقترحة

### مساهمة #2: إضافة Suno AI لتوليد الموسيقى

**الصعوبة:** متوسطة
**الوقت المتوقع:** 4-6 ساعات
**التأثير:** عالي جداً

**Files to modify:**
```
unity-mcp/tools/suno_generate_audio.py (NEW)
coplay-unity-plugin/Editor/SunoIntegration.cs (NEW)
coplay-unity-plugin/Editor/OrchestratorMode.cs (UPDATE)
```

**Branch name:** `feature/suno-audio-integration`

**Steps:**
1. Create `suno_generate_audio.py` MCP tool
2. Create `SunoIntegration.cs` Unity wrapper
3. Add Step 8 (Audio Integration) to Orchestrator
4. Write tests
5. Update documentation
6. Submit PR

### مساهمة #3: إضافة ElevenLabs لتوليد الأصوات

**الصعوبة:** متوسطة
**الوقت المتوقع:** 3-5 ساعات
**التأثير:** عالي

**Files to modify:**
```
unity-mcp/tools/elevenlabs_generate_sfx.py (NEW)
coplay-unity-plugin/Editor/ElevenLabsIntegration.cs (NEW)
```

**Branch name:** `feature/elevenlabs-sfx-integration`

### مساهمة #4: Pipeline Marketplace Backend

**الصعوبة:** عالية
**الوقت المتوقع:** 2-3 أسابيع
**التأثير:** عالي جداً

**New Repository:** `coplay-marketplace`

**Stack:**
- Backend: FastAPI (Python)
- Database: PostgreSQL
- Storage: S3 or similar
- Auth: JWT

**Features:**
- Upload/download pipelines
- Search and filter
- Ratings and reviews
- User profiles

---

## 📋 Checklist قبل Submit PR

### Code Quality
- [ ] Code follows project style guide
- [ ] No commented-out code
- [ ] No debug print statements
- [ ] Meaningful variable names
- [ ] Functions are small and focused

### Documentation
- [ ] XML comments on public methods (C#)
- [ ] Docstrings on functions (Python)
- [ ] README updated if needed
- [ ] Examples added if needed

### Testing
- [ ] Unit tests added
- [ ] All tests passing locally
- [ ] Manual testing done
- [ ] Edge cases considered

### Git
- [ ] Descriptive commit messages
- [ ] Branch name follows convention
- [ ] Rebased on latest main
- [ ] No merge conflicts

### PR Description
- [ ] Clear description of changes
- [ ] Screenshots/videos if UI change
- [ ] Links to related issues
- [ ] Migration guide if breaking change

---

## 🤝 Communication

### Where to Discuss

**GitHub Issues:**
- Bug reports
- Feature requests
- Questions about implementation

**GitHub Discussions:**
- General questions
- Ideas and brainstorming
- Community help

**Discord:** (if available)
- Real-time chat
- Quick questions
- Community building

**Email:**
- Private matters
- Security issues

### Issue Templates

**Bug Report:**
```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Go to...
2. Click on...
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Coplay version: 8.3.0
- Unity version: 2021.3.25f1
- OS: Windows 10

## Screenshots
(if applicable)
```

**Feature Request:**
```markdown
## Feature Description
Clear description of proposed feature

## Motivation
Why is this needed?

## Proposed Solution
How would this work?

## Alternatives Considered
What other approaches did you think about?

## Additional Context
Any other relevant information
```

---

## 🎓 Learning Resources

### Understanding the Codebase

**1. Start Here:**
```bash
# Read these files first
coplay-unity-plugin/README.md
coplay-unity-plugin/CONTRIBUTING.md (if exists)
unity-mcp/README.md

# Then explore
Editor/CoplayWindow.cs  # Main UI
Editor/OrchestratorMode.cs  # Core logic
tools/ai_code_generation.py  # AI integration
```

**2. Follow the Flow:**
```
User clicks "Generate" in Unity
    → CoplayWindow.OnGenerateClicked()
    → OrchestratorMode.Execute()
    → MCPClient.SendRequest()
    → (network) →
    → server.py receives request
    → tools/ai_code_generation.py
    → AI API (Claude/Gemini/etc)
    → Response back through chain
    → Unity creates files
```

**3. Debug & Learn:**
```csharp
// Add logging to understand flow
Debug.Log($"[Coplay] Generating script: {scriptName}");
Debug.Log($"[Coplay] Using model: {currentModel}");
Debug.Log($"[Coplay] Response: {response.Substring(0, 100)}...");
```

### C# for Unity Plugin

**Resources:**
- Unity Documentation: https://docs.unity3d.com/
- C# Guide: https://learn.microsoft.com/en-us/dotnet/csharp/
- Unity Editor Scripting: https://docs.unity3d.com/ScriptReference/

**Key Concepts:**
- EditorWindow (for UI)
- AssetDatabase (file operations)
- SerializedObject (settings)
- Async/Await (for network calls)

### Python for MCP Server

**Resources:**
- FastAPI: https://fastapi.tiangolo.com/
- asyncio: https://docs.python.org/3/library/asyncio.html
- aiohttp: https://docs.aiohttp.org/

**Key Concepts:**
- async/await
- WebSocket connections
- JSON serialization
- Error handling

---

## 🏆 Recognition

### Contributor Levels

**🌟 First-Time Contributor**
- First PR merged
- Listed in CONTRIBUTORS.md

**⭐ Regular Contributor**
- 5+ PRs merged
- Badge on profile

**⭐⭐ Core Contributor**
- 20+ PRs merged
- Write access to repo (maybe)
- Mentioned in release notes

**⭐⭐⭐ Maintainer**
- Trusted community member
- Can review PRs
- Help guide project direction

---

## 📊 Tracking Progress

### Personal Contribution Tracker

Create file: `~/coplay-contributions.md`

```markdown
# My Coplay Contributions

## PRs Submitted
- [ ] #1: Add Claude Opus support - Submitted 2025-11-21
- [ ] #2: Suno AI integration - In Progress
- [ ] #3: ElevenLabs integration - Planning

## PRs Merged
- [x] #1: Add Claude Opus support - Merged 2025-11-25 🎉

## Issues Created
- #15: Feature request for Llama 3 support
- #23: Bug in orchestrator step 5

## Impact
- Models added: 1 (Claude Opus)
- Lines of code: 347
- Tests added: 5
- Documentation pages: 2

## Goals
- [ ] Get 5 PRs merged (1/5)
- [ ] Become regular contributor
- [ ] Add all asset APIs
- [ ] Build marketplace
```

---

## ✅ Ready to Contribute!

**Quick Start Checklist:**

1. ✅ Fork repositories
2. ✅ Setup development environment
3. ✅ Read codebase
4. ✅ Pick first issue
5. ✅ Create feature branch
6. ✅ Implement feature
7. ✅ Write tests
8. ✅ Update docs
9. ✅ Submit PR
10. ✅ Respond to review
11. ✅ Celebrate merge! 🎉

---

**Let's make Coplay even better! 🚀**

*Happy Contributing!*
