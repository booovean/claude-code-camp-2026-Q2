import os
import sys
import re

# Add mud_manager to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../mud_manager/lib")))
from mud_manager import Session

host = os.environ.get("MUD_HOST", "localhost")
port = int(os.environ.get("MUD_PORT", "4000"))
username = os.environ.get("MUD_USER", "player")
password = os.environ.get("MUD_PASS", "hellowworld")

if len(sys.argv) < 2:
    print("Usage: python play.py <command1> [command2] ...")
    sys.exit(1)

session = Session(host=host, port=port)
try:
    session.open()
    session.login(username, password)
    
    for cmd_str in sys.argv[1:]:
        for sub_cmd in cmd_str.split(";"):
            sub_cmd = sub_cmd.strip()
            if not sub_cmd:
                continue
            
            session.send_command(sub_cmd)
            output = session.read_until_quiet(0.5)
            # Strip ANSI escape sequences
            clean_output = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", str(output)).strip()
            print(clean_output)
            
except Exception as e:
    print(f"Error: {str(e)}", file=sys.stderr)
    sys.exit(1)
finally:
    if session.is_open():
        session.close()
