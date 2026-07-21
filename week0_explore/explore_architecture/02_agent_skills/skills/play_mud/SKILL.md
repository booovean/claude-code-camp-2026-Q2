---
name: play_mud
description: Connects to the CircleMUD/tbaMUD server at localhost:4000 and executes game commands on behalf of the player.
---

# Play MUD Skill

This skill allows the agent to interact with the CircleMUD/tbaMUD instance running locally. It encapsulates logging in and running commands via a reusable Ruby script that references the `mud_manager` library.

## Configuration & Credentials

By default, the connection uses:
- **Host:** `localhost` (override via `MUD_HOST`)
- **Port:** `4000` (override via `MUD_PORT`)
- **Username:** `dummy` (override via `MUD_USER`)
- **Password:** `hellowworld` (override via `MUD_PASS`)

## Usage

Run the helper script `play.py` inside the skill's `scripts/` directory to send commands.

### Execution Command

```bash
python week0_explore/explore_architecture/02_agent_skills/skills/play_mud/scripts/play.py "<commands>"
```

### Examples

1. Look around:
   ```bash
   python week0_explore/explore_architecture/02_agent_skills/skills/play_mud/scripts/play.py "look"
   ```

2. Perform multiple actions sequentially (semicolon-separated):
   ```bash
   python week0_explore/explore_architecture/02_agent_skills/skills/play_mud/scripts/play.py "look; exits"
   ```

## Memory & State Persistence

To drive longer-term goals (such as leveling up, finding specific areas, or defeating monsters), the agent must maintain and update two memory files located under `week0_explore/explore_architecture/02_agent_skills/data/`:

1. **Player State ([player.md](file:///c:/Repos/Exampro/bootcamp/claude-code-camp-2026-Q2/week0_explore/explore_architecture/02_agent_skills/data/player.md)):**
   - Track player stats (Level, XP, Gold, HP, Mana, Moves), equipped gear, inventory items, and current quest goals.
   - Update this file whenever you observe status/stat changes or gain/lose items.

2. **World State ([world.md](file:///c:/Repos/Exampro/bootcamp/claude-code-camp-2026-Q2/week0_explore/explore_architecture/02_agent_skills/data/world.md)):**
   - Document the map layouts, room exits, shop locations, item prices, and where specific monsters reside.
   - Update this file as you explore new rooms or discover new points of interest.

**Workflow:** Always read these memory files before executing MUD commands to retain context, and update them immediately after actions are performed to keep the state persistent.
