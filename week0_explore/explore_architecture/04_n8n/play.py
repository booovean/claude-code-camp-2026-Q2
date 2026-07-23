"""
n8n AI Agent - Custom Code Tool for MUD Interaction (Python)
-------------------------------------------------------------
How to use in n8n:
1. Add a "Custom Tool" node and attach it to your "AI Agent" node.
2. In the Custom Tool configuration:
   - Tool Name: play_mud
   - Description: Executes commands in the MUD game. Accepts 'commands' (semicolon separated), optional 'user', and 'password'.
   - Language: Python (Beta)
3. Under Tool Parameters (JSON Schema or Parameters depending on n8n version):
   - 'commands' (string, required): e.g., "look" or "n; n; n; e; n"
   - 'user' (string, optional): e.g., "dummy" or "smarty" (default: "dummy")
   - 'password' (string, optional): e.g., "helloworld" or "goodbyemoon" (default: "helloworld")
"""

import os
import sys
import re

# 1. Ensure mud_manager is in Python Path
# Adjust path to mud_manager/lib depending on your server/environment setup
MUD_LIB_PATH = os.getenv(
    "MUD_MANAGER_PATH",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../mud_manager/lib"))
)
if MUD_LIB_PATH not in sys.path:
    sys.path.append(MUD_LIB_PATH)

from mud_manager import Session

def execute_mud_commands(commands_str, user="dummy", password="helloworld", host="localhost", port=4000):
    """
    Connects to the MUD server, executes commands (split by semicolon),
    and returns the cleaned string output for the AI Agent.
    """
    session = Session(host=host, port=port)
    output_lines = []
    
    try:
        session.open()
        session.login(user, password)
        
        # Process each command (supporting semicolon separation)
        for cmd in commands_str.split(";"):
            cmd = cmd.strip()
            if not cmd:
                continue
            
            session.send_command(cmd)
            raw_output = session.read_until_quiet(0.5)
            # Strip ANSI color/control codes
            clean_output = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", str(raw_output)).strip()
            if clean_output:
                output_lines.append(clean_output)
                
    except Exception as e:
        return f"Error executing MUD command: {str(e)}"
    finally:
        if session.is_open():
            session.close()
            
    return "\n\n".join(output_lines)


# --- n8n Code Tool Execution Wrapper ---
# n8n provides inputs either via variables, `_input`, `query`, or `items[0].json`

def run_n8n_tool():
    # Attempt to extract parameters from n8n globals / inputs
    commands = None
    user = os.environ.get("MUD_USER", "dummy")
    password = os.environ.get("MUD_PASS", "helloworld")
    host = os.environ.get("MUD_HOST", "localhost")
    port = int(os.environ.get("MUD_PORT", "4000"))

    # Check n8n '_input' or 'query' or local variables
    if "commands" in locals() or "commands" in globals():
        commands = globals().get("commands") or locals().get("commands")
    elif "_input" in globals() and isinstance(_input, dict):
        commands = _input.get("commands") or _input.get("query")
        user = _input.get("user", user)
        password = _input.get("pass", _input.get("password", password))
    elif "query" in globals():
        commands = globals().get("query")

    # CLI Fallback for local testing outside of n8n
    if not commands and len(sys.argv) > 1:
        import argparse
        parser = argparse.ArgumentParser(description="MUD Client Script for n8n")
        parser.add_argument("commands", nargs="+", help="Commands to send to the MUD server")
        parser.add_argument("--user", default=user, help="MUD username")
        parser.add_argument("--pass", dest="password", default=password, help="MUD password")
        parser.add_argument("--host", default=host, help="MUD host")
        parser.add_argument("--port", type=int, default=port, help="MUD port")
        
        args, _ = parser.parse_known_args()
        commands = " ".join(args.commands)
        user = args.user
        password = args.password
        host = args.host
        port = args.port

    if not commands:
        return "Error: No commands provided to MUD tool."

    return execute_mud_commands(commands, user=user, password=password, host=host, port=port)


# Execute and print/return output for n8n
result = run_n8n_tool()
print(result)
