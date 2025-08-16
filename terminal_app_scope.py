import os
from pathlib import Path
import toml

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

from utils import show_prompt
from prompts import clarify_with_user_instructions
from scope_management.research_agent_scope import scope_research, deep_researcher_builder
from scope_management.state_scope import AgentState
from langgraph.checkpoint.memory import InMemorySaver


def save_scope_graph_png(path: str = "scope_graph.png"):
    checkpointer = InMemorySaver()
    scope = deep_researcher_builder.compile(checkpointer=checkpointer)
    graph = scope.get_graph(xray=True)
    png_bytes = graph.draw_mermaid_png()
    with open(path, "wb") as f:
        f.write(png_bytes)
    #print(f"Graph written to {path}. On macOS: run `open {path}`")
    return scope

scope = save_scope_graph_png()

from utils import format_messages
from langchain_core.messages import HumanMessage
thread = {"configurable": {"thread_id": "1"}}
user_ask=input("What do you want to know? ")
#user_ask="What is the meaning of life?"
result = scope.invoke({"messages": [HumanMessage(content=user_ask)]}, config=thread)
if result['clarification_needed']:
    print("Clarification needed")
    #print(f'DEBUG Full result messages: {result["messages"][-1].content}')
    user_ask=input(result['messages'][-1].content)
    result = scope.invoke({"messages": [HumanMessage(content=user_ask)]}, config=thread)
    format_messages(result['messages'])
else:
    print("No clarification needed")
    format_messages(result['messages'])
print(f"DEBUG Full result: {result}")


