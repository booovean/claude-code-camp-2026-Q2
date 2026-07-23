# Preweek Techinical Documentation

## Technical Goal
The technical goal of Peweek Explore is to determine how well do agent architectures fit our use case. 

Example of agent architecture that scale with effort:
- an agent file with reference files (such as agent.md, player.md, world.md)
- Agent skills driven by main agent, each skill manage its own data
- Filesystem subagent driven by a coding harness
- AI workflow automation platform, such as n8n
- Use a generic AI agent SDK that leverages plug and play generic AI packages
- Use a low level first-party LLM SDK and write our own agentic loop
- Use REST API directly, write our own agentic loop
    - the agentic loop is model-driven orchestration with middleware programmatic guidance
    - The agentic loop is code-drive orchestration

## Technical Uncertainty

I did not know where to start, being new to this whole agent programming thing. 

Following through the bootcamp videos, I was fairly successful at following along and getting the MUD working, playing the game and exploring the world. 

My biggest uncertainty was around what if a coding harness agentic loop is effective enough to drive a non coding workload for our use case.

## Technical Hypothesis

- As I have no experience yet with this type of task, but have too much belief in AI (more than I should), I am hoping for a successful result of our week0 objectives.

- I will be using Antigravity IDE to take advantage of my current subscription and compare it with Claude's results from the videos from week0 Explore.

## Technical Obsevations

Using Gemini Flash 3.5 (later on 3.6 as it was released this week) through Google Antigravity IDE, I've had great success to complete the multiple tasks required through the Preweek Explore and going through the MUD as well.

More specifically:

- An agent.md file connected successfully to the MUD
- Skills and subagents performed well with a script to manage the nc sessions. They were able to play the MUD as instructed.
- Using markdown files where the coding harness updates it as simple memory was surprisingly efficient.

## Technical Conclusions

- Skills and subagents are capable of driving the MUD. 
- We do need specialized memory for map navigation and world data.
- We opened a new technical use case of if we should have our agent handle multiple sessions of multiple players playing simultaneously (as COOP is a comon factor in MUD games)
- We could not exploire n8n completely, although Antigravity  seems to have generated the necessary coding snippets.
- Implementing our own specialized loops remain technically uncertain and will need to be explored in depth during week 2.
- As mentioned earlier, Antigravity IDE + Gemini Flash 3.5 functioned rather well and am rather disappointed by all the pain points the instructor experienced while using Claude Code with the Sonnet 4.6 model. This may be quite different with the new Sonnet 5 model though.

## Key Takeaway

When we have a specialized use case, such as playing a MUD, we cannot leverage generic SDKs for agents, because we need specialized tooling and agentic loops.

From my experience in Preweek Explore, it was going rather well, but tokens were running low.