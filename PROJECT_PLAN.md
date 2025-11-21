# 🎮 AI Game Development System - Complete Implementation Plan
**Version:** 1.0.0
**Status:** Production Ready
**Last Updated:** 2025-11-21

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Architecture Overview](#architecture-overview)
4. [Directory Structure](#directory-structure)
5. [File Descriptions](#file-descriptions)
6. [Build & Run Scripts](#build--run-scripts)
7. [CI/CD Setup](#cicd-setup)
8. [Environment Configuration](#environment-configuration)
9. [Deployment Guide](#deployment-guide)
10. [Testing Strategy](#testing-strategy)

---

## 🎯 Project Overview

### Project Goal
Build a **fully automated AI-powered system** that creates complete Unity games from concept to Steam deployment using multi-agent AI architecture with minimal human intervention (95%+ automation).

### Key Objectives
1. **Automation**: Automate game development workflow from idea → design → implementation → deployment
2. **Multi-Agent System**: Coordinate specialized AI agents (Designer, Builder, Asset Generator)
3. **Asset Generation**: Generate all game assets (3D models, textures, audio, UI) via APIs
4. **Unity Integration**: Direct Unity Editor control via Model Context Protocol (MCP)
5. **Complete Pipeline**: End-to-end workflow including Steam upload

### Target Users
- Indie game developers
- Game design students
- AI researchers
- Rapid prototyping teams
- Solo developers with limited resources

### Success Metrics
- **Time Reduction**: 60-80% faster than traditional development
- **Cost Reduction**: 40-50% lower development costs
- **Automation Level**: 95%+ of tasks automated
- **Game Quality**: Indie game standard quality
- **Iteration Speed**: Prototype in days instead of weeks

---

## 🛠️ Tech Stack

### Core Technologies

#### Backend / AI Agents
| Technology | Version | Purpose | License |
|-----------|---------|---------|---------|
| Python | 3.10+ | Primary language for agents | PSF |
| Anthropic Claude API | Latest (Sonnet 4.5) | Master Agent, Designer, Asset Gen | Commercial |
| Google Gemini API | 2.0 Flash | Unity Builder Agent | Commercial |
| Unity | 2021.3 LTS+ | Game engine | Unity EULA |
| Unity MCP | Latest | Unity Editor control protocol | MIT |

#### Asset Generation APIs
| Service | Purpose | Free Tier | Pricing |
|---------|---------|-----------|---------|
| Meshy AI | 3D Model generation | 100 credits/month | ~$30/mo Pro |
| Polyhive | Texture generation | Trial | ~$30/mo |
| Suno AI | Music generation | No | ~$10/mo |
| ElevenLabs | Voice/SFX generation | Limited | ~$22/mo Creator |
| Stability AI | Image/UI generation | Trial credits | Pay per use |
| Leonardo AI | Texture generation | Limited | ~$12/mo |

#### Development Tools
```yaml
# Python Libraries
core:
  - anthropic: ^0.40.0
  - google-generativeai: ^0.8.0
  - requests: ^2.31.0
  - python-dotenv: ^1.0.0

asset_apis:
  - elevenlabs: ^1.0.0
  - Pillow: ^10.0.0

utilities:
  - asyncio: ^3.4.3
  - aiohttp: ^3.9.0
  - tqdm: ^4.66.0
  - colorlog: ^6.7.0

testing:
  - pytest: ^7.4.0
  - pytest-asyncio: ^0.21.0

optional:
  - flask: ^3.0.0  # Web interface
  - sqlalchemy: ^2.0.0  # Database
```

#### Infrastructure
- **Version Control**: Git + GitHub
- **CI/CD**: GitHub Actions
- **Build System**: Unity Build Automation + SteamCMD
- **Deployment**: Steam (via SteamCMD)
- **Monitoring**: Custom logging system

---

## 🏗️ Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INPUT                                │
│              (Game Concept via Natural Language)                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MASTER ORCHESTRATOR AGENT                      │
│                    (Claude + Computer Use)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • Concept Analysis          • Task Distribution           │  │
│  │ • Agent Coordination        • Progress Monitoring         │  │
│  │ • Computer Control (via Computer Use API)                 │  │
│  │ • Quality Assurance         • Final Integration          │  │
│  └──────────────────────────────────────────────────────────┘  │
└───┬─────────────────┬──────────────────┬────────────────────────┘
    │                 │                  │
    ▼                 ▼                  ▼
┌─────────┐      ┌─────────┐      ┌──────────────┐
│ AGENT 1 │      │ AGENT 2 │      │   AGENT 3    │
│Designer │      │ Unity   │      │    Asset     │
│(Claude) │      │Builder  │      │  Generator   │
│         │      │(Gemini) │      │   (Claude)   │
└────┬────┘      └────┬────┘      └──────┬───────┘
     │                │                   │
     │                │                   │
     ▼                ▼                   ▼
┌─────────┐   ┌──────────────┐   ┌──────────────┐
│   GDD   │   │  Unity MCP   │   │  Asset APIs  │
│  JSON   │   │   Bridge     │   │    Pool      │
└─────────┘   └──────┬───────┘   └──────┬───────┘
                     │                   │
                     ▼                   ▼
              ┌──────────────┐   ┌──────────────┐
              │Unity Editor  │   │  Generated   │
              │   Project    │   │    Assets    │
              └──────┬───────┘   └──────┬───────┘
                     │                   │
                     └────────┬──────────┘
                              ▼
                     ┌─────────────────┐
                     │  Build Pipeline │
                     │  • Unity Build  │
                     │  • SteamCMD     │
                     │  • Publishing   │
                     └────────┬────────┘
                              ▼
                     ┌─────────────────┐
                     │ Steam Platform  │
                     └─────────────────┘
```

### Component Interaction Flow

```
1. USER → Master Agent
   Input: "Create a football manager game"

2. Master Agent → Designer Agent
   Task: "Create GDD for football manager"
   Output: game_design.json

3. Master Agent → Asset Generator Agent
   Task: "Generate assets per GDD requirements"
   Output: /assets/{models,textures,audio,ui}

4. Master Agent → Unity Builder Agent
   Task: "Build game in Unity using GDD + assets"
   Output: Unity project + C# scripts

5. Unity Builder → Unity MCP → Unity Editor
   Actions: Create scenes, add scripts, import assets

6. Master Agent → Computer Use API
   Task: "Build game for Steam"
   Output: Executable builds

7. Master Agent → Steam Upload
   Task: "Upload to Steam"
   Output: Published game
```

### Agent Responsibilities

#### Master Orchestrator Agent
```python
Responsibilities:
- Parse user input
- Create execution plan
- Delegate tasks to sub-agents
- Monitor progress
- Handle errors and retries
- Computer automation (open apps, click buttons, etc.)
- Final integration and QA

Technologies:
- Claude Sonnet 4.5 (large context)
- Computer Use API
- Retry logic with exponential backoff

Input: Natural language game concept
Output: Complete game on Steam
```

#### Designer Agent
```python
Responsibilities:
- Game Design Document creation
- System architecture design
- Database schema design
- Asset requirements list
- UI/UX flow design

Technologies:
- Claude Sonnet 4.5
- JSON schema validation

Input: Game concept + requirements
Output: Comprehensive GDD (JSON)
```

#### Unity Builder Agent
```python
Responsibilities:
- Unity project creation
- C# script generation
- Scene setup
- Prefab creation
- Component configuration
- Build execution

Technologies:
- Google Gemini 2.0 Flash
- Unity MCP protocol
- Unity Scripting API

Input: GDD + Assets
Output: Complete Unity project
```

#### Asset Generator Agent
```python
Responsibilities:
- 3D model generation (Meshy AI)
- Texture creation (Polyhive, Leonardo)
- Music generation (Suno AI)
- Voice/SFX (ElevenLabs)
- UI assets (Stability AI)
- Asset optimization

Technologies:
- Claude Sonnet 4.5
- Multiple asset APIs
- Asset processing pipelines

Input: Asset requirements list
Output: Game-ready assets
```

---

## 📁 Directory Structure

```
Game-OS/
│
├── .github/                          # GitHub specific files
│   ├── workflows/                    # CI/CD workflows
│   │   ├── test.yml                 # Automated testing
│   │   ├── lint.yml                 # Code linting
│   │   └── deploy.yml               # Deployment pipeline
│   └── ISSUE_TEMPLATE/              # Issue templates
│
├── ai_game_dev/                      # Main source directory
│   │
│   ├── agents/                       # AI Agent implementations
│   │   ├── __init__.py
│   │   ├── base_agent.py            # Base agent class
│   │   ├── master_agent.py          # Master orchestrator
│   │   ├── designer_agent.py        # GDD creator
│   │   ├── unity_builder_agent.py   # Unity builder
│   │   └── asset_generator_agent.py # Asset generator
│   │
│   ├── apis/                         # API integrations
│   │   ├── __init__.py
│   │   ├── meshy_client.py          # Meshy AI wrapper
│   │   ├── polyhive_client.py       # Polyhive wrapper
│   │   ├── suno_client.py           # Suno AI wrapper
│   │   ├── elevenlabs_client.py     # ElevenLabs wrapper
│   │   ├── stability_client.py      # Stability AI wrapper
│   │   └── leonardo_client.py       # Leonardo AI wrapper
│   │
│   ├── unity/                        # Unity integration
│   │   ├── __init__.py
│   │   ├── mcp_client.py            # Unity MCP client
│   │   ├── project_manager.py       # Unity project operations
│   │   ├── script_generator.py      # C# code generation
│   │   └── build_manager.py         # Unity build operations
│   │
│   ├── computer_use/                 # Computer Use automation
│   │   ├── __init__.py
│   │   ├── controller.py            # Main controller
│   │   ├── unity_automation.py      # Unity app control
│   │   └── steam_automation.py      # Steam upload control
│   │
│   ├── utils/                        # Utility modules
│   │   ├── __init__.py
│   │   ├── logger.py                # Logging configuration
│   │   ├── config.py                # Config management
│   │   ├── validators.py            # Input validation
│   │   ├── retry.py                 # Retry logic
│   │   └── file_manager.py          # File operations
│   │
│   ├── templates/                    # Code templates
│   │   ├── unity_scripts/           # C# templates
│   │   │   ├── GameManager.template
│   │   │   ├── Player.template
│   │   │   └── UIManager.template
│   │   └── gdd_templates/           # GDD templates
│   │       ├── base_gdd.json
│   │       └── sports_game.json
│   │
│   └── schemas/                      # JSON schemas
│       ├── gdd_schema.json          # GDD validation
│       ├── asset_schema.json        # Asset requirements
│       └── config_schema.json       # Config validation
│
├── examples/                         # Example implementations
│   ├── output/                      # Generated output
│   │   └── football_manager/        # Example game output
│   ├── simple_football_manager.py   # Full example
│   ├── simple_clicker.py            # Simple game example
│   └── README.md                    # Examples documentation
│
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── unit/                        # Unit tests
│   │   ├── test_agents.py
│   │   ├── test_apis.py
│   │   └── test_utils.py
│   ├── integration/                 # Integration tests
│   │   ├── test_workflow.py
│   │   └── test_unity_integration.py
│   └── fixtures/                    # Test fixtures
│       └── sample_data.json
│
├── scripts/                          # Utility scripts
│   ├── install_unity_mcp.sh        # Unity MCP setup
│   ├── download_assets.py          # Asset downloader
│   ├── validate_env.py             # Environment validator
│   └── steam_upload.sh             # Steam upload script
│
├── configs/                          # Configuration files
│   ├── default_config.yaml         # Default settings
│   ├── dev_config.yaml             # Development settings
│   ├── prod_config.yaml            # Production settings
│   └── logging_config.yaml         # Logging configuration
│
├── docs/                             # Documentation
│   ├── api/                         # API documentation
│   │   ├── agents.md
│   │   ├── apis.md
│   │   └── unity.md
│   ├── guides/                      # User guides
│   │   ├── getting_started.md
│   │   ├── advanced_usage.md
│   │   └── troubleshooting.md
│   └── architecture/                # Architecture docs
│       ├── system_design.md
│       └── agent_design.md
│
├── unity-mcp/                        # Unity MCP submodule
│   └── (cloned from justinpbarnett/unity-mcp)
│
├── .env.example                      # Environment template
├── .env                             # Environment variables (gitignored)
├── .gitignore                       # Git ignore rules
├── requirements.txt                 # Python dependencies
├── requirements-dev.txt             # Dev dependencies
├── setup.py                         # Package setup
├── setup.sh                         # Automated setup script
├── pytest.ini                       # Pytest configuration
├── .pylintrc                        # Pylint configuration
├── .dockerignore                    # Docker ignore (optional)
├── Dockerfile                       # Docker container (optional)
├── docker-compose.yml               # Docker compose (optional)
│
├── AI_GAME_DEVELOPMENT_MASTER_PLAN.md  # Master plan
├── QUICK_START_GUIDE.md             # Quick start guide
├── PROJECT_PLAN.md                  # This file
├── README.md                        # Main README
├── CONTRIBUTING.md                  # Contribution guidelines
├── LICENSE                          # MIT License
└── CHANGELOG.md                     # Version changelog
```

---

## 📄 File Descriptions

### Core Agent Files

#### `ai_game_dev/agents/base_agent.py`
```python
"""
Base Agent Class
================
Abstract base class for all AI agents.

Purpose:
- Define common agent interface
- Handle API communication
- Implement retry logic
- Error handling
- Logging

Key Methods:
- execute(task): Main execution method
- validate_input(data): Input validation
- handle_error(error): Error handling
- log_progress(message): Progress logging

Dependencies:
- anthropic
- google.generativeai
- utils.logger
- utils.retry
"""
```

#### `ai_game_dev/agents/master_agent.py`
```python
"""
Master Orchestrator Agent
==========================
Main coordinator for the entire system.

Purpose:
- Parse user input
- Create execution plan
- Delegate tasks to sub-agents
- Monitor progress
- Computer Use API integration
- Final QA and integration

Key Methods:
- analyze_concept(prompt): Parse game idea
- create_execution_plan(concept): Build task plan
- orchestrate(plan): Coordinate all agents
- integrate_results(): Combine all outputs
- deploy_to_steam(): Upload to Steam

APIs Used:
- Claude Sonnet 4.5
- Computer Use API

Input: User game concept (string)
Output: Complete game (Steam link)
"""
```

#### `ai_game_dev/agents/designer_agent.py`
```python
"""
Game Designer Agent
===================
Creates comprehensive Game Design Documents.

Purpose:
- Analyze game concept
- Create GDD structure
- Define game systems
- Specify asset requirements
- Design UI/UX flow

Key Methods:
- create_gdd(concept): Generate GDD
- define_systems(concept): System design
- create_asset_list(gdd): Asset requirements
- validate_gdd(gdd): GDD validation

APIs Used:
- Claude Sonnet 4.5

Input: Game concept
Output: game_design_document.json
"""
```

#### `ai_game_dev/agents/unity_builder_agent.py`
```python
"""
Unity Builder Agent
===================
Builds complete Unity projects.

Purpose:
- Create Unity projects
- Generate C# scripts
- Setup scenes and prefabs
- Import assets
- Configure build settings
- Execute builds

Key Methods:
- create_project(name): New Unity project
- generate_script(spec): C# script generation
- setup_scene(spec): Scene configuration
- import_assets(paths): Asset import
- build_game(platform): Build execution

APIs Used:
- Google Gemini 2.0 Flash
- Unity MCP

Input: GDD + Assets
Output: Unity project + builds
"""
```

#### `ai_game_dev/agents/asset_generator_agent.py`
```python
"""
Asset Generator Agent
=====================
Generates all game assets via APIs.

Purpose:
- Generate 3D models
- Create textures
- Generate music
- Create SFX and voices
- Generate UI assets
- Optimize assets

Key Methods:
- generate_3d_model(spec): 3D generation
- generate_texture(spec): Texture creation
- generate_music(spec): Music generation
- generate_voice(spec): Voice/SFX
- optimize_asset(path): Asset optimization

APIs Used:
- Meshy AI
- Polyhive
- Suno AI
- ElevenLabs
- Stability AI
- Leonardo AI

Input: Asset requirements list
Output: Game-ready assets
"""
```

### API Integration Files

#### `ai_game_dev/apis/meshy_client.py`
```python
"""
Meshy AI Client
===============
Wrapper for Meshy AI 3D model generation API.

Purpose:
- Text-to-3D generation
- Image-to-3D generation
- Model downloading
- Format conversion

Key Methods:
- text_to_3d(prompt, style): Generate from text
- image_to_3d(image_path): Generate from image
- get_model_status(id): Check generation status
- download_model(id, format): Download model

API Endpoints:
- POST /v1/text-to-3d
- POST /v1/image-to-3d
- GET /v1/models/{id}

Supported Formats: GLB, FBX, OBJ, USDZ
Rate Limits: Based on subscription tier
"""
```

### Unity Integration Files

#### `ai_game_dev/unity/mcp_client.py`
```python
"""
Unity MCP Client
================
Client for Unity Model Context Protocol.

Purpose:
- Connect to Unity Editor
- Send commands to Unity
- Receive Unity responses
- Handle Unity operations

Key Methods:
- connect(): Establish connection
- send_command(cmd): Send Unity command
- create_gameobject(spec): Create object
- add_component(obj, component): Add component
- execute_script(code): Run C# code

Protocol: WebSocket (port 3000)
Unity Plugin Required: Yes

Based on: justinpbarnett/unity-mcp
"""
```

### Utility Files

#### `ai_game_dev/utils/logger.py`
```python
"""
Logging Configuration
=====================
Centralized logging system.

Purpose:
- Configure logging levels
- File and console output
- Colored console output
- Log rotation
- Performance tracking

Features:
- Multi-level logging (DEBUG, INFO, WARNING, ERROR)
- Separate log files per agent
- Console output with colors
- Automatic log rotation (10MB max)
- Performance metrics logging

Configuration: configs/logging_config.yaml
"""
```

#### `ai_game_dev/utils/config.py`
```python
"""
Configuration Management
========================
Load and manage configuration.

Purpose:
- Load config from YAML
- Environment variable override
- Config validation
- Default values

Key Methods:
- load_config(env): Load config for environment
- get(key, default): Get config value
- validate(): Validate configuration
- merge_configs(): Merge multiple configs

Supported Environments: dev, staging, prod
Config Files: configs/
"""
```

### Build & Deployment Files

#### `scripts/steam_upload.sh`
```bash
#!/bin/bash
# Steam Upload Script
# Purpose: Upload game builds to Steam using SteamCMD
# Requirements: SteamCMD installed
# Usage: ./steam_upload.sh <app_id> <build_path> <depot_id>

# Features:
# - Automatic SteamCMD download if missing
# - Build validation
# - VDF file generation
# - Multi-platform support
# - Upload progress tracking
# - Error handling and retry

# Environment Variables Required:
# - STEAM_USERNAME
# - STEAM_PASSWORD
# - STEAM_APP_ID (optional, can pass as arg)
```

---

## 🚀 Build & Run Scripts

### Development Setup

#### `setup.sh` - Complete Setup
```bash
#!/bin/bash
# Complete System Setup
# Installs everything needed to run the system

Features:
✅ Python environment setup
✅ Dependency installation
✅ Unity MCP clone & setup
✅ Directory structure creation
✅ Environment file template
✅ Configuration files
✅ Test execution

Usage:
./setup.sh

Time: ~5-10 minutes
Requirements: Python 3.10+, Git
```

### Running the System

#### Option 1: Quick Example
```bash
# Activate environment
source venv/bin/activate

# Run simple example
python examples/simple_football_manager.py

# Output: examples/output/football_manager/
```

#### Option 2: Full System
```bash
# Activate environment
source venv/bin/activate

# Run full system
python -m ai_game_dev.main create-game \
  --concept "Football manager game" \
  --output "./output/my_game" \
  --deploy-steam true
```

#### Option 3: Interactive Mode
```bash
# Start interactive CLI
python -m ai_game_dev.cli

# Follow prompts:
# 1. Enter game concept
# 2. Configure options
# 3. Monitor progress
# 4. Review outputs
```

### Build Scripts

#### `scripts/build_game.sh`
```bash
#!/bin/bash
# Build Game Script
# Purpose: Build Unity game for multiple platforms

Usage:
./scripts/build_game.sh <unity_project_path> <platform>

Platforms:
- windows   (Windows 64-bit)
- mac       (MacOS)
- linux     (Linux 64-bit)
- all       (All platforms)

Example:
./scripts/build_game.sh ./output/my_game/Unity windows

Output:
./output/my_game/builds/Windows/
```

#### `scripts/deploy.sh`
```bash
#!/bin/bash
# Deployment Script
# Purpose: Complete deployment pipeline

Steps:
1. Build game for target platform
2. Generate Steam VDF files
3. Upload to Steam via SteamCMD
4. Verify upload
5. Set live branch

Usage:
./scripts/deploy.sh <app_id> <project_path>

Example:
./scripts/deploy.sh 123456 ./output/my_game

Environment:
Requires STEAM_USERNAME and STEAM_PASSWORD
```

### Testing Scripts

#### `scripts/run_tests.sh`
```bash
#!/bin/bash
# Test Runner
# Purpose: Run full test suite

Test Types:
- Unit tests (fast)
- Integration tests (medium)
- E2E tests (slow)

Usage:
./scripts/run_tests.sh [type]

Examples:
./scripts/run_tests.sh unit        # Unit tests only
./scripts/run_tests.sh integration # Integration only
./scripts/run_tests.sh all         # All tests
./scripts/run_tests.sh             # All tests (default)

Coverage Report: tests/coverage/
```

---

## ⚙️ CI/CD Setup

### GitHub Actions Workflows

#### `.github/workflows/test.yml`
```yaml
name: Test Suite

on:
  push:
    branches: [ main, develop, claude/* ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10, 3.11, 3.12]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Run linting
      run: |
        pylint ai_game_dev/

    - name: Run unit tests
      run: |
        pytest tests/unit/ -v --cov=ai_game_dev

    - name: Run integration tests
      run: |
        pytest tests/integration/ -v
      env:
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
```

#### `.github/workflows/lint.yml`
```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install linting tools
      run: |
        pip install pylint black flake8 mypy

    - name: Run Black (formatting check)
      run: black --check ai_game_dev/

    - name: Run Flake8
      run: flake8 ai_game_dev/ --max-line-length=100

    - name: Run Pylint
      run: pylint ai_game_dev/ --rcfile=.pylintrc

    - name: Run MyPy (type checking)
      run: mypy ai_game_dev/ --ignore-missing-imports
```

#### `.github/workflows/deploy.yml`
```yaml
name: Deploy to Production

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Build package
      run: |
        python -m pip install --upgrade pip
        pip install build
        python -m build

    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}

    - name: Create GitHub Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        draft: false
        prerelease: false
```

### Pre-commit Hooks

#### `.pre-commit-config.yaml`
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.10

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=100']

  - repo: https://github.com/pycqa/pylint
    rev: v3.0.0
    hooks:
      - id: pylint
        args: ['--rcfile=.pylintrc']

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

---

## 🔐 Environment Configuration

### `.env.example` Template
```bash
# ============================================
# AI Game Development System - Environment Variables
# ============================================

# --------------------------------------------
# AI API Keys
# --------------------------------------------
# Get from: https://console.anthropic.com
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Get from: https://aistudio.google.com/app/apikey
GOOGLE_API_KEY=your-gemini-key-here

# --------------------------------------------
# Asset Generation APIs
# --------------------------------------------
# Get from: https://www.meshy.ai
MESHY_API_KEY=your-meshy-key-here

# Get from: https://polyhive.ai
POLYHIVE_API_KEY=your-polyhive-key-here

# Get from: https://sunoapi.org
SUNO_API_KEY=your-suno-key-here

# Get from: https://elevenlabs.io
ELEVENLABS_API_KEY=your-elevenlabs-key-here

# Get from: https://platform.stability.ai
STABILITY_API_KEY=your-stability-key-here

# Get from: https://leonardo.ai
LEONARDO_API_KEY=your-leonardo-key-here

# --------------------------------------------
# Unity Configuration
# --------------------------------------------
# Path to Unity projects folder
UNITY_PROJECT_PATH=/home/user/Unity/Projects

# Path to Unity MCP installation
UNITY_MCP_PATH=/home/user/Game-OS/unity-mcp

# Unity MCP server port
UNITY_MCP_PORT=3000

# Unity Editor path (auto-detected if not set)
UNITY_EDITOR_PATH=/usr/bin/unity-editor

# --------------------------------------------
# Project Paths
# --------------------------------------------
# Root project directory
PROJECT_ROOT=/home/user/Game-OS

# Output directory for generated games
OUTPUT_DIR=/home/user/Game-OS/output

# Assets cache directory
ASSETS_CACHE_DIR=/home/user/Game-OS/.cache/assets

# --------------------------------------------
# Steam Configuration (Optional)
# --------------------------------------------
# Your Steam username
STEAM_USERNAME=your-steam-username

# Your Steam password (use Steam Guard)
STEAM_PASSWORD=your-steam-password

# Steam App ID (if you have one)
STEAM_APP_ID=

# SteamCMD path (auto-installed if not set)
STEAMCMD_PATH=/home/user/.steamcmd

# --------------------------------------------
# Development Settings
# --------------------------------------------
# Environment: dev, staging, prod
ENV=dev

# Debug mode (true/false)
DEBUG=true

# Log level: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL=INFO

# Log file path
LOG_FILE=logs/ai_game_dev.log

# Enable performance profiling
ENABLE_PROFILING=false

# --------------------------------------------
# API Rate Limiting
# --------------------------------------------
# Max API calls per minute
MAX_API_CALLS_PER_MINUTE=60

# Retry attempts for failed API calls
MAX_RETRY_ATTEMPTS=3

# Retry delay in seconds
RETRY_DELAY_SECONDS=2

# --------------------------------------------
# Agent Configuration
# --------------------------------------------
# Master agent model
MASTER_AGENT_MODEL=claude-sonnet-4-5-20250929

# Master agent max tokens
MASTER_AGENT_MAX_TOKENS=8000

# Designer agent model
DESIGNER_AGENT_MODEL=claude-sonnet-4-5-20250929

# Unity builder agent model
UNITY_BUILDER_MODEL=gemini-2.0-flash-exp

# Asset generator model
ASSET_GEN_MODEL=claude-sonnet-4-5-20250929

# --------------------------------------------
# Computer Use Configuration
# --------------------------------------------
# Enable Computer Use API
ENABLE_COMPUTER_USE=true

# Display settings for Computer Use
DISPLAY_WIDTH=1920
DISPLAY_HEIGHT=1080
DISPLAY_NUMBER=1

# --------------------------------------------
# Database (Optional - for game data caching)
# --------------------------------------------
# Database URL (SQLite by default)
DATABASE_URL=sqlite:///data/ai_game_dev.db

# --------------------------------------------
# Optional Features
# --------------------------------------------
# Enable web interface
ENABLE_WEB_UI=false
WEB_UI_PORT=5000

# Enable telemetry
ENABLE_TELEMETRY=false

# Enable automatic backups
ENABLE_AUTO_BACKUP=true
BACKUP_DIR=/home/user/Game-OS/backups

# --------------------------------------------
# Advanced Settings
# --------------------------------------------
# Concurrent asset generation jobs
MAX_CONCURRENT_JOBS=3

# Asset download timeout (seconds)
ASSET_DOWNLOAD_TIMEOUT=300

# Unity build timeout (seconds)
UNITY_BUILD_TIMEOUT=600

# Steam upload timeout (seconds)
STEAM_UPLOAD_TIMEOUT=1800
```

### Environment Setup Guide

#### 1. Copy Template
```bash
cp .env.example .env
nano .env
```

#### 2. Get API Keys

**Claude API:**
1. Visit https://console.anthropic.com
2. Create account
3. Navigate to API Keys
4. Create new key
5. Copy to `ANTHROPIC_API_KEY`

**Gemini API:**
1. Visit https://aistudio.google.com/app/apikey
2. Sign in with Google
3. Create API key
4. Copy to `GOOGLE_API_KEY`

**Asset APIs:**
- Meshy: https://www.meshy.ai → Dashboard → API Keys
- Polyhive: https://polyhive.ai → Settings → API
- Suno: https://sunoapi.org → Account → API Keys
- ElevenLabs: https://elevenlabs.io → Profile → API Keys
- Stability: https://platform.stability.ai → Account → API Keys

#### 3. Validate Environment
```bash
python scripts/validate_env.py
```

Expected output:
```
🔍 Validating Environment Configuration...

✅ ANTHROPIC_API_KEY: Valid (sk-ant-...)
✅ GOOGLE_API_KEY: Valid
✅ MESHY_API_KEY: Valid
✅ UNITY_PROJECT_PATH: Directory exists
✅ PROJECT_ROOT: Directory exists

⚠️ Optional: STEAM_USERNAME not set (Steam upload disabled)

Environment Status: READY ✅
```

---

## 🚢 Deployment Guide

### Local Development Deployment

```bash
# 1. Setup environment
./setup.sh

# 2. Configure API keys
nano .env

# 3. Validate setup
python test_setup.py

# 4. Run example
cd examples
python simple_football_manager.py

# 5. Check output
ls -la output/football_manager/
```

### Production Deployment

#### Option 1: Bare Metal Server

```bash
# 1. Clone repository
git clone https://github.com/yourusername/Game-OS.git
cd Game-OS

# 2. Run setup
./setup.sh

# 3. Configure production env
cp .env.example .env
nano .env
# Set ENV=prod
# Add production API keys

# 4. Install Unity (headless for servers)
# Follow: https://docs.unity3d.com/Manual/CommandLineArguments.html

# 5. Setup Unity MCP
cd unity-mcp
python server.py &

# 6. Run system as service
# Create systemd service: /etc/systemd/system/ai-game-dev.service
sudo systemctl enable ai-game-dev
sudo systemctl start ai-game-dev
```

#### Option 2: Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run setup
RUN chmod +x setup.sh

EXPOSE 5000

CMD ["python", "-m", "ai_game_dev.main"]
```

Deploy:
```bash
# Build image
docker build -t ai-game-dev:latest .

# Run container
docker run -d \
  --name ai-game-dev \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/output:/app/output \
  -p 5000:5000 \
  ai-game-dev:latest
```

#### Option 3: Cloud Deployment (AWS)

```bash
# Using AWS EC2 + ECS

# 1. Push Docker image to ECR
aws ecr create-repository --repository-name ai-game-dev
docker tag ai-game-dev:latest <ecr-url>/ai-game-dev:latest
docker push <ecr-url>/ai-game-dev:latest

# 2. Create ECS task definition
# See: aws/ecs-task-definition.json

# 3. Deploy to ECS
aws ecs create-service \
  --cluster ai-game-dev-cluster \
  --service-name ai-game-dev \
  --task-definition ai-game-dev-task \
  --desired-count 1
```

### Monitoring & Logging

#### Setup Logging
```bash
# Logs directory
mkdir -p logs

# Log rotation (logrotate)
sudo nano /etc/logrotate.d/ai-game-dev

# Add:
/home/user/Game-OS/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 user user
}
```

#### Monitor Logs
```bash
# Real-time logs
tail -f logs/ai_game_dev.log

# Specific agent logs
tail -f logs/master_agent.log
tail -f logs/unity_builder.log

# Error logs only
grep ERROR logs/ai_game_dev.log
```

---

## 🧪 Testing Strategy

### Test Pyramid

```
       /\
      /E2E\         <- End-to-End Tests (5%)
     /------\
    /  INT   \      <- Integration Tests (25%)
   /----------\
  /   UNIT     \    <- Unit Tests (70%)
 /--------------\
```

### Unit Tests

#### `tests/unit/test_agents.py`
```python
"""
Unit Tests for AI Agents

Test Coverage:
- Base agent functionality
- Input validation
- Error handling
- API mocking
- Response parsing

Run: pytest tests/unit/test_agents.py -v
"""

import pytest
from ai_game_dev.agents.master_agent import MasterAgent
from ai_game_dev.agents.designer_agent import DesignerAgent

class TestMasterAgent:
    def test_analyze_concept(self, mock_claude_api):
        """Test concept analysis"""
        agent = MasterAgent(api_key="test-key")
        concept = agent.analyze_concept("Football manager game")

        assert concept['type'] == 'simulation'
        assert 'systems' in concept
        assert len(concept['systems']) > 0

    def test_invalid_input(self):
        """Test input validation"""
        agent = MasterAgent(api_key="test-key")

        with pytest.raises(ValueError):
            agent.analyze_concept("")

        with pytest.raises(ValueError):
            agent.analyze_concept(None)

class TestDesignerAgent:
    def test_create_gdd(self, mock_claude_api):
        """Test GDD creation"""
        agent = DesignerAgent(api_key="test-key")
        concept = {"title": "Football Manager", "type": "simulation"}

        gdd = agent.create_gdd(concept)

        assert 'title' in gdd
        assert 'systems' in gdd
        assert 'asset_requirements' in gdd

# Run with: pytest tests/unit/ -v --cov
```

### Integration Tests

#### `tests/integration/test_workflow.py`
```python
"""
Integration Tests for Complete Workflow

Test Coverage:
- Multi-agent coordination
- API integration
- File I/O
- Unity MCP communication

Run: pytest tests/integration/test_workflow.py -v
Note: Requires API keys in .env
"""

import pytest
from ai_game_dev.main import GameDevelopmentSystem

@pytest.mark.integration
class TestCompleteWorkflow:
    def test_simple_game_creation(self, test_env):
        """Test creating a simple game"""
        system = GameDevelopmentSystem()

        result = system.create_game(
            concept="Simple clicker game",
            output_dir="tests/output/clicker"
        )

        assert result['success'] is True
        assert 'gdd' in result
        assert 'scripts' in result
        assert len(result['scripts']) >= 3

    @pytest.mark.slow
    def test_with_asset_generation(self, test_env):
        """Test with actual asset generation"""
        system = GameDevelopmentSystem()

        result = system.create_game(
            concept="Football manager",
            generate_assets=True,
            output_dir="tests/output/football"
        )

        assert result['success'] is True
        assert len(result['assets']['models']) > 0
        assert len(result['assets']['ui']) > 0

# Run with: pytest tests/integration/ -v -m integration
```

### End-to-End Tests

#### `tests/e2e/test_full_pipeline.py`
```python
"""
End-to-End Tests

Test Coverage:
- Complete game creation
- Unity project build
- Asset generation and import
- Steam upload simulation

Run: pytest tests/e2e/ -v -m e2e
Warning: These tests are slow (10-30 minutes)
"""

import pytest

@pytest.mark.e2e
@pytest.mark.slow
class TestFullPipeline:
    def test_complete_game_to_steam(self, production_env):
        """Test complete pipeline: concept → Steam"""
        from ai_game_dev.main import GameDevelopmentSystem

        system = GameDevelopmentSystem()

        # This takes 15-30 minutes
        result = system.create_game(
            concept="Football manager game",
            generate_assets=True,
            build_unity=True,
            upload_steam=False,  # Don't actually upload in tests
            output_dir="tests/output/e2e/football"
        )

        # Verify all stages completed
        assert result['stages']['design']['completed']
        assert result['stages']['assets']['completed']
        assert result['stages']['unity']['completed']
        assert result['stages']['build']['completed']

        # Verify outputs exist
        assert os.path.exists(result['unity_project_path'])
        assert os.path.exists(result['build_path'])

# Run with: pytest tests/e2e/ -v -m e2e --timeout=3600
```

### Test Commands

```bash
# All tests
pytest

# Unit tests only (fast)
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v -m integration

# E2E tests (slow - requires setup)
pytest tests/e2e/ -v -m e2e

# With coverage
pytest --cov=ai_game_dev --cov-report=html

# Specific test
pytest tests/unit/test_agents.py::TestMasterAgent::test_analyze_concept -v

# Skip slow tests
pytest -v -m "not slow"

# Parallel execution
pytest -n 4  # 4 workers
```

---

## 📚 Additional Documentation

### API Documentation
See `docs/api/` for detailed API documentation.

### Architecture Documentation
See `docs/architecture/` for system design details.

### User Guides
- Getting Started: `docs/guides/getting_started.md`
- Advanced Usage: `docs/guides/advanced_usage.md`
- Troubleshooting: `docs/guides/troubleshooting.md`

---

## 🔧 Maintenance & Updates

### Regular Maintenance Tasks

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update Unity MCP
cd unity-mcp && git pull

# Clear cache
rm -rf .cache/*

# Rotate logs
logrotate -f /etc/logrotate.d/ai-game-dev

# Backup configuration
./scripts/backup.sh
```

### Version Updates

```bash
# Update version in setup.py
# Update CHANGELOG.md
# Commit changes
git add .
git commit -m "Bump version to X.Y.Z"
git tag vX.Y.Z
git push origin main --tags
```

---

## 📞 Support & Contact

- **Issues**: https://github.com/yourusername/Game-OS/issues
- **Discussions**: https://github.com/yourusername/Game-OS/discussions
- **Email**: support@aigamedev.com
- **Discord**: (Coming soon)

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file.

---

**🎮 Ready to Build the Future of Game Development!**

*Last Updated: 2025-11-21*
*Document Version: 1.0.0*
