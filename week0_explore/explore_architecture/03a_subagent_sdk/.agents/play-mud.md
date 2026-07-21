---
name: play_mud
description: Connects to the CircleMUD/tbaMUD server at localhost:4000 and executes game commands on behalf of a player.
---

# Play MUD Agent

This agent allows interaction with the CircleMUD/tbaMUD instance running locally. It encapsulates logging in and running commands via a间 Python script that references the `mud_manager` library.

## Players Configuration

- **Main player:** `dummy` / `helloworld`
- **Secondary player:** `smarty` / `goodbyemoon`

## Configuration & Credentials

By default, the connection uses:
- **Host:** `localhost` (override via `MUD_HOST` or `--host`)
- **Port:** `4000` (override via `MUD_PORT` or `--port`)
- **Username:** `dummy` (override via `MUD_USER` or `--user`)
- **Password:** `helloworld` (override via `MUD_PASS` or `--pass`)

## Usage

Run the helper script `play.py` inside the `scripts/` directory to send commands.

### Execution Command

```bash
# Default (dummy)
python week0_explore/explore_architecture/03_subagent_sdk/scripts/play.py "<commands>"

# Specifying a user/agent (e.g. smarty)
python week0_explore/explore_architecture/03_subagent_sdk/scripts/play.py --user smarty --pass goodbyemoon "<commands>"
```

### Examples

1. Look around:
   ```bash
   python week0_explore/explore_architecture/03_subagent_sdk/scripts/play.py "look"
   ```

2. Perform multiple actions sequentially as `smarty`:
   ```bash
   python week0_explore/explore_architecture/03_subagent_sdk/scripts/play.py --user smarty --pass goodbyemoon "look; score"
   ```

## Memory & State Persistence

To drive longer-term goals (such as leveling up, finding specific areas, or defeating monsters), each agent should maintain and update its memory files located under `week0_explore/explore_architecture/03_subagent_sdk/data/`:

1. **Player State ([player.md](file:///c:/Repos/Exampro/bootcamp/claude-code-camp-2026-Q2/week0_explore/explore_architecture/03_subagent_sdk/data/player.md)):**
   - Track player stats (Level, XP, Gold, HP, Mana, Moves), equipped gear, inventory items, and current quest goals.
   - Update this file whenever you observe status/stat changes or gain/lose items.

2. **World State ([world.md](file:///c:/Repos/Exampro/bootcamp/claude-code-camp-2026-Q2/week0_explore/explore_architecture/03_subagent_sdk/data/world.md)):**
   - Document the map layouts, room exits, shop locations, item prices, and where specific monsters reside.
   - Update this file as you explore new rooms or discover new points of interest.

**Workflow:** Always read these memory files before executing MUD commands to retain context, and update them immediately after actions are performed to keep the state persistent.
