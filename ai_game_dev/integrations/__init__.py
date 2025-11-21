"""
Coplay Integration Package

Provides wrappers and clients for integrating with:
- Coplay Unity Plugin
- Unity MCP Server
- Multi-model AI orchestration
"""

from .coplay_orchestrator import (
    CoplayOrchestratorClient,
    CoplayConfig,
    AIModel,
    create_game_from_gdd,
    create_game_from_gdd_sync
)

__all__ = [
    'CoplayOrchestratorClient',
    'CoplayConfig',
    'AIModel',
    'create_game_from_gdd',
    'create_game_from_gdd_sync'
]
