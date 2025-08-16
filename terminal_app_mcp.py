import os
from pathlib import Path
import toml
import asyncio

def load_secrets():
    """Load secrets from .streamlit/secrets.toml and set as environment variables."""
    secrets_path = Path(__file__).parent / ".streamlit" / "secrets.toml"
    
    if not secrets_path.exists():
        print(f"Warning: {secrets_path} not found. Using environment variables only.")
        return
    
    try:
        secrets = toml.load(secrets_path)
        set_keys = []
        for key, value in secrets.items():
            if isinstance(value, (str, int, float, bool)):
                os.environ[key.upper()] = str(value)
                set_keys.append(key.upper())
            elif isinstance(value, dict):
                for subkey, subvalue in value.items():
                    env_key = f"{key.upper()}_{subkey.upper()}"
                    os.environ[env_key] = str(subvalue)
                    set_keys.append(env_key)
        #if set_keys:
        #    print(f"Loaded secrets for: {', '.join(sorted(set_keys))}")
    except Exception as e:
        print(f"Error loading secrets: {e}")


load_secrets()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "ArrowStreet"

from prompts import research_agent_prompt
from research_mcp.mcp_research_agent import agent_builder_mcp
from langgraph.checkpoint.memory import InMemorySaver

def save_research_agent_graph_png(path: str = "basic_research_mcp_graph.png"):
    checkpointer = InMemorySaver()
    research_mcp = agent_builder_mcp.compile(checkpointer=checkpointer)
    graph = research_mcp.get_graph(xray=True)
    png_bytes = graph.draw_mermaid_png()
    with open(path, "wb") as f:
        f.write(png_bytes)
    #print(f"Graph written to {path}. On macOS: run `open {path}`")
    return research_mcp

research_mcp = save_research_agent_graph_png()

from langchain_core.messages import HumanMessage

async def main():
    thread = {"configurable": {"thread_id": "1"}}

    research_brief = """What are the most effective short-term stock investment strategies for a $50,000 investment, 
    considering factors such as market trends, risk tolerance, and potential returns, 
    while prioritizing reputable financial analysis sources and stock market reports?
    """

    result = await research_mcp.ainvoke({"researcher_messages": [HumanMessage(content=f"{research_brief}.")]}, 
        config=thread)
    print(f"DEBUG Full result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
