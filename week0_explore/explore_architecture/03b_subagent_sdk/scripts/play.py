import os
import sys
import re
import argparse

# Add mud_manager to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../mud_manager/lib")))
from mud_manager import Session

parser = argparse.ArgumentParser(description="MUD Client Script")
parser.add_argument("commands", nargs="+", help="Commands to send to the MUD server")
parser.add_argument("--user", default=os.environ.get("MUD_USER", "dummy"), help="MUD username")
parser.add_argument("--pass", dest="password", default=os.environ.get("MUD_PASS", "helloworld"), help="MUD password")
parser.add_argument("--host", default=os.environ.get("MUD_HOST", "localhost"), help="MUD host")
parser.add_argument("--port", type=int, default=int(os.environ.get("MUD_PORT", "4000")), help="MUD port")

args = parser.parse_args()

session = Session(host=args.host, port=args.port)
try:
    session.open()
    session.login(args.user, args.password)
    
    for cmd_str in args.commands:
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
