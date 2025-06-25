"""ElevenLabs Agent implementation using ADK and MCPToolset."""

import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from mcp.client.stdio import StdioServerParameters

from elevenlabs_agent.prompt import ELEVENLABS_PROMPT


def create_elevenlabs_agent() -> Agent:
    """Creates the ElevenLabs agent with proper timeout handling."""
    # This is the best practice for deployment.
    # Get the API key from the environment variables set on the server.
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    tool_env = {}
    if elevenlabs_key:
        tool_env["ELEVENLABS_API_KEY"] = elevenlabs_key
    else:
        # This provides a clear warning if the key is missing during startup.
        print("Warning: ELEVENLABS_API_KEY environment variable not set. Tool may fail.")

    return Agent(
        name="elevenlabs_agent_mcp",
        model=LiteLlm(
            model="anthropic/claude-3-5-sonnet-20241022",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        ),
        description="Specialized agent for converting text to speech using ElevenLabs via MCPToolset.",
        instruction=ELEVENLABS_PROMPT,
        tools=[
            MCPToolset(
                connection_params=StdioConnectionParams(
                    server_params=StdioServerParameters(
                        command="uvx",
                        args=["elevenlabs-mcp"],
                        env=tool_env,
                    ),
                    timeout=30,
                )
            )
        ],
    )


root_agent = create_elevenlabs_agent()