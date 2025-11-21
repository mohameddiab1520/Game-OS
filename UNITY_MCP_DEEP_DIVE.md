# 🔍 Unity MCP - تحليل عميق للكود
## مراجعة شاملة من الكود المصدري

---

## 📋 جدول المحتويات
1. [نظرة عامة](#نظرة-عامة)
2. [الهيكل المعماري](#الهيكل-المعماري)
3. [تحليل الملفات الرئيسية](#تحليل-الملفات-الرئيسية)
4. [الأدوات المتاحة](#الأدوات-المتاحة)
5. [الموارد](#الموارد)
6. [كيف يعمل النظام](#كيف-يعمل-النظام)
7. [فرص التطوير](#فرص-التطوير)
8. [خطة التطوير المقترحة](#خطة-التطوير-المقترحة)

---

## 🎯 نظرة عامة

### ما هو Unity MCP؟

**Unity MCP** هو جسر (Bridge) بين AI Assistants (مثل Claude, Cursor) و Unity Editor عن طريق بروتوكول MCP (Model Context Protocol).

### المكونات الأساسية

```
Unity MCP System:
├── Unity Editor
│   └── MCPForUnity Package (C# Plugin)
│       ├── WebSocket Client
│       ├── Command Handler
│       └── Unity API Wrapper
│
├── MCP Server (Python)
│   ├── server.py (FastMCP)
│   ├── tools/ (14 أدوات)
│   ├── resources/ (12 موارد)
│   └── unity_connection.py
│
└── AI Assistant (Claude/Cursor)
    └── MCP Client
        └── stdio transport
```

### Maintained by Coplay

- ✅ Coplay تولت صيانة المشروع (كان من Justin Barnett)
- ✅ Funding: $1.2M
- ✅ Active development
- ✅ Discord community: 3,000+ users
- ✅ MIT License

---

## 🏗️ الهيكل المعماري

### Directory Structure

```
unity-mcp/
├── MCPForUnity/              # Unity C# Package
│   ├── Runtime/
│   │   ├── MCPForUnity.cs    # Main bridge class
│   │   ├── WebSocketClient.cs
│   │   └── CommandHandler.cs
│   └── Editor/
│       ├── MCPWindow.cs      # Unity Editor window
│       └── AutoSetup.cs      # Auto-configuration
│
├── Server/                   # Python MCP Server
│   ├── server.py             # Main FastMCP server
│   ├── unity_connection.py   # Unity WebSocket manager
│   ├── config.py             # Configuration
│   ├── models.py             # Data models
│   │
│   ├── tools/                # 14 Tools
│   │   ├── __init__.py
│   │   ├── manage_script.py          # Script CRUD
│   │   ├── script_apply_edits.py     # Structured edits
│   │   ├── manage_gameobject.py      # GameObject operations
│   │   ├── manage_scene.py           # Scene management
│   │   ├── manage_asset.py           # Asset operations
│   │   ├── manage_prefabs.py         # Prefab management
│   │   ├── manage_shader.py          # Shader operations
│   │   ├── manage_editor.py          # Editor control
│   │   ├── execute_menu_item.py      # Menu execution
│   │   ├── read_console.py           # Console reading
│   │   ├── run_tests.py              # Test runner
│   │   ├── resource_tools.py         # Resource tools
│   │   └── set_active_instance.py    # Instance targeting
│   │
│   ├── resources/            # 12 Resources
│   │   ├── __init__.py
│   │   ├── unity_instances.py        # Running instances
│   │   ├── editor_state.py           # Editor state
│   │   ├── project_info.py           # Project metadata
│   │   ├── menu_items.py             # Available menus
│   │   ├── tests.py                  # Test list
│   │   ├── selection.py              # Current selection
│   │   ├── active_tool.py            # Active editor tool
│   │   ├── prefab_stage.py           # Prefab editing context
│   │   ├── windows.py                # Open windows
│   │   ├── layers.py                 # Project layers
│   │   └── tags.py                   # Project tags
│   │
│   ├── registry/             # Tool registry
│   ├── tests/                # Integration tests
│   ├── telemetry.py          # Anonymous telemetry
│   └── port_discovery.py     # Unity port discovery
│
├── CustomTools/              # User custom tools
├── TestProjects/             # Test Unity projects
└── docs/                     # Documentation
```

---

## 📄 تحليل الملفات الرئيسية

### 1. `Server/server.py` (261 سطر)

**الوظيفة:** MCP Server الرئيسي باستخدام FastMCP

**Key Components:**

```python
# Main server instance
mcp = FastMCP(
    name="mcp-for-unity-server",
    lifespan=server_lifespan,
    instructions="..." # تعليمات للـ AI
)

# Lifespan management
@asynccontextmanager
async def server_lifespan(server: FastMCP):
    # Startup:
    - Initialize logging
    - Discover Unity instances
    - Connect to default instance
    - Record telemetry

    yield {"pool": unity_connection_pool}

    # Shutdown:
    - Disconnect all instances
    - Cleanup
```

**Features:**
- ✅ Async/await architecture
- ✅ Rotating file logger (512KB logs)
- ✅ Telemetry (anonymous, opt-out available)
- ✅ Multi-instance support
- ✅ Session-based routing middleware
- ✅ Environment variable configuration

**Logging:**
```python
# Logs to:
~/Library/Application Support/UnityMCP/Logs/unity_mcp_server.log  # macOS
%USERPROFILE%\AppData\Local\UnityMCP\Logs\unity_mcp_server.log  # Windows
```

### 2. `Server/unity_connection.py` (252 سطر)

**الوظيفة:** إدارة الاتصال مع Unity عبر WebSocket

**Key Classes:**

```python
class UnityConnection:
    """Single connection to a Unity instance"""

    def __init__(self, instance_info: InstanceInfo):
        self.host = instance_info.host
        self.port = instance_info.port
        self.websocket = None
        self.is_connected = False

    async def connect(self):
        """Establish WebSocket connection"""
        self.websocket = await websockets.connect(
            f"ws://{self.host}:{self.port}"
        )
        self.is_connected = True

    async def send_command(self, command: str, data: dict):
        """Send command to Unity and wait for response"""
        message = json.dumps({
            "command": command,
            "data": data
        })
        await self.websocket.send(message)
        response = await self.websocket.recv()
        return json.loads(response)

class UnityConnectionPool:
    """Manages multiple Unity instances"""

    def __init__(self):
        self.connections: Dict[str, UnityConnection] = {}
        self.default_instance: str = None

    def discover_all_instances(self) -> List[InstanceInfo]:
        """Discover running Unity instances via port scanning"""
        # Scans ports 53000-53999
        # Returns list of InstanceInfo objects

    def get_connection(self, instance_id: str = None):
        """Get connection to specific instance"""
        if not instance_id:
            instance_id = self.default_instance
        return self.connections.get(instance_id)
```

**Port Discovery:**
```python
# Unity instances listen on:
- Base port: 53000
- Range: 53000-53999
- Each Unity instance gets unique port
- Discovery via HTTP GET to /info endpoint
```

### 3. `Server/tools/manage_script.py` (700+ سطر)

**الوظيفة:** إدارة C# scripts (CRUD + editing)

**Main Functions:**

```python
@mcp_for_unity_tool
def apply_text_edits(
    uri: str,
    edits: List[dict],
    precondition_sha256: str = None,
    strict: bool = None
):
    """
    Apply precise text edits to C# script

    Edit format:
    {
        "startLine": 10,    # 1-indexed
        "startCol": 5,      # 1-indexed
        "endLine": 10,
        "endCol": 15,
        "newText": "new code"
    }

    Features:
    - SHA256 precondition check (prevent concurrent edits)
    - Atomic batch edits
    - LSP-style range support
    - Index-based range support
    - Normalization of 0-based to 1-based
    """

@mcp_for_unity_tool
def create_script(
    uri: str,
    content: str
):
    """Create new C# script"""

@mcp_for_unity_tool
def delete_script(uri: str):
    """Delete C# script"""

@mcp_for_unity_tool
def get_sha(uri: str):
    """Get SHA256 hash + metadata without file contents"""
```

**URI Formats Supported:**
```
unity://path/Assets/Scripts/PlayerController.cs
file:///Users/name/UnityProject/Assets/Scripts/PlayerController.cs
Assets/Scripts/PlayerController.cs
```

### 4. `Server/tools/script_apply_edits.py` (1100+ سطر)

**الوظيفة:** Structured C# edits (methods, classes, properties)

**Key Features:**

```python
@mcp_for_unity_tool
def script_apply_edits(
    uri: str,
    operations: List[dict],
    precondition_sha256: str = None
):
    """
    Structured edits for C# code

    Operation types:
    - insert_method
    - replace_method
    - delete_method
    - insert_class
    - replace_class
    - delete_class
    - insert_property
    - replace_property

    Example:
    {
        "type": "insert_method",
        "anchor": "after:MethodName",
        "code": "public void NewMethod() { ... }"
    }
    """
```

**Anchor System:**
```python
# Anchors for precise insertion:
"after:MethodName"          # After method
"before:MethodName"         # Before method
"start_of_class:ClassName"  # At start of class
"end_of_class:ClassName"    # At end of class
"replace:MethodName"        # Replace method
```

**Safety Features:**
- ✅ SHA256 precondition checks
- ✅ Syntax validation before applying
- ✅ Rollback on failure
- ✅ Detailed error messages with line numbers

### 5. `Server/tools/manage_gameobject.py` (400+ سطر)

**الوظيفة:** GameObject operations in Unity scenes

```python
@mcp_for_unity_tool
def manage_gameobject(
    action: Literal["create", "modify", "delete", "find", "add_component", "remove_component"],
    name: str,
    data: dict = None
):
    """
    GameObject management

    Actions:
    - create: Create new GameObject
    - modify: Modify existing GameObject
    - delete: Delete GameObject
    - find: Find GameObject by name/tag/layer
    - add_component: Add component to GameObject
    - remove_component: Remove component

    Example create:
    {
        "action": "create",
        "name": "Player",
        "data": {
            "position": [0, 1, 0],
            "rotation": [0, 0, 0],
            "scale": [1, 1, 1],
            "components": [
                {"type": "Rigidbody", "mass": 1.0},
                {"type": "BoxCollider"}
            ]
        }
    }
    """
```

**Component System:**
```python
# Common components:
- Transform (position, rotation, scale)
- Rigidbody (physics)
- Collider (BoxCollider, SphereCollider, etc.)
- MeshRenderer (rendering)
- Light (lighting)
- Camera (camera)
- AudioSource (audio)
- Custom scripts (via MonoBehaviour)
```

### 6. `Server/tools/manage_scene.py` (200+ سطر)

**الوظيفة:** Scene management

```python
@mcp_for_unity_tool
def manage_scene(
    action: Literal["load", "save", "create", "get_hierarchy"],
    scene_path: str = None,
    data: dict = None
):
    """
    Scene operations

    Actions:
    - load: Load scene by path
    - save: Save current scene
    - create: Create new scene
    - get_hierarchy: Get scene hierarchy (all GameObjects)
    """
```

---

## 🛠️ الأدوات المتاحة (14 Tools)

### 1. `execute_menu_item`
**الوصف:** تنفيذ أي menu item في Unity Editor

```python
execute_menu_item(menu_path="File/Save Project")
execute_menu_item(menu_path="GameObject/3D Object/Cube")
execute_menu_item(menu_path="Window/Package Manager")
```

**Use Cases:**
- حفظ المشروع
- إنشاء GameObjects جاهزة
- فتح نوافذ Unity
- تشغيل plugins خارجية

### 2. `manage_asset`
**الوصف:** إدارة الـ Assets (import, create, modify, delete)

```python
# Import asset
manage_asset(
    operation="import",
    asset_path="Models/Character.fbx",
    source_path="/path/to/character.fbx"
)

# Create material
manage_asset(
    operation="create",
    asset_path="Materials/PlayerMaterial.mat",
    asset_type="Material",
    data={"color": [1.0, 0.0, 0.0, 1.0]}
)
```

**Asset Types:**
- Material, Texture, Prefab, AudioClip, AnimationClip, etc.

### 3. `manage_gameobject`
**الوصف:** إدارة GameObjects في Scene

```python
# Create player
manage_gameobject(
    action="create",
    name="Player",
    data={
        "position": [0, 1, 0],
        "components": [
            {"type": "Rigidbody"},
            {"type": "CapsuleCollider"}
        ]
    }
)

# Add component
manage_gameobject(
    action="add_component",
    name="Player",
    data={
        "component": "Scripts/PlayerController"
    }
)
```

### 4. `manage_scene`
**الوصف:** إدارة Scenes

```python
# Create new scene
manage_scene(
    action="create",
    scene_path="Scenes/MainMenu.unity"
)

# Get hierarchy
hierarchy = manage_scene(action="get_hierarchy")
```

### 5. `manage_prefabs`
**الوصف:** إدارة Prefabs

```python
# Create prefab from GameObject
manage_prefabs(
    operation="create",
    prefab_path="Prefabs/Player.prefab",
    gameobject_name="Player"
)
```

### 6. `apply_text_edits`
**الوصف:** تعديل نصوص C# scripts بدقة

```python
apply_text_edits(
    uri="Assets/Scripts/PlayerController.cs",
    edits=[
        {
            "startLine": 10,
            "startCol": 1,
            "endLine": 10,
            "endCol": 20,
            "newText": "public float speed = 10f;"
        }
    ],
    precondition_sha256="abc123..."  # Safety check
)
```

### 7. `script_apply_edits`
**الوصف:** تعديل structured للـ C# (methods, classes)

```python
script_apply_edits(
    uri="Assets/Scripts/GameManager.cs",
    operations=[
        {
            "type": "insert_method",
            "anchor": "end_of_class:GameManager",
            "code": """
                public void RestartGame() {
                    SceneManager.LoadScene(SceneManager.GetActiveScene().name);
                }
            """
        }
    ]
)
```

### 8. `validate_script`
**الوصف:** Validate C# script قبل/بعد التعديل

```python
validate_script(
    file_path="Assets/Scripts/PlayerController.cs",
    validation_level="standard"  # basic | standard | strict
)

# Returns:
# {
#     "success": True,
#     "errors": [],
#     "warnings": []
# }
```

**Validation Levels:**
- **basic**: Syntax only
- **standard**: Syntax + basic semantic checks
- **strict**: Full Roslyn compiler (requires Microsoft.CodeAnalysis)

### 9. `create_script`
**الوصف:** إنشاء C# script جديد

```python
create_script(
    uri="Assets/Scripts/EnemyAI.cs",
    content="""
using UnityEngine;

public class EnemyAI : MonoBehaviour {
    void Start() {
        // Initialization
    }
}
    """
)
```

### 10. `delete_script`
**الوصف:** حذف C# script

```python
delete_script(uri="Assets/Scripts/OldScript.cs")
```

### 11. `get_sha`
**الوصف:** الحصول على SHA256 hash للـ script

```python
result = get_sha(uri="Assets/Scripts/PlayerController.cs")

# Returns:
# {
#     "sha256": "abc123...",
#     "file_size": 1234,
#     "last_modified": "2025-11-21T12:00:00Z"
# }
```

### 12. `manage_editor`
**الوصف:** التحكم في Unity Editor state

```python
# Enter play mode
manage_editor(action="enter_play_mode")

# Exit play mode
manage_editor(action="exit_play_mode")

# Pause
manage_editor(action="pause")
```

### 13. `read_console`
**الوصف:** قراءة console logs

```python
logs = read_console(
    log_type="Error",  # Error | Warning | Log
    limit=10
)

# Clear console
read_console(action="clear")
```

### 14. `run_tests`
**الوصف:** تشغيل Unity tests

```python
run_tests(
    test_mode="EditMode",  # EditMode | PlayMode
    filter="PlayerTests"
)
```

### 15. `set_active_instance`
**الوصف:** تحديد Unity instance للعمل عليه

```python
set_active_instance(instance_name="MyGame@abc123")
```

---

## 📚 الموارد المتاحة (12 Resources)

Resources هي read-only data من Unity Editor

### 1. `unity_instances`
**الوصف:** قائمة بكل Unity instances الشغالة

```json
{
  "instances": [
    {
      "id": "MyGame@abc123",
      "name": "MyGame",
      "hash": "abc123",
      "path": "/path/to/project",
      "port": 53000,
      "status": "connected"
    }
  ]
}
```

### 2. `editor_state`
**الوصف:** حالة Editor الحالية

```json
{
  "isPlaying": false,
  "isPaused": false,
  "isCompiling": false,
  "activeScene": "Assets/Scenes/MainMenu.unity",
  "selection": ["Player", "Camera"]
}
```

### 3. `project_info`
**الوصف:** معلومات عن Unity project

```json
{
  "name": "MyGame",
  "path": "/path/to/project",
  "unityVersion": "2021.3.25f1",
  "platform": "StandaloneWindows64"
}
```

### 4. `menu_items`
**الوصف:** كل menu items المتاحة

```json
{
  "menus": [
    "File/Save Project",
    "File/Build Settings",
    "GameObject/Create Empty",
    "GameObject/3D Object/Cube",
    "Window/Package Manager"
  ]
}
```

### 5. `tests`
**الوصف:** كل tests المتاحة

```json
{
  "tests": [
    {
      "name": "PlayerTests",
      "type": "EditMode",
      "methods": ["TestMovement", "TestJump"]
    }
  ]
}
```

### 6. `editor_selection`
**الوصف:** الأشياء المختارة حالياً

```json
{
  "selected": [
    {
      "name": "Player",
      "type": "GameObject",
      "path": "Player",
      "components": ["Transform", "Rigidbody", "PlayerController"]
    }
  ]
}
```

### 7. `editor_active_tool`
**الوصف:** الأداة النشطة حالياً

```json
{
  "tool": "Move",  // Move | Rotate | Scale | Rect
  "pivot": "Center",
  "space": "World"
}
```

### 8. `editor_prefab_stage`
**الوصف:** Prefab editing context (إذا كان prefab مفتوح)

```json
{
  "isOpen": true,
  "prefabPath": "Assets/Prefabs/Player.prefab"
}
```

### 9. `editor_windows`
**الوصف:** كل windows المفتوحة

```json
{
  "windows": [
    {
      "title": "Scene",
      "type": "SceneView",
      "position": {"x": 0, "y": 0, "width": 800, "height": 600},
      "focused": true
    }
  ]
}
```

### 10. `project_layers`
**الوصف:** كل layers في المشروع

```json
{
  "layers": [
    {"index": 0, "name": "Default"},
    {"index": 1, "name": "TransparentFX"},
    {"index": 8, "name": "Player"},
    {"index": 9, "name": "Enemy"}
  ]
}
```

### 11. `project_tags`
**الوصف:** كل tags في المشروع

```json
{
  "tags": [
    "Untagged",
    "Player",
    "Enemy",
    "Collectible"
  ]
}
```

---

## ⚙️ كيف يعمل النظام

### Flow الكامل

```
1. User → AI Assistant (Claude/Cursor)
   "Create a player with movement script"

2. AI Assistant → MCP Client
   Decides to use Unity MCP tools

3. MCP Client → MCP Server (Python)
   Via stdio transport
   {
     "tool": "create_script",
     "params": {...}
   }

4. MCP Server → Unity Editor
   Via WebSocket (port 53000+)
   {
     "command": "manage_script",
     "data": {
       "action": "create",
       ...
     }
   }

5. Unity Editor → MCPForUnity Plugin (C#)
   Executes command using Unity API
   - Creates file in Assets/
   - Refreshes AssetDatabase
   - Compiles script

6. Unity Editor → MCP Server
   Returns result via WebSocket
   {
     "success": true,
     "data": {...}
   }

7. MCP Server → MCP Client
   Returns result via stdio

8. AI Assistant → User
   "✅ Created PlayerController.cs"
```

### WebSocket Protocol

```python
# Message format:
{
    "command": "manage_script",
    "data": {
        "action": "create",
        "name": "PlayerController",
        "path": "Assets/Scripts",
        "content": "..."
    }
}

# Response format:
{
    "success": true,
    "message": "Script created successfully",
    "data": {
        "path": "Assets/Scripts/PlayerController.cs",
        "sha256": "abc123..."
    }
}
```

### Session Management

```python
# كل MCP Client session له Unity instance خاصة به
# يتم التوجيه عن طريق middleware:

class UnityInstanceMiddleware:
    def __init__(self):
        self.session_instances = {}

    async def __call__(self, request, call_next):
        session_id = request.context.session_id
        instance_id = self.session_instances.get(session_id)

        # Inject instance_id into request context
        request.context.unity_instance = instance_id

        response = await call_next(request)
        return response
```

### Multi-Instance Support

```python
# يمكن تشغيل عدة Unity instances في نفس الوقت:
# - ProjectA@abc123 على port 53000
# - ProjectB@def456 على port 53001

# للتبديل:
set_active_instance(instance_name="ProjectA@abc123")

# كل الأدوات بعد كده توجه لـ ProjectA
```

---

## 💡 فرص التطوير

### 1. إضافة AI Code Generation Tool ⭐⭐⭐⭐⭐

**الفكرة:** أداة تستخدم AI models مباشرة لتوليد scripts

```python
# New tool: ai_code_generation.py

@mcp_for_unity_tool
async def ai_code_generation(
    ctx: Context,
    prompt: str,
    model: Literal["claude-opus", "gemini-2.5-pro", "gpt-4"] = "claude-opus",
    script_type: Literal["monobehaviour", "scriptableobject", "editor"] = "monobehaviour",
    validate: bool = True
) -> dict:
    """
    Generate C# Unity script using AI

    Args:
        prompt: Description of what the script should do
        model: AI model to use
        script_type: Type of Unity script
        validate: Validate before returning

    Returns:
        {
            "success": True,
            "code": "...",
            "file_path": "Assets/Scripts/Generated/...",
            "validation": {...}
        }
    """

    # 1. Generate code with AI
    code = await generate_with_ai(prompt, model, script_type)

    # 2. Validate
    if validate:
        validation = await validate_csharp(code)
        if not validation["success"]:
            # Retry with error feedback
            code = await generate_with_ai(
                f"{prompt}\n\nPrevious attempt had errors:\n{validation['errors']}",
                model
            )

    # 3. Create file
    file_path = f"Assets/Scripts/Generated/{generate_name(prompt)}.cs"
    result = await create_script(ctx, file_path, code)

    return {
        "success": True,
        "code": code,
        "file_path": file_path,
        "validation": validation,
        "model_used": model
    }
```

**Use Cases:**
```python
# Generate player controller
ai_code_generation(
    prompt="Player controller with WASD movement, jump, and ground check",
    model="claude-opus"
)

# Generate enemy AI
ai_code_generation(
    prompt="Enemy AI that patrols between waypoints and chases player when in range",
    model="gemini-2.5-pro"
)

# Generate UI controller
ai_code_generation(
    prompt="UI Manager with fade in/out for panels",
    model="gpt-4"
)
```

**Benefits:**
- ⚡ أسرع من كتابة الكود يدوياً
- 🎯 مخصص للـ prompt
- ✅ Validation تلقائية
- 🔄 Retry with feedback

### 2. إضافة Asset Generation Tools ⭐⭐⭐⭐⭐

**الفكرة:** أدوات لتوليد assets (3D, textures, audio)

```python
# New tool: meshy_generate_3d.py

@mcp_for_unity_tool
async def meshy_generate_3d(
    ctx: Context,
    prompt: str,
    art_style: Literal["realistic", "lowpoly", "stylized"] = "lowpoly",
    output_format: Literal["fbx", "obj", "glb"] = "fbx",
    import_to_unity: bool = True
) -> dict:
    """
    Generate 3D model using Meshy AI

    Args:
        prompt: Description of 3D model
        art_style: Visual style
        output_format: 3D file format
        import_to_unity: Auto-import to Unity
    """

    # 1. Call Meshy API
    model_url = await meshy_api.generate(
        prompt=prompt,
        style=art_style,
        format=output_format
    )

    # 2. Download model
    model_path = await download_file(model_url, "/tmp/model.fbx")

    # 3. Import to Unity
    if import_to_unity:
        result = await manage_asset(
            ctx,
            operation="import",
            asset_path=f"Models/Generated/{prompt[:30]}.fbx",
            source_path=model_path
        )

    return result

# Similar tools:
# - suno_generate_music()
# - elevenlabs_generate_voice()
# - leonardo_generate_texture()
# - stability_generate_image()
```

### 3. إضافة Orchestrator Mode ⭐⭐⭐⭐⭐

**الفكرة:** أداة واحدة تنفذ workflow كامل (GDD → Game)

```python
# New tool: orchestrator_mode.py

@mcp_for_unity_tool
async def orchestrator_mode(
    ctx: Context,
    gdd: dict,
    enable_asset_generation: bool = True,
    ai_model: str = "claude-opus"
) -> dict:
    """
    Execute complete game development workflow

    Steps:
    1. Create project structure
    2. Generate all scripts
    3. Generate assets (if enabled)
    4. Build scenes
    5. Create prefabs
    6. Validate everything

    Args:
        gdd: Game Design Document (JSON)
        enable_asset_generation: Generate 3D/audio assets
        ai_model: AI model for code generation

    Returns:
        Complete execution result with all files generated
    """

    results = {
        "success": False,
        "steps_completed": [],
        "files_generated": [],
        "errors": []
    }

    try:
        # Step 1: Project structure
        await create_project_structure(ctx, gdd)
        results["steps_completed"].append("project_structure")

        # Step 2: Generate scripts
        scripts = []
        for script_spec in gdd["technical_requirements"]["scripts"]:
            code = await ai_code_generation(
                ctx,
                prompt=script_spec["description"],
                model=ai_model
            )
            scripts.append(code)
        results["files_generated"].extend(scripts)
        results["steps_completed"].append("scripts")

        # Step 3: Generate assets
        if enable_asset_generation:
            for asset_spec in gdd["asset_requirements"]["3d_models"]:
                asset = await meshy_generate_3d(
                    ctx,
                    prompt=asset_spec["description"]
                )
                results["files_generated"].append(asset)
        results["steps_completed"].append("assets")

        # Step 4: Build scenes
        for scene_spec in gdd["technical_requirements"]["scenes"]:
            await manage_scene(
                ctx,
                action="create",
                scene_path=f"Assets/Scenes/{scene_spec['name']}.unity"
            )
        results["steps_completed"].append("scenes")

        # Step 5: Validate
        validation = await validate_all_scripts(ctx)
        results["steps_completed"].append("validation")

        results["success"] = True

    except Exception as e:
        results["errors"].append(str(e))

    return results
```

### 4. إضافة Pipeline Recorder ⭐⭐⭐⭐

**الفكرة:** تسجيل سلسلة commands وإعادة تشغيلها

```python
# New tool: pipeline_recorder.py

pipelines = {}  # In-memory storage

@mcp_for_unity_tool
async def record_pipeline_start(
    ctx: Context,
    pipeline_name: str,
    description: str = ""
):
    """Start recording a pipeline"""
    pipelines[pipeline_name] = {
        "name": pipeline_name,
        "description": description,
        "commands": [],
        "recording": True
    }

@mcp_for_unity_tool
async def record_pipeline_stop(
    ctx: Context,
    pipeline_name: str
):
    """Stop recording and save pipeline"""
    pipeline = pipelines.get(pipeline_name)
    if pipeline:
        pipeline["recording"] = False
        # Save to file
        save_pipeline(pipeline)

@mcp_for_unity_tool
async def replay_pipeline(
    ctx: Context,
    pipeline_name: str,
    parameters: dict = None
):
    """Replay a recorded pipeline"""
    pipeline = load_pipeline(pipeline_name)

    for command in pipeline["commands"]:
        # Replace parameters if provided
        if parameters:
            command = replace_parameters(command, parameters)

        # Execute command
        await execute_command(ctx, command)
```

**Use Case:**
```python
# Record creating a character
record_pipeline_start("create_character", "Complete character setup")
# ... do actions in Unity ...
record_pipeline_stop("create_character")

# Replay with different parameters
replay_pipeline("create_character", {
    "name": "Enemy",
    "health": 50,
    "speed": 3.0
})
```

### 5. إضافة Steam Integration ⭐⭐⭐⭐

**الفكرة:** رفع Build على Steam مباشرة

```python
# New tool: steam_upload.py

@mcp_for_unity_tool
async def steam_upload(
    ctx: Context,
    app_id: str,
    build_path: str,
    depot_id: str,
    username: str = None,
    password: str = None
):
    """
    Upload build to Steam using SteamCMD

    Args:
        app_id: Steam App ID
        build_path: Path to built game
        depot_id: Steam Depot ID
        username: Steam username (or from env)
        password: Steam password (or from env)
    """

    # 1. Create VDF files
    create_app_build_vdf(app_id, depot_id)
    create_depot_build_vdf(depot_id, build_path)

    # 2. Run SteamCMD
    cmd = f"steamcmd +login {username} {password} +run_app_build app_build_{app_id}.vdf +quit"
    result = await run_command(cmd)

    return {
        "success": result.returncode == 0,
        "output": result.stdout
    }
```

### 6. إضافة Testing Tools ⭐⭐⭐

**الفكرة:** أدوات testing متقدمة

```python
# New tool: advanced_testing.py

@mcp_for_unity_tool
async def generate_tests(
    ctx: Context,
    script_path: str,
    test_type: Literal["unit", "integration"] = "unit"
):
    """
    Generate test file for a script

    Analyzes the script and generates appropriate tests
    """

    # 1. Read script
    script = await read_script(ctx, script_path)

    # 2. Analyze methods
    methods = parse_methods(script)

    # 3. Generate tests with AI
    tests = await ai_code_generation(
        ctx,
        prompt=f"Generate {test_type} tests for:\n{script}",
        model="claude-opus",
        script_type="editor"
    )

    return tests

@mcp_for_unity_tool
async def run_tests_with_coverage(
    ctx: Context,
    filter: str = None
):
    """Run tests and return code coverage"""
    # Implementation
```

---

## 📋 خطة التطوير المقترحة

### Phase 1: AI Code Generation (أسبوع واحد)

**الأهداف:**
- [ ] إضافة `ai_code_generation` tool
- [ ] دعم 3 models (Claude Opus, Gemini 2.5 Pro, GPT-4)
- [ ] Validation تلقائية
- [ ] Retry with feedback

**الملفات:**
```
Server/tools/
├── ai_code_generation.py  (NEW)
└── ai_providers/          (NEW)
    ├── __init__.py
    ├── claude.py
    ├── gemini.py
    └── openai.py
```

**Code Structure:**
```python
# ai_providers/claude.py
class ClaudeProvider:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    async def generate(self, prompt: str, temperature: float = 0.7):
        response = self.client.messages.create(
            model="claude-3-5-opus-20241022",
            max_tokens=4000,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
```

### Phase 2: Asset Generation (أسبوعين)

**الأهداف:**
- [ ] إضافة `meshy_generate_3d` tool
- [ ] إضافة `suno_generate_music` tool
- [ ] إضافة `elevenlabs_generate_voice` tool
- [ ] Auto-import إلى Unity

**الملفات:**
```
Server/tools/
├── meshy_generate_3d.py     (NEW)
├── suno_generate_music.py   (NEW)
└── elevenlabs_generate_voice.py (NEW)
```

### Phase 3: Orchestrator Mode (3 أسابيع)

**الأهداف:**
- [ ] إضافة `orchestrator_mode` tool
- [ ] 7 steps automation
- [ ] Integration مع AI code generation
- [ ] Integration مع asset generation
- [ ] Validation شاملة

**الملفات:**
```
Server/tools/
└── orchestrator_mode.py     (NEW - 500+ lines)
```

### Phase 4: Pipeline Recorder (أسبوعين)

**الأهداف:**
- [ ] Record/replay system
- [ ] Parameter replacement
- [ ] Pipeline marketplace (optional)

### Phase 5: Steam Integration (أسبوع واحد)

**الأهداف:**
- [ ] SteamCMD integration
- [ ] VDF generation
- [ ] Multi-platform builds

---

## ✅ الخلاصة

### ما تعلمته

1. ✅ Unity MCP هو bridge قوي بين AI و Unity
2. ✅ Architecture نظيف: Python server + C# Unity plugin
3. ✅ 14 tools متاحة حالياً
4. ✅ 12 resources للقراءة
5. ✅ WebSocket protocol للاتصال
6. ✅ Multi-instance support
7. ✅ Session-based routing
8. ✅ Telemetry (anonymous)

### فرص التطوير الكبيرة

1. 🌟 **AI Code Generation** - أهم شيء!
2. 🌟 **Asset Generation** - Meshy, Suno, ElevenLabs
3. 🌟 **Orchestrator Mode** - GDD → Complete Game
4. 🌟 **Pipeline Recorder** - Reusable workflows
5. 🌟 **Steam Integration** - Auto-upload

### Next Steps

1. ✅ Fork المشروع
2. ✅ Setup development environment
3. ✅ Implement AI Code Generation (Phase 1)
4. ✅ Test thoroughly
5. ✅ Submit PR
6. ✅ Move to Phase 2

---

**🚀 جاهز للبدء في التطوير!**

*آخر تحديث: 2025-11-21*
