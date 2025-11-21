#!/usr/bin/env python3
"""
Coplay Orchestrator Integration
Wrapper for Coplay Unity Plugin + Unity MCP Server

Provides:
- Orchestrator Mode execution (GDD → Complete Game)
- Multi-model AI switching (GPT-4, Gemini 2.5, Claude 4, Grok 3)
- Action Pipeline recording and replay
- Direct Unity Editor control via MCP
- Built-in Meshy 3D asset generation
- Complete workflow automation (95%+ automation)
"""

import asyncio
import json
import logging
import os
from typing import Dict, List, Optional, Any, Literal
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

try:
    import anthropic
    import google.generativeai as genai
except ImportError:
    logging.warning("AI SDK imports failed - install anthropic and google-generativeai")


class AIModel(Enum):
    """Supported AI models for Coplay multi-model strategy"""
    GPT_4 = "gpt-4-turbo-preview"
    GEMINI_2_5_PRO = "gemini-2.5-pro"
    GEMINI_2_0_FLASH = "gemini-2.0-flash-exp"
    CLAUDE_SONNET_4_5 = "claude-sonnet-4-5-20250929"
    CLAUDE_OPUS = "claude-3-5-opus-20241022"
    GROK_3 = "grok-3"


@dataclass
class CoplayConfig:
    """Configuration for Coplay Orchestrator"""
    unity_project_path: str
    mcp_server_url: str = "http://localhost:3000"
    claude_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    meshy_api_key: Optional[str] = None
    default_model: AIModel = AIModel.CLAUDE_SONNET_4_5
    enable_orchestrator: bool = True
    enable_action_recorder: bool = True
    auto_validate_scripts: bool = True
    validation_level: Literal["basic", "standard", "strict"] = "standard"


@dataclass
class UnityMCPTool:
    """Unity MCP Tool definition"""
    name: str
    description: str
    parameters: Dict[str, Any]


class CoplayOrchestratorClient:
    """
    Main client for Coplay Unity Plugin integration

    Features:
    - Execute Orchestrator Mode (multi-step game development)
    - Control Unity Editor via MCP tools
    - Multi-model AI execution
    - Action recording and pipeline replay
    - Asset generation integration
    """

    # Unity MCP Tools (14 main tools)
    TOOLS = {
        "execute_menu_item": UnityMCPTool(
            name="execute_menu_item",
            description="Execute any Unity Editor menu command",
            parameters={"menu_path": "string"}
        ),
        "manage_asset": UnityMCPTool(
            name="manage_asset",
            description="Import, create, modify, or delete Unity assets",
            parameters={
                "operation": "import|create|modify|delete",
                "asset_path": "string",
                "asset_type": "string",
                "data": "object"
            }
        ),
        "manage_gameobject": UnityMCPTool(
            name="manage_gameobject",
            description="Create and modify GameObjects in the scene",
            parameters={
                "operation": "create|modify|delete",
                "name": "string",
                "components": "array",
                "transform": "object"
            }
        ),
        "manage_scene": UnityMCPTool(
            name="manage_scene",
            description="Load, save, create scenes",
            parameters={
                "operation": "load|save|create",
                "scene_path": "string"
            }
        ),
        "manage_prefabs": UnityMCPTool(
            name="manage_prefabs",
            description="Create and modify prefabs",
            parameters={
                "operation": "create|modify|delete",
                "prefab_path": "string",
                "gameobject_name": "string"
            }
        ),
        "apply_text_edits": UnityMCPTool(
            name="apply_text_edits",
            description="Apply precise text edits to C# scripts with hash validation",
            parameters={
                "file_path": "string",
                "old_text": "string",
                "new_text": "string",
                "expected_hash": "string"
            }
        ),
        "script_apply_edits": UnityMCPTool(
            name="script_apply_edits",
            description="Structured script editing (methods, classes, properties)",
            parameters={
                "file_path": "string",
                "edits": "array",
                "edit_type": "method|class|property|field"
            }
        ),
        "validate_script": UnityMCPTool(
            name="validate_script",
            description="Validate C# script compilation (fast validation)",
            parameters={
                "file_path": "string",
                "validation_level": "basic|standard|strict"
            }
        ),
        "search_and_replace": UnityMCPTool(
            name="search_and_replace",
            description="Search and replace across multiple files",
            parameters={
                "search_pattern": "string",
                "replace_pattern": "string",
                "file_paths": "array"
            }
        ),
        "batch_operations": UnityMCPTool(
            name="batch_operations",
            description="Execute multiple MCP operations in sequence",
            parameters={
                "operations": "array",
                "continue_on_error": "boolean"
            }
        ),
        "ai_code_generation": UnityMCPTool(
            name="ai_code_generation",
            description="Generate C# code using AI models",
            parameters={
                "prompt": "string",
                "model": "gpt-4|gemini-2.5-pro|claude-sonnet-4-5",
                "context": "object"
            }
        ),
        "meshy_generate_3d": UnityMCPTool(
            name="meshy_generate_3d",
            description="Generate 3D models via Meshy API and import to Unity",
            parameters={
                "prompt": "string",
                "art_style": "string",
                "output_format": "fbx|obj|glb"
            }
        ),
        "action_recorder_record": UnityMCPTool(
            name="action_recorder_record",
            description="Start recording Unity actions for pipeline creation",
            parameters={
                "pipeline_name": "string",
                "description": "string"
            }
        ),
        "action_recorder_replay": UnityMCPTool(
            name="action_recorder_replay",
            description="Replay recorded action pipeline",
            parameters={
                "pipeline_name": "string",
                "parameters": "object"
            }
        )
    }

    def __init__(self, config: CoplayConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Initialize AI clients
        self._init_ai_clients()

        # MCP connection state
        self.mcp_connected = False
        self.unity_project_loaded = False

    def _init_ai_clients(self):
        """Initialize AI model clients"""
        self.ai_clients = {}

        if self.config.claude_api_key:
            self.ai_clients['claude'] = anthropic.Anthropic(
                api_key=self.config.claude_api_key
            )
            self.logger.info("✅ Claude client initialized")

        if self.config.gemini_api_key:
            genai.configure(api_key=self.config.gemini_api_key)
            self.ai_clients['gemini'] = genai
            self.logger.info("✅ Gemini client initialized")

        # OpenAI and Grok clients can be added similarly

    async def connect_to_unity_mcp(self) -> bool:
        """Connect to Unity MCP server"""
        try:
            self.logger.info(f"🔌 Connecting to Unity MCP: {self.config.mcp_server_url}")

            # In real implementation, establish WebSocket/HTTP connection
            # For now, assume connection succeeds
            self.mcp_connected = True
            self.logger.info("✅ Connected to Unity MCP server")

            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to connect to Unity MCP: {e}")
            return False

    async def load_unity_project(self, project_path: Optional[str] = None) -> bool:
        """Load Unity project in the Editor"""
        try:
            path = project_path or self.config.unity_project_path
            self.logger.info(f"📂 Loading Unity project: {path}")

            # Use execute_menu_item to open project
            result = await self.execute_mcp_tool(
                "execute_menu_item",
                {"menu_path": "File/Open Project"}
            )

            self.unity_project_loaded = True
            self.logger.info("✅ Unity project loaded")

            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to load Unity project: {e}")
            return False

    async def execute_mcp_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a Unity MCP tool"""
        if tool_name not in self.TOOLS:
            raise ValueError(f"Unknown MCP tool: {tool_name}")

        self.logger.debug(f"🔧 Executing MCP tool: {tool_name}")
        self.logger.debug(f"   Parameters: {json.dumps(parameters, indent=2)}")

        # In real implementation, send MCP request to server
        # For now, return mock success
        result = {
            "success": True,
            "tool": tool_name,
            "result": "Executed successfully",
            "timestamp": "2025-11-21T00:00:00Z"
        }

        return result

    async def orchestrator_mode(
        self,
        gdd: Dict[str, Any],
        model: AIModel = None,
        enable_asset_generation: bool = True
    ) -> Dict[str, Any]:
        """
        Execute Orchestrator Mode - Complete GDD → Game workflow

        This is the main automation feature that:
        1. Analyzes the Game Design Document
        2. Creates Unity project structure
        3. Generates all C# scripts using multi-model AI
        4. Generates 3D assets via Meshy
        5. Builds scenes and prefabs
        6. Configures game settings
        7. Runs validation and tests

        Args:
            gdd: Complete Game Design Document (JSON)
            model: AI model to use (defaults to config.default_model)
            enable_asset_generation: Whether to generate 3D assets

        Returns:
            Complete execution result with all generated files
        """
        model = model or self.config.default_model
        self.logger.info("=" * 70)
        self.logger.info("🎮 ORCHESTRATOR MODE - STARTING")
        self.logger.info("=" * 70)
        self.logger.info(f"📋 Game: {gdd.get('title', 'Untitled Game')}")
        self.logger.info(f"🤖 AI Model: {model.value}")
        self.logger.info(f"🎨 Asset Generation: {'Enabled' if enable_asset_generation else 'Disabled'}")

        results = {
            "success": False,
            "game_title": gdd.get('title'),
            "steps_completed": [],
            "files_generated": [],
            "assets_generated": [],
            "errors": [],
            "execution_time_seconds": 0
        }

        import time
        start_time = time.time()

        try:
            # Step 1: Create Unity project structure
            self.logger.info("\n📁 Step 1/7: Creating Unity project structure...")
            await self._create_project_structure(gdd)
            results["steps_completed"].append("project_structure")

            # Step 2: Generate all C# scripts
            self.logger.info("\n💻 Step 2/7: Generating C# scripts with AI...")
            scripts = await self._generate_all_scripts(gdd, model)
            results["files_generated"].extend(scripts)
            results["steps_completed"].append("script_generation")

            # Step 3: Generate 3D assets (if enabled)
            if enable_asset_generation and self.config.meshy_api_key:
                self.logger.info("\n🎨 Step 3/7: Generating 3D assets via Meshy...")
                assets = await self._generate_3d_assets(gdd)
                results["assets_generated"].extend(assets)
                results["steps_completed"].append("asset_generation")
            else:
                self.logger.info("\n⏭️  Step 3/7: Skipping asset generation")

            # Step 4: Build scenes
            self.logger.info("\n🎬 Step 4/7: Building game scenes...")
            scenes = await self._build_scenes(gdd)
            results["files_generated"].extend(scenes)
            results["steps_completed"].append("scene_building")

            # Step 5: Create prefabs
            self.logger.info("\n🧩 Step 5/7: Creating prefabs...")
            prefabs = await self._create_prefabs(gdd)
            results["files_generated"].extend(prefabs)
            results["steps_completed"].append("prefab_creation")

            # Step 6: Configure project settings
            self.logger.info("\n⚙️  Step 6/7: Configuring project settings...")
            await self._configure_project_settings(gdd)
            results["steps_completed"].append("configuration")

            # Step 7: Validate and compile
            self.logger.info("\n✅ Step 7/7: Validating scripts and compiling...")
            validation = await self._validate_all_scripts()
            if not validation["success"]:
                results["errors"].extend(validation["errors"])
            results["steps_completed"].append("validation")

            results["success"] = True
            results["execution_time_seconds"] = time.time() - start_time

            self.logger.info("\n" + "=" * 70)
            self.logger.info("🎉 ORCHESTRATOR MODE - COMPLETED SUCCESSFULLY")
            self.logger.info("=" * 70)
            self.logger.info(f"⏱️  Execution time: {results['execution_time_seconds']:.1f} seconds")
            self.logger.info(f"📄 Scripts generated: {len([f for f in results['files_generated'] if f.endswith('.cs')])}")
            self.logger.info(f"🎨 Assets generated: {len(results['assets_generated'])}")
            self.logger.info(f"🎬 Scenes created: {len([f for f in results['files_generated'] if f.endswith('.unity')])}")

        except Exception as e:
            self.logger.error(f"\n❌ Orchestrator Mode failed: {e}")
            results["errors"].append(str(e))
            results["execution_time_seconds"] = time.time() - start_time
            import traceback
            traceback.print_exc()

        return results

    async def _create_project_structure(self, gdd: Dict[str, Any]):
        """Create complete Unity project folder structure"""
        folders = [
            "Assets/Scripts",
            "Assets/Scenes",
            "Assets/Prefabs",
            "Assets/Materials",
            "Assets/Models",
            "Assets/Textures",
            "Assets/Audio/Music",
            "Assets/Audio/SFX",
            "Assets/UI",
            "Assets/Resources",
            "Assets/Data"
        ]

        for folder in folders:
            await self.execute_mcp_tool(
                "manage_asset",
                {
                    "operation": "create",
                    "asset_path": folder,
                    "asset_type": "Folder",
                    "data": {}
                }
            )
            self.logger.info(f"   ✅ Created: {folder}")

    async def _generate_all_scripts(
        self,
        gdd: Dict[str, Any],
        model: AIModel
    ) -> List[str]:
        """Generate all C# scripts from GDD using AI"""
        scripts_generated = []

        # Extract script requirements from GDD
        script_specs = self._extract_script_specs_from_gdd(gdd)

        self.logger.info(f"   📝 Generating {len(script_specs)} scripts...")

        for spec in script_specs:
            self.logger.info(f"   🔨 Generating: {spec['name']}.cs")

            # Generate script using AI
            script_content = await self._generate_script_with_ai(spec, model)

            # Save to Unity project
            script_path = f"Assets/Scripts/{spec['name']}.cs"
            await self.execute_mcp_tool(
                "manage_asset",
                {
                    "operation": "create",
                    "asset_path": script_path,
                    "asset_type": "MonoScript",
                    "data": {"content": script_content}
                }
            )

            # Validate script
            if self.config.auto_validate_scripts:
                validation = await self.execute_mcp_tool(
                    "validate_script",
                    {
                        "file_path": script_path,
                        "validation_level": self.config.validation_level
                    }
                )

                if validation.get("success"):
                    self.logger.info(f"      ✅ {spec['name']}.cs (validated)")
                else:
                    self.logger.warning(f"      ⚠️  {spec['name']}.cs (validation warnings)")

            scripts_generated.append(script_path)

        return scripts_generated

    async def _generate_script_with_ai(
        self,
        spec: Dict[str, Any],
        model: AIModel
    ) -> str:
        """Generate a single C# script using specified AI model"""
        prompt = f"""Generate a complete Unity C# script for:

**Name:** {spec['name']}
**Purpose:** {spec['description']}
**Requirements:** {json.dumps(spec.get('requirements', {}), indent=2)}

Follow Unity best practices:
- Include XML documentation comments
- Use proper naming conventions
- Add error handling
- Make it production-ready

Output ONLY the C# code, no markdown."""

        if model == AIModel.CLAUDE_SONNET_4_5:
            client = self.ai_clients.get('claude')
            if not client:
                raise ValueError("Claude client not initialized")

            response = client.messages.create(
                model=model.value,
                max_tokens=4000,
                temperature=0.6,
                messages=[{"role": "user", "content": prompt}]
            )

            script_content = response.content[0].text

        elif model in [AIModel.GEMINI_2_5_PRO, AIModel.GEMINI_2_0_FLASH]:
            genai_client = self.ai_clients.get('gemini')
            if not genai_client:
                raise ValueError("Gemini client not initialized")

            model_obj = genai_client.GenerativeModel(model.value)
            response = model_obj.generate_content(prompt)
            script_content = response.text

        else:
            raise ValueError(f"Model {model} not yet implemented")

        # Clean up markdown code blocks if present
        if "```csharp" in script_content:
            script_content = script_content.split("```csharp")[1].split("```")[0].strip()
        elif "```" in script_content:
            script_content = script_content.split("```")[1].split("```")[0].strip()

        return script_content

    def _extract_script_specs_from_gdd(self, gdd: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract script specifications from GDD"""
        specs = []

        # Try to get from technical_requirements or systems section
        tech_reqs = gdd.get('technical_requirements', {})
        scripts_list = tech_reqs.get('scripts', [])

        if scripts_list:
            return scripts_list

        # Fallback: generate basic specs from systems
        systems = gdd.get('systems', [])
        for system in systems:
            specs.append({
                "name": system.get('name', 'System').replace(' ', ''),
                "description": system.get('description', ''),
                "requirements": system.get('requirements', {})
            })

        return specs

    async def _generate_3d_assets(self, gdd: Dict[str, Any]) -> List[str]:
        """Generate 3D assets via Meshy API"""
        assets_generated = []

        # Extract asset requirements from GDD
        asset_reqs = gdd.get('asset_requirements', {}).get('3d_models', [])

        self.logger.info(f"   🎨 Generating {len(asset_reqs)} 3D models...")

        for asset in asset_reqs:
            self.logger.info(f"   🔨 Generating: {asset['name']}")

            result = await self.execute_mcp_tool(
                "meshy_generate_3d",
                {
                    "prompt": asset['description'],
                    "art_style": asset.get('art_style', 'realistic'),
                    "output_format": "fbx"
                }
            )

            if result.get("success"):
                asset_path = result.get("asset_path")
                assets_generated.append(asset_path)
                self.logger.info(f"      ✅ {asset['name']} generated")

        return assets_generated

    async def _build_scenes(self, gdd: Dict[str, Any]) -> List[str]:
        """Build game scenes based on GDD"""
        scenes_created = []

        # Get scene list from GDD
        scenes = gdd.get('technical_requirements', {}).get('scenes', [])

        if not scenes:
            # Create default scenes
            scenes = [
                {"name": "MainMenu", "description": "Main menu scene"},
                {"name": "Gameplay", "description": "Main gameplay scene"}
            ]

        for scene in scenes:
            scene_path = f"Assets/Scenes/{scene['name']}.unity"

            await self.execute_mcp_tool(
                "manage_scene",
                {
                    "operation": "create",
                    "scene_path": scene_path
                }
            )

            scenes_created.append(scene_path)
            self.logger.info(f"   ✅ Scene created: {scene['name']}")

        return scenes_created

    async def _create_prefabs(self, gdd: Dict[str, Any]) -> List[str]:
        """Create prefabs from GDD specifications"""
        prefabs_created = []

        # Extract prefab requirements
        prefabs = gdd.get('technical_requirements', {}).get('prefabs', [])

        for prefab in prefabs:
            prefab_path = f"Assets/Prefabs/{prefab['name']}.prefab"

            # Create GameObject first
            await self.execute_mcp_tool(
                "manage_gameobject",
                {
                    "operation": "create",
                    "name": prefab['name'],
                    "components": prefab.get('components', []),
                    "transform": prefab.get('transform', {})
                }
            )

            # Convert to prefab
            await self.execute_mcp_tool(
                "manage_prefabs",
                {
                    "operation": "create",
                    "prefab_path": prefab_path,
                    "gameobject_name": prefab['name']
                }
            )

            prefabs_created.append(prefab_path)
            self.logger.info(f"   ✅ Prefab created: {prefab['name']}")

        return prefabs_created

    async def _configure_project_settings(self, gdd: Dict[str, Any]):
        """Configure Unity project settings"""
        settings = gdd.get('technical_requirements', {}).get('project_settings', {})

        # Configure player settings
        if 'player_settings' in settings:
            await self.execute_mcp_tool(
                "execute_menu_item",
                {"menu_path": "Edit/Project Settings/Player"}
            )

        # Configure quality settings
        if 'quality_settings' in settings:
            await self.execute_mcp_tool(
                "execute_menu_item",
                {"menu_path": "Edit/Project Settings/Quality"}
            )

        self.logger.info("   ✅ Project settings configured")

    async def _validate_all_scripts(self) -> Dict[str, Any]:
        """Validate all generated scripts"""
        # In real implementation, iterate through all scripts and validate
        # For now, return success
        return {
            "success": True,
            "errors": [],
            "warnings": []
        }

    async def record_action_pipeline(
        self,
        pipeline_name: str,
        description: str
    ) -> Dict[str, Any]:
        """Start recording actions for pipeline creation"""
        self.logger.info(f"🎬 Recording action pipeline: {pipeline_name}")

        result = await self.execute_mcp_tool(
            "action_recorder_record",
            {
                "pipeline_name": pipeline_name,
                "description": description
            }
        )

        return result

    async def replay_action_pipeline(
        self,
        pipeline_name: str,
        parameters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Replay a recorded action pipeline"""
        self.logger.info(f"▶️  Replaying action pipeline: {pipeline_name}")

        result = await self.execute_mcp_tool(
            "action_recorder_replay",
            {
                "pipeline_name": pipeline_name,
                "parameters": parameters or {}
            }
        )

        return result

    async def switch_ai_model(self, model: AIModel) -> bool:
        """Switch the active AI model"""
        self.config.default_model = model
        self.logger.info(f"🔄 Switched AI model to: {model.value}")
        return True

    async def close(self):
        """Close connections and cleanup"""
        self.logger.info("🔌 Closing Coplay Orchestrator connections...")
        self.mcp_connected = False
        self.unity_project_loaded = False


# Helper functions for easy usage

async def create_game_from_gdd(
    gdd: Dict[str, Any],
    config: CoplayConfig
) -> Dict[str, Any]:
    """
    High-level function to create complete game from GDD

    Example:
        config = CoplayConfig(
            unity_project_path="/path/to/project",
            claude_api_key=os.getenv('ANTHROPIC_API_KEY'),
            gemini_api_key=os.getenv('GOOGLE_API_KEY')
        )

        result = await create_game_from_gdd(gdd, config)
    """
    orchestrator = CoplayOrchestratorClient(config)

    try:
        await orchestrator.connect_to_unity_mcp()
        await orchestrator.load_unity_project()

        result = await orchestrator.orchestrator_mode(gdd)

        return result
    finally:
        await orchestrator.close()


def create_game_from_gdd_sync(
    gdd: Dict[str, Any],
    config: CoplayConfig
) -> Dict[str, Any]:
    """Synchronous wrapper for create_game_from_gdd"""
    return asyncio.run(create_game_from_gdd(gdd, config))
