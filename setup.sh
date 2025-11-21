#!/bin/bash
# GameOS AI - Setup Script

set -e

echo "🎮 GameOS AI - Setup"
echo "===================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.10+ required (found $python_version)"
    exit 1
fi
echo "✅ Python $python_version"

# Check uv
echo ""
echo "📋 Checking uv..."
if ! command -v uv &> /dev/null; then
    echo "❌ uv not found. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi
echo "✅ uv $(uv --version)"

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
uv sync
echo "✅ Dependencies installed"

# Create directories
echo ""
echo "📁 Creating directories..."
mkdir -p ~/.gameos/{cache/assets,pipelines,logs}
echo "✅ Directories created"

# Create default config
echo ""
echo "⚙️  Creating default configuration..."
config_file=~/.gameos/config.json
if [ ! -f "$config_file" ]; then
    cat > "$config_file" << EOF
{
  "server_host": "localhost",
  "server_port": 8765,
  "log_level": "INFO",
  "unity_host": "localhost",
  "unity_port_range": [5555, 5565],
  "default_model": "claude-sonnet-4.5",
  "orchestrator_enabled": true,
  "asset_generation_enabled": true,
  "pipeline_recording_enabled": true,
  "todo_enabled": true,
  "telemetry_enabled": true,
  "debug_mode": false
}
EOF
    echo "✅ Configuration created at $config_file"
else
    echo "⚠️  Configuration already exists at $config_file"
fi

# Optional: Configure API keys
echo ""
echo "🔑 API Keys Configuration (Optional)"
echo "====================================="
echo ""
echo "To use asset generation features, you'll need API keys:"
echo "  • Meshy API: https://meshy.ai"
echo "  • OpenAI: https://platform.openai.com"
echo "  • Anthropic: https://console.anthropic.com"
echo ""
read -p "Do you want to configure API keys now? (y/N): " configure_keys

if [[ $configure_keys =~ ^[Yy]$ ]]; then
    echo ""
    read -p "Meshy API Key (optional): " meshy_key
    read -p "OpenAI API Key (optional): " openai_key
    read -p "Anthropic API Key (optional): " anthropic_key

    # Update config with API keys
    python3 << EOF
import json
config_file = "$config_file"
with open(config_file, 'r') as f:
    config = json.load(f)

if "$meshy_key":
    config["meshy_api_key"] = "$meshy_key"
if "$openai_key":
    config["openai_api_key"] = "$openai_key"
if "$anthropic_key":
    config["anthropic_api_key"] = "$anthropic_key"

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)
print("✅ API keys saved to configuration")
EOF
fi

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "Next steps:"
echo "1. Start the server: uv run ai_game_dev/core/server.py"
echo "2. Install Unity plugin (see README.md)"
echo "3. Open Unity and go to Window → GameOS AI"
echo ""
echo "Documentation: https://github.com/YOUR_USERNAME/Game-OS/docs"
echo "Support: https://discord.gg/YOUR_DISCORD"
echo ""
