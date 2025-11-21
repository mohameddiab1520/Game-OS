# GameOS AI - System Architecture
## Building Coplay-Like System on Unity MCP

---

## 📋 Executive Summary

We are building **GameOS AI** - an open-source, fully-featured Unity AI assistant that matches Coplay's capabilities by extending Unity MCP (open source) with premium features:

- ✅ **Orchestrator Mode** - Automated game development from plan files
- ✅ **Asset Generation** - 3D models, textures, images via AI APIs
- ✅ **Pipeline Recording** - Record and replay workflows
- ✅ **Multi-Model AI** - Support for GPT-4, Claude, Gemini, and more
- ✅ **Todo List System** - Track progress automatically
- ✅ **Unity Editor Plugin** - Professional UI matching Coplay

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Unity Editor Window                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              GameOS AI Panel (C#)                   │   │
│  │  • Chat Interface                                   │   │
│  │  • Mode Selector (Chat/Agent/Orchestrator)          │   │
│  │  • Model Selector (GPT-4/Claude/Gemini)             │   │
│  │  • Todo List View                                   │   │
│  │  • Pipeline Recording Controls                      │   │
│  │  • Function Call UI (3D/Texture/Scene Generation)   │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                  │
│                           │ WebSocket                        │
│                           ▼                                  │
└───────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                Python Backend (FastMCP)                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         GameOS AI Server (Extended MCP)             │   │
│  │                                                      │   │
│  │  Unity MCP Base (14 tools)                          │   │
│  │  ├─ manage_scene                                    │   │
│  │  ├─ manage_gameobject                               │   │
│  │  ├─ manage_script                                   │   │
│  │  └─ ... etc                                         │   │
│  │                                                      │   │
│  │  NEW: Orchestrator Module                           │   │
│  │  ├─ plan_parser.py                                  │   │
│  │  ├─ orchestrator_engine.py                          │   │
│  │  └─ task_executor.py                                │   │
│  │                                                      │   │
│  │  NEW: Asset Generation Module                       │   │
│  │  ├─ meshy_api.py (3D models)                        │   │
│  │  ├─ texture_generator.py                            │   │
│  │  └─ image_generator.py                              │   │
│  │                                                      │   │
│  │  NEW: Multi-Model AI                                │   │
│  │  ├─ openai_client.py                                │   │
│  │  ├─ anthropic_client.py                             │   │
│  │  ├─ google_client.py                                │   │
│  │  └─ model_router.py                                 │   │
│  │                                                      │   │
│  │  NEW: Pipeline Recording                            │   │
│  │  ├─ action_recorder.py                              │   │
│  │  └─ pipeline_player.py                              │   │
│  │                                                      │   │
│  │  NEW: Todo System                                   │   │
│  │  └─ todo_manager.py                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                  │
│                    External APIs                             │
│                           ▼                                  │
│  ┌──────────────┬──────────────┬──────────────┐            │
│  │  Meshy API   │  OpenAI API  │  Claude API  │            │
│  │ (3D Models)  │   (GPT-4)    │  (Sonnet)    │            │
│  └──────────────┴──────────────┴──────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Game-OS/
├── README.md
├── setup.sh
├── requirements.txt
│
├── ai_game_dev/                      # Python Backend
│   ├── __init__.py
│   │
│   ├── core/                         # Core Engine
│   │   ├── __init__.py
│   │   ├── server.py                 # Main FastMCP server (extends Unity MCP)
│   │   ├── config.py                 # Configuration
│   │   └── models.py                 # Data models
│   │
│   ├── mcp_bridge/                   # Unity MCP Integration
│   │   ├── __init__.py
│   │   ├── unity_connection.py       # WebSocket connection (from Unity MCP)
│   │   ├── unity_tools.py            # Unity MCP tools (14 tools)
│   │   └── unity_resources.py        # Unity MCP resources (12 resources)
│   │
│   ├── orchestrator/                 # 🆕 Orchestrator Mode
│   │   ├── __init__.py
│   │   ├── plan_parser.py            # Parse GamePlan.md files
│   │   ├── orchestrator_engine.py    # Main execution engine
│   │   ├── task_executor.py          # Execute individual tasks
│   │   └── task_types.py             # Task type definitions
│   │
│   ├── assets/                       # 🆕 Asset Generation
│   │   ├── __init__.py
│   │   ├── meshy_api.py              # Meshy 3D model generation
│   │   ├── texture_generator.py      # Texture generation
│   │   ├── image_generator.py        # Image generation
│   │   └─�� asset_importer.py          # Import assets to Unity
│   │
│   ├── ai_models/                    # 🆕 Multi-Model AI
│   │   ├── __init__.py
│   │   ├── base_client.py            # Base AI client interface
│   │   ├── openai_client.py          # OpenAI (GPT-4, GPT-4o)
│   │   ├── anthropic_client.py       # Anthropic (Claude Sonnet/Opus)
│   │   ├── google_client.py          # Google (Gemini 2.5 Pro)
│   │   ├── groq_client.py            # Groq (Fast inference)
│   │   └── model_router.py           # Route to appropriate model
│   │
│   ├── pipeline/                     # 🆕 Pipeline Recording
│   │   ├── __init__.py
│   │   ├── action_recorder.py        # Record action sequences
│   │   ├── pipeline_player.py        # Replay recorded pipelines
│   │   └── pipeline_storage.py       # Save/load pipelines
│   │
│   ├── todo/                         # 🆕 Todo System
│   │   ├── __init__.py
│   │   ├── todo_manager.py           # Manage todo lists
│   │   └── progress_tracker.py       # Track task progress
│   │
│   └── utils/                        # Utilities
│       ├── __init__.py
│       ├── logger.py                 # Logging
│       └── telemetry.py              # Anonymous usage stats
│
├── unity_plugin/                     # Unity C# Plugin
│   ├── package.json
│   ├── README.md
│   │
│   ├── Editor/
│   │   ├── GameOSAI.Editor.asmdef
│   │   │
│   │   ├── Core/
│   │   │   ├── GameOSBridge.cs       # WebSocket connection (from Unity MCP)
│   │   │   ├── GameOSMenu.cs         # Menu items
│   │   │   └── GameOSConfig.cs       # Configuration
│   │   │
│   │   ├── Windows/                  # 🆕 Editor Windows
│   │   │   ├── GameOSWindow.cs       # Main editor window
│   │   │   ├── GameOSWindow.uxml     # UI layout
│   │   │   └── GameOSWindow.uss      # Styles
│   │   │
│   │   ├── UI/                       # 🆕 UI Components
│   │   │   ├── ChatView.cs           # Chat interface
│   │   │   ├── TodoListView.cs       # Todo list
│   │   │   ├── PipelineView.cs       # Pipeline controls
│   │   │   ├── FunctionCallView.cs   # Function execution UI
│   │   │   └── Resources/
│   │   │       ├── chat_message.uxml
│   │   │       ├── todo_list_item.uxml
│   │   │       ├── function_call_3d_model.uxml
│   │   │       ├── function_call_texture.uxml
│   │   │       ├── function_call_scene.uxml
│   │   │       ├── pipeline_recording.uxml
│   │   │       ├── style.uss
│   │   │       ├── style_dark.uss
│   │   │       └── style_light.uss
│   │   │
│   │   ├── Models/                   # Data models
│   │   │   ├── ChatMessage.cs
│   │   │   ├── TodoItem.cs
│   │   │   └── FunctionCall.cs
│   │   │
│   │   ├── Services/                 # Services
│   │   │   ├── WebSocketService.cs   # WebSocket communication
│   │   │   ├── ModelService.cs       # AI model management
│   │   │   └── AssetService.cs       # Asset import/management
│   │   │
│   │   └── Tools/                    # Unity tools (from MCP)
│   │       ├── SceneTools.cs
│   │       ├── GameObjectTools.cs
│   │       └── ScriptTools.cs
│   │
│   └── Runtime/
│       └── Serialization/
│           └── UnityTypeConverters.cs
│
├── docs/                             # Documentation
│   ├── GETTING_STARTED.md
│   ├── ORCHESTRATOR_MODE.md
│   ├── ASSET_GENERATION.md
│   ├── PIPELINE_RECORDING.md
│   └── API_REFERENCE.md
│
└── examples/                         # Example projects
    ├── simple_platformer/
    │   └── GamePlan.md
    ├── racing_game/
    │   └── GamePlan.md
    └── puzzle_game/
        └── GamePlan.md
```

---

## 🎯 Component Details

### 1. Unity MCP Base (Already Available)

**From:** `coplay-original/` (Unity MCP open source)

**14 Tools:**
1. `execute_menu_item` - Execute Unity menu items
2. `manage_asset` - Asset operations
3. `manage_editor` - Editor control
4. `manage_gameobject` - GameObject operations
5. `manage_prefabs` - Prefab operations
6. `manage_scene` - Scene management
7. `manage_script` - Script operations
8. `manage_shader` - Shader operations
9. `read_console` - Console messages
10. `run_tests` - Run Unity tests
11. `set_active_instance` - Multi-instance support
12. `apply_text_edits` - Precise text editing
13. `script_apply_edits` - Structured C# edits
14. `validate_script` - Script validation

**12 Resources:**
1. `unity_instances` - Running Unity instances
2. `menu_items` - Available menu items
3. `tests` - Available tests
4. `editor_active_tool` - Active editor tool
5. `editor_prefab_stage` - Prefab editing context
6. `editor_selection` - Selected objects
7. `editor_state` - Editor state
8. `editor_windows` - Open windows
9. `project_info` - Project information
10. `project_layers` - Project layers
11. `project_tags` - Project tags
12. `scene_hierarchy` - Current scene hierarchy

---

### 2. 🆕 Orchestrator Mode

**Purpose:** Automate game development from plan files

**Files:**
- `ai_game_dev/orchestrator/plan_parser.py`
- `ai_game_dev/orchestrator/orchestrator_engine.py`
- `ai_game_dev/orchestrator/task_executor.py`

**Plan File Format:** `Assets/GamePlan.md`

```markdown
# Game Title

## Assets
- [ ] {3d_model} Generate player: "cute robot character"
- [ ] {texture} Generate ground: "grass field texture"
- [ ] {image} Generate UI button: "red play button"

## Scripts
- [ ] {script} PlayerController: WASD movement + Space jump
- [ ] {script} CameraFollow: smooth third-person camera

## Scenes
- [ ] {scene} MainLevel: create with lighting and spawn points

## Polish
- [ ] {particle} Add jump effect
- [ ] {audio} Add footstep sounds
```

**Task Types:**
- `{3d_model}` - Generate 3D model via Meshy
- `{texture}` - Generate texture
- `{image}` - Generate image
- `{script}` - Write C# script
- `{scene}` - Create Unity scene
- `{gameobject}` - Create GameObject
- `{prefab}` - Create prefab
- `{material}` - Create material
- `{particle}` - Create particle system
- `{audio}` - Handle audio
- `{ui}` - Create UI elements

**Execution Flow:**
1. Parse `GamePlan.md` into task list
2. Execute tasks sequentially
3. Update todo list in UI
4. Handle errors and retry
5. Mark tasks as complete

---

### 3. 🆕 Asset Generation

**Purpose:** Generate 3D models, textures, and images using AI

**APIs Supported:**
- **Meshy API** - 3D model generation
- **Leonardo.ai** - Images and textures
- **Replicate** - Alternative 3D/image generation
- **Stable Diffusion** - Local image generation

**Files:**
- `ai_game_dev/assets/meshy_api.py`
- `ai_game_dev/assets/texture_generator.py`
- `ai_game_dev/assets/image_generator.py`
- `ai_game_dev/assets/asset_importer.py`

**Functions:**

```python
class MeshyAPI:
    async def generate_model_from_text(prompt: str) -> str:
        """Generate 3D model from text description"""

    async def generate_model_from_image(image_path: str) -> str:
        """Convert image to 3D model"""

    async def generate_texture(prompt: str, model_id: str) -> str:
        """Generate texture for model"""

class AssetImporter:
    def import_gltf_to_unity(gltf_path: str, unity_path: str):
        """Import glTF model to Unity project"""

    def import_texture_to_unity(texture_path: str, unity_path: str):
        """Import texture to Unity"""
```

**Unity Integration:**
- glTF import via `com.unity.cloud.gltfast`
- Automatic material setup
- Asset placement in scenes

---

### 4. 🆕 Multi-Model AI

**Purpose:** Support multiple AI models with automatic routing

**Supported Models:**
- **OpenAI:** GPT-4, GPT-4o, GPT-4 Turbo
- **Anthropic:** Claude Sonnet 4.5, Claude Opus 4
- **Google:** Gemini 2.5 Pro, Gemini 2.0 Flash
- **Groq:** Fast inference (Llama, Mixtral)
- **Local:** Ollama support for local models

**Files:**
- `ai_game_dev/ai_models/base_client.py`
- `ai_game_dev/ai_models/openai_client.py`
- `ai_game_dev/ai_models/anthropic_client.py`
- `ai_game_dev/ai_models/google_client.py`
- `ai_game_dev/ai_models/groq_client.py`
- `ai_game_dev/ai_models/model_router.py`

**Features:**
- Runtime model switching
- Cost tracking per message
- Automatic fallback if model fails
- Specialized routing (e.g., Claude for code, GPT for creativity)

```python
class ModelRouter:
    async def route_message(
        message: str,
        task_type: TaskType,
        preferred_model: str = None
    ) -> AIResponse:
        """Route message to best model for task type"""

    def get_model_cost(model_name: str, tokens: int) -> float:
        """Calculate cost for model usage"""
```

---

### 5. 🆕 Pipeline Recording

**Purpose:** Record and replay action sequences

**Files:**
- `ai_game_dev/pipeline/action_recorder.py`
- `ai_game_dev/pipeline/pipeline_player.py`
- `ai_game_dev/pipeline/pipeline_storage.py`

**Features:**
- Record Unity operations
- Save pipelines to JSON
- Replay with parameters
- Edit recorded pipelines

**Pipeline Format:**

```json
{
  "name": "Setup New Scene",
  "description": "Create scene with lighting and camera",
  "actions": [
    {
      "type": "create_scene",
      "params": {"name": "{{scene_name}}"}
    },
    {
      "type": "create_gameobject",
      "params": {"name": "Directional Light", "type": "Light"}
    },
    {
      "type": "create_gameobject",
      "params": {"name": "Main Camera", "type": "Camera"}
    }
  ],
  "parameters": {
    "scene_name": {"type": "string", "default": "NewScene"}
  }
}
```

---

### 6. 🆕 Todo List System

**Purpose:** Track tasks and progress

**Files:**
- `ai_game_dev/todo/todo_manager.py`
- `ai_game_dev/todo/progress_tracker.py`

**Features:**
- Automatic task creation from plan
- Progress bar visualization
- Task dependencies
- Completion notifications

**UI Components:**
- Collapsed view with progress bar
- Expanded view with task list
- Task status indicators (pending/in_progress/completed)

---

### 7. 🆕 Unity Editor Plugin UI

**Purpose:** Professional editor window matching Coplay

**Main Window:** `unity_plugin/Editor/Windows/GameOSWindow.cs`

**UI Elements:**
- Settings bar with logo and controls
- Thread/chat selection
- Mode selector (Chat/Agent/Orchestrator)
- Model selector dropdown
- Chat interface with message history
- Context selection area
- Todo list (collapsible)
- Pipeline recording controls
- Function call UI for asset generation
- Progress bar for operations
- Status bar

**UI Toolkit (UXML/USS):**
- `GameOSWindow.uxml` - Main layout
- `chat_message.uxml` - Chat message template
- `todo_list_view.uxml` - Todo list view
- `todo_list_item.uxml` - Individual todo item
- `function_call_3d_model.uxml` - 3D generation UI
- `function_call_texture.uxml` - Texture generation UI
- `function_call_scene.uxml` - Scene generation UI
- `pipeline_recording.uxml` - Pipeline controls
- `style.uss` - Main styles
- `style_dark.uss` - Dark theme
- `style_light.uss` - Light theme

---

## 🔄 Data Flow

### Example: Creating a 3D Platformer Game

**User Action:**
1. Create `Assets/GamePlan.md` with game plan
2. Open GameOS AI window in Unity
3. Select "Orchestrator Mode"
4. Select AI model (e.g., Claude Sonnet)
5. Click "Execute Plan"

**System Flow:**

```
1. Unity Plugin → WebSocket → Python Server
   Message: {"action": "start_orchestrator", "plan_path": "Assets/GamePlan.md"}

2. Python: Plan Parser
   - Read GamePlan.md
   - Parse into task list
   - Send to orchestrator engine

3. Python: Orchestrator Engine
   For each task:
     - Determine task type
     - Route to appropriate module

4. Python: Asset Generation (if 3D model task)
   - Call Meshy API with prompt
   - Wait for generation (2-5 minutes)
   - Download glTF file
   - Send to Unity for import

5. Python → Unity via WebSocket
   Message: {"tool": "manage_asset", "action": "import", "path": "/path/to/model.gltf"}

6. Unity Plugin: Asset Importer
   - Import glTF file
   - Create materials
   - Place in scene

7. Python: Todo Manager
   - Update task status to "completed"
   - Send progress update

8. Unity Plugin: UI Update
   - Update todo list
   - Update progress bar
   - Show completion notification
```

---

## 🚀 Implementation Phases

### Phase 1: Foundation (Week 1) ⏰ 5-7 days

**Tasks:**
- [x] Review Coplay and Unity MCP
- [ ] Set up project structure
- [ ] Copy Unity MCP as base
- [ ] Create FastMCP server extension
- [ ] Basic Unity plugin window
- [ ] WebSocket communication
- [ ] Configuration system

**Deliverable:** Basic system with Unity MCP tools working

---

### Phase 2: Orchestrator Mode (Week 2) ⏰ 5-7 days

**Tasks:**
- [ ] Plan parser implementation
- [ ] Orchestrator engine
- [ ] Task executor
- [ ] Task type handlers
- [ ] Integration with Unity tools
- [ ] Error handling and retry logic
- [ ] Progress tracking

**Deliverable:** Orchestrator can read plans and execute basic tasks

---

### Phase 3: Asset Generation (Week 2-3) ⏰ 5-7 days

**Tasks:**
- [ ] Meshy API integration
- [ ] Texture generation
- [ ] Image generation
- [ ] Asset importer (glTF → Unity)
- [ ] Material auto-setup
- [ ] Progress indicators for generation
- [ ] Caching and asset library

**Deliverable:** Can generate 3D models, textures, and images

---

### Phase 4: Multi-Model AI (Week 3) ⏰ 3-5 days

**Tasks:**
- [ ] Base AI client interface
- [ ] OpenAI client
- [ ] Anthropic client
- [ ] Google client
- [ ] Model router
- [ ] Cost tracking
- [ ] Model switching UI

**Deliverable:** Support for multiple AI models

---

### Phase 5: Unity Plugin UI (Week 3-4) ⏰ 7-10 days

**Tasks:**
- [ ] Main window layout (UXML)
- [ ] Chat interface
- [ ] Mode selector
- [ ] Model selector
- [ ] Todo list view
- [ ] Function call UIs
- [ ] Pipeline controls
- [ ] Dark/light themes
- [ ] Progress indicators

**Deliverable:** Professional Unity editor window

---

### Phase 6: Pipeline Recording (Week 4) ⏰ 3-5 days

**Tasks:**
- [ ] Action recorder
- [ ] Pipeline player
- [ ] Pipeline storage (JSON)
- [ ] UI controls
- [ ] Parameter support
- [ ] Pipeline editor

**Deliverable:** Can record and replay workflows

---

### Phase 7: Testing & Polish (Week 4) ⏰ 3-5 days

**Tasks:**
- [ ] Test with example games
- [ ] Bug fixes
- [ ] Performance optimization
- [ ] Documentation
- [ ] Example projects
- [ ] Video tutorials

**Deliverable:** Production-ready system

---

## 📊 Comparison: GameOS AI vs Coplay

| Feature | Coplay | GameOS AI (Ours) |
|---------|--------|------------------|
| **Base Unity Tools** | ✅ 14 tools | ✅ 14 tools (Unity MCP) |
| **Orchestrator Mode** | ✅ Yes | ✅ Yes |
| **3D Model Generation** | ✅ Meshy | ✅ Meshy + Replicate |
| **Texture Generation** | ✅ Yes | ✅ Yes |
| **Image Generation** | ✅ Yes | ✅ Yes |
| **Pipeline Recording** | ✅ Yes | ✅ Yes |
| **Multi-Model AI** | ✅ 4 models | ✅ 4+ models + local |
| **Todo List** | ✅ Yes | ✅ Yes |
| **Unity Editor UI** | ✅ Professional | ✅ Professional |
| **Cost Tracking** | ✅ Yes | ✅ Yes + breakdown |
| **Local Models** | ❌ No | ✅ Ollama support |
| **Open Source** | ❌ No | ✅ MIT License |
| **Monthly Cost** | 💰 $30-100 | 🆓 API costs only |
| **Customization** | ❌ Limited | ✅ Full control |

---

## 🎯 Key Innovations

### Beyond Coplay:

1. **Local Model Support** - Run Ollama/LM Studio locally
2. **Advanced Pipeline Editor** - Visual pipeline builder
3. **Asset Library** - Save and reuse generated assets
4. **Template Plans** - Pre-made game templates
5. **Git Integration** - Auto-commit after tasks
6. **Performance Profiling** - AI-powered optimization
7. **Test Generation** - Auto-generate unit tests
8. **Multiplayer Setup** - Netcode automation
9. **Build Pipeline** - Automated builds
10. **Community Features** - Share pipelines and assets

---

## 💻 Technology Stack

**Python Backend:**
- **FastMCP** - MCP server framework
- **WebSockets** - Unity communication
- **httpx** - HTTP client for APIs
- **Pydantic** - Data validation
- **asyncio** - Async operations

**Unity Plugin (C#):**
- **Unity UI Toolkit** - Modern UI system
- **WebSocket4Net** - WebSocket client
- **Newtonsoft.Json** - JSON serialization
- **Unity.Cloud.GLTFast** - glTF import

**External APIs:**
- **Meshy API** - 3D generation
- **OpenAI API** - GPT models
- **Anthropic API** - Claude models
- **Google AI API** - Gemini models
- **Leonardo.ai** - Image/texture generation

---

## 📝 Next Steps

1. **Set up project structure** ✅
2. **Copy Unity MCP as base**
3. **Create extended FastMCP server**
4. **Build basic Unity window**
5. **Implement Orchestrator Mode**
6. **Add Meshy integration**
7. **Build UI components**
8. **Test with example games**

---

## 🎉 Timeline

**Total Development Time:** 3-4 weeks

**Weekly Breakdown:**
- Week 1: Foundation + Orchestrator
- Week 2: Asset Generation + Multi-Model AI
- Week 3: Unity Plugin UI
- Week 4: Pipeline Recording + Testing

**Target Launch:** End of Week 4

---

**Status:** Architecture complete ✅
**Next:** Begin implementation 🚀
