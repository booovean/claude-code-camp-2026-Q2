"""
Antigravity Agent SDK - Programmatic Subagent Definition with AgentDefinition
-------------------------------------------------------------------------------
This module demonstrates defining subagents programmatically using AgentDefinition 
instead of relying on file-system based (.agents/play-mud.md) declarations.
"""

import os
import sys
import subprocess
from dataclasses import dataclass, field
from typing import List, Callable, Dict, Any

# --- Antigravity Agent SDK: AgentDefinition ---

@dataclass
class AgentDefinition:
    """
    Programmatic definition for an Antigravity Agent / Subagent.
    Replaces file-based markdown declarations (.agents/*.md).
    """
    name: str
    description: str
    instructions: str
    tools: List[Callable] = field(default_factory=list)
    subagents: List["AgentDefinition"] = field(default_factory=list)

    def run(self, command: str) -> str:
        """
        Executes a command through the agent using its registered tools.
        """
        print(f"[{self.name}] Executing command: {command}")
        results = []
        for tool in self.tools:
            res = tool(command)
            results.append(res)
        return "\n".join(results)


# --- Tool Definitions ---

def play_mud_as_user(username: str, password: str, commands: str) -> str:
    """
    Helper tool to execute MUD commands for a specific user.
    """
    script_path = os.path.join(os.path.dirname(__file__), "scripts", "play.py")
    cmd = [
        sys.executable,
        script_path,
        "--user", username,
        "--pass", password,
        commands
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def play_as_dummy(commands: str) -> str:
    """Tool for the Warrior subagent (dummy)."""
    return play_mud_as_user("dummy", "helloworld", commands)


def play_as_smarty(commands: str) -> str:
    """Tool for the Mage subagent (smarty)."""
    return play_mud_as_user("smarty", "goodbyemoon", commands)


# --- Agent Definitions (Programmatic setup via AgentDefinition) ---

warrior_subagent = AgentDefinition(
    name="warrior_agent",
    description="Subagent responsible for controlling the Warrior character (dummy).",
    instructions=(
        "You manage the Warrior player 'dummy'. "
        "Your primary duties are combat, physical training at the Guild of Swordsmen, "
        "and exploring physical dungeons."
    ),
    tools=[play_as_dummy]
)

mage_subagent = AgentDefinition(
    name="mage_agent",
    description="Subagent responsible for controlling the Mage character (smarty).",
    instructions=(
        "You manage the Mage player 'smarty'. "
        "Your primary duties are spellcasting, studying magic at the Mages' Guild, "
        "and managing mana/resources."
    ),
    tools=[play_as_smarty]
)

main_agent = AgentDefinition(
    name="main_orchestrator",
    description="Main orchestrator agent that delegates MUD tasks to specialized subagents.",
    instructions=(
        "You coordinate actions between the Warrior subagent and the Mage subagent. "
        "Delegate warrior tasks to warrior_subagent and mage tasks to mage_subagent."
    ),
    subagents=[warrior_subagent, mage_subagent]
)


# --- Demonstration ---

if __name__ == "__main__":
    print("=== Antigravity Agent SDK: Programmatic Subagent Execution ===\n")
    
    print("1. Running Warrior Subagent (dummy):")
    out_dummy = warrior_subagent.run("look")
    print(out_dummy)
    print("-" * 50)
    
    print("\n2. Running Mage Subagent (smarty):")
    out_smarty = mage_subagent.run("look")
    print(out_smarty)
    print("-" * 50)
