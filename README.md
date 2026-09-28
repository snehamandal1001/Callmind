# CallMind — Memory-Powered Call Prep Agent

Built for HackWithHyderabad 3.0, using [Hindsight](https://github.com/vectorize-io/hindsight) as the memory layer.

## The problem
Sales/CS reps re-read old notes before every call with the same contact. It's slow, and important details (objections, budget limits, competitor mentions) get lost between meetings.

## The idea
CallMind remembers every meeting with a contact and gives the rep a synthesized prep briefing before the next call — objections raised, competitors mentioned, budget constraints, and a suggested talking point. Memory quality directly determines the quality of the briefing, so it's the actual product, not a feature bolted on.

## Setup

pip install -r requirements.txt

Get a Hindsight Cloud API key at https://ui.hindsight.vectorize.io (Connect, then Create API Key), then:

Windows (PowerShell):
$env:HINDSIGHT_API_KEY="your-key-here"

Mac/Linux:
export HINDSIGHT_API_KEY=your-key-here

python agent.py

(To use Hindsight Cloud instead of the embedded server — including the `MEMHACK99` promo credits — see the commented-out block in `get_client()` in `agent.py`.)

## How to demo this to judges (60-second story)

1. Run `agent.py`, choose option **3**, type "Priya Sharma" *before* loading any data.
   → Agent has nothing to say. This is your "before memory" baseline.
2. Choose option **1** to seed 4 realistic past meetings (already written in `agent.py`, feel free to edit them to your own scenario).
3. Choose option **3** again for "Priya Sharma".
   → Now the agent gives a full briefing: her budget ceiling, her boss Raj's sign-off threshold, the competitor she's weighing you against, and what she needs to see next (a fintech case study).
4. Say out loud: *"Notice it didn't just repeat facts — it synthesized four separate conversations into one actionable brief in under a second."*

That before/after is exactly what the judging doc says to show.

## Where to take it further (if you have time)
- Swap the CLI for a tiny Streamlit page (one dropdown for contact, one button "Prep Me").
- Add a second contact so judges see it's not hardcoded to one person.
- Log a *new* meeting live during the demo, then immediately ask for a fresh prep to show it updates instantly.
- Add a short paragraph in your submission on how the multi-strategy recall (semantic + graph + temporal) helped surface things a plain vector search would've missed.

## Files
- `agent.py` — the whole agent (retain / recall / reflect + CLI)
- `requirements.txt` — one dependency, `hindsight-all` (embedded, no Docker needed)
