# GameOS AI - Open Source Unity AI Assistant

<div align="center">

![GameOS AI Logo](docs/images/logo.png)

**The Open Source Alternative to Coplay**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Unity 2022.3+](https://img.shields.io/badge/Unity-2022.3+-black.svg)](https://unity.com/)
[![MCP](https://badge.mcpx.dev?status=on)](https://modelcontextprotocol.io/introduction)

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Examples](#-examples)

</div>

---

## 🎯 What is GameOS AI?

**GameOS AI** is a fully open-source Unity AI assistant that brings professional game development automation to everyone. Built on Unity MCP and extended with premium features inspired by Coplay, it offers:

✨ **Orchestrator Mode** - Automated game development from simple plan files
🎨 **Asset Generation** - AI-powered 3D models, textures, and images
📝 **Pipeline Recording** - Record and replay your workflows
🤖 **Multi-Model AI** - GPT-4, Claude, Gemini, and local models
✅ **Progress Tracking** - Built-in todo lists and progress bars
🎮 **Professional UI** - Sleek Unity Editor integration

**And it's 100% free and open source!** 🎉

---

## ✨ Features

### 🎯 Core Features (Unity MCP Base)

- **14 Unity Tools** - Full control over scenes, GameObjects, scripts, and more
- **12 Unity Resources** - Access editor state, project info, and hierarchy
- **WebSocket Bridge** - Seamless communication between Unity and AI
- **Multi-Instance Support** - Work with multiple Unity editors simultaneously

### 🆕 Premium Features (GameOS Extensions)

#### 🎭 Orchestrator Mode
Automate entire game projects from markdown files:

```markdown
# My Platformer Game

## Assets
- [ ] {3d_model} Generate player character: "cute robot with blue armor"
- [ ] {texture} Generate ground texture: "grass field with flowers"

## Scripts
- [ ] {script} PlayerController: WASD movement + Space jump
- [ ] {script} CameraFollow: smooth third-person camera

## Scenes
- [ ] {scene} MainLevel: create with lighting and spawn points
```

**Result:** Complete game created automatically! 🚀

#### 🎨 Asset Generation

- **3D Models** via Meshy API - From text or images
- **Textures** - Any style, any resolution
- **Images** - UI elements, concept art
- **Automatic Import** - Directly into your Unity project

#### 🤖 Multi-Model AI

Choose the right AI for each task:
- **GPT-4** - Best for creative content
- **Claude Sonnet** - Best for code generation
- **Gemini 2.5 Pro** - Fast and cost-effective
- **Local Models** - Use Ollama for privacy

#### 📹 Pipeline Recording

Record your workflows once, replay them infinite times:
1. Click "Start Recording"
2. Perform Unity operations
3. Save pipeline
4. Replay with different parameters

Perfect for:
- Asset import workflows
- Scene setup routines
- Build pipelines
- Testing sequences

---

## 📦 Installation

### Prerequisites

- **Python** 3.10 or newer - [Download](https://www.python.org/downloads/)
- **Unity** 2022.3 LTS or newer - [Download](https://unity.com/download)
- **uv** (Python package manager) - [Install Guide](https://docs.astral.sh/uv/getting-started/installation/)

### Step 1: Install Python Backend

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Game-OS.git
cd Game-OS

# Install with uv
uv sync

# Run the server
uv run ai_game_dev/core/server.py
```

### Step 2: Install Unity Plugin

1. Open your Unity project
2. Go to **Window → Package Manager**
3. Click **+** → **Add package from git URL**
4. Enter:
   ```
   https://github.com/YOUR_USERNAME/Game-OS.git?path=/unity_plugin
   ```
5. Click **Add**

### Step 3: Configure API Keys (Optional)

For asset generation features, add API keys to `~/.gameos/config.json`:

```json
{
  "meshy_api_key": "your_meshy_key_here",
  "openai_api_key": "your_openai_key_here",
  "anthropic_api_key": "your_anthropic_key_here"
}
```

---

## 🚀 Quick Start

### Basic Usage

1. **Open Unity** and your project
2. **Open GameOS AI**: `Window → GameOS AI` or press `Ctrl+G` (Cmd+G on Mac)
3. **Start chatting!**

**Example:**
```
You: "Create a red cube that rotates"
GameOS: *creates rotating red cube in your scene*
```

### Orchestrator Mode

1. Create `Assets/GamePlan.md`:
```markdown
# Simple Game

## Scene Setup
- [ ] {scene} MainScene: create with directional light
- [ ] {gameobject} Ground: create plane at (0,0,0)

## Player
- [ ] {3d_model} Player: "small robot character"
- [ ] {script} PlayerController: simple movement
```

2. In GameOS AI window:
   - Select **Orchestrator Mode**
   - Click **Execute Plan**
   - Watch the magic happen! ✨

---

## 📚 Documentation

- [**Getting Started Guide**](docs/GETTING_STARTED.md)
- [**Orchestrator Mode**](docs/ORCHESTRATOR_MODE.md)
- [**Asset Generation**](docs/ASSET_GENERATION.md)
- [**Pipeline Recording**](docs/PIPELINE_RECORDING.md)
- [**API Reference**](docs/API_REFERENCE.md)
- [**Architecture**](SYSTEM_ARCHITECTURE.md)

---

## 🎮 Examples

Check out complete example projects in [`examples/`](examples/):

- **Simple Platformer** - 2D platformer with player, enemies, collectibles
- **Racing Game** - 3D racing with car physics and track generation
- **Puzzle Game** - Match-3 style puzzle with scoring

Each example includes a `GamePlan.md` that can be executed in Orchestrator Mode!

---

## 🆚 Comparison

| Feature | Coplay (Paid) | GameOS AI (Free) | Unity MCP (Free) |
|---------|---------------|------------------|------------------|
| Unity Control | ✅ | ✅ | ✅ |
| Orchestrator Mode | ✅ | ✅ | ❌ |
| Asset Generation | ✅ | ✅ | ❌ |
| Pipeline Recording | ✅ | ✅ | ❌ |
| Multi-Model AI | ✅ (4) | ✅ (4+) | ❌ |
| Local Models | ❌ | ✅ | ❌ |
| Todo Lists | ✅ | ✅ | ❌ |
| Cost Tracking | ✅ | ✅ | ❌ |
| Open Source | ❌ | ✅ | ✅ |
| Monthly Cost | $30-100 | $0 + API | $0 |

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ways to contribute:**
- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the repository!

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Unity MCP** - Built on the excellent open-source foundation by CoplayDev
- **Coplay** - Inspiration for premium features
- **Model Context Protocol** - Anthropic's MCP framework

---

## 📞 Support

- **Discord**: [Join our community](https://discord.gg/YOUR_DISCORD)
- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/Game-OS/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/Game-OS/discussions)

---

<div align="center">

**Made with ❤️ by the GameOS AI community**

[⭐ Star us on GitHub](https://github.com/YOUR_USERNAME/Game-OS) • [📖 Read the Docs](docs/) • [💬 Join Discord](https://discord.gg/YOUR_DISCORD)

</div>
