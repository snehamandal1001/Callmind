"""
CallMind — a memory-powered call-prep agent built on Hindsight.

What it does:
  1. Every time you finish a call/meeting with a contact, you "retain" the notes.
  2. Before your NEXT call with that contact, you ask for a "prep briefing" and
     the agent RECALLS + REFLECTS on everything it remembers about them and
     hands you a sharp, personalized brief in seconds.

This is the whole point of the hackathon: memory has to be the star, not a
side feature. Every function below either writes to memory or reads from it.

Setup:
  pip install -r requirements.txt
  export GROQ_API_KEY=your-groq-key      # https://groq.com (free tier)
  python agent.py

If you'd rather use Hindsight Cloud (ui.hindsight.vectorize.io) instead of the
embedded local server, see the comment at the bottom of `get_client()`.
"""

import os
import time
from hindsight_client import Hindsight

# ---------------------------------------------------------------------------
# 1. CONNECT TO HINDSIGHT CLOUD
# ---------------------------------------------------------------------------

def get_client():
    """
    Connects to Hindsight Cloud (ui.hindsight.vectorize.io) instead of running
    a local server. This avoids the free-tier Groq rate limits we were
    hitting with the embedded/local setup, since Cloud runs on properly
    provisioned infrastructure.

    Setup (one-time):
      1. Go to https://ui.hindsight.vectorize.io and sign up
      2. Create an organization, then a memory bank (any name is fine)
      3. Apply promo code MEMHACK99 in billing for $50 free credits
      4. Click "Connect" in the top nav, then "Create API Key"
      5. Copy that key and set it as an environment variable:
           Windows (PowerShell): $env:HINDSIGHT_API_KEY="your-key-here"
           Mac/Linux:             export HINDSIGHT_API_KEY=your-key-here
    """
    api_key = os.environ.get("HINDSIGHT_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Set HINDSIGHT_API_KEY first.\n"
            "Get one at https://ui.hindsight.vectorize.io -> Connect -> Create API Key"
        )

    client = Hindsight(
        base_url="https://api.hindsight.vectorize.io",
        api_key=api_key,
    )
    return client


# ---------------------------------------------------------------------------
# 2. CORE FUNCTIONS — this is the whole "product"
# ---------------------------------------------------------------------------

def bank_for(contact_name: str) -> str:
    """Each contact gets their own memory bank so memories never mix."""
    return f"contact-{contact_name.lower().replace(' ', '-')}"

def log_meeting(client, contact_name: str, notes: str):
    """RETAIN: store what happened in this meeting."""
    bank_id = bank_for(contact_name)
    client.retain(bank_id=bank_id, content=notes)
    print(f"[retained] Logged meeting notes for {contact_name}.")

def prep_for_call(client, contact_name: str) -> str:
    """
    RECALL + REFLECT: this is the moneymaker function. It's what you'll show
    judges. Before a call, this pulls everything relevant and synthesizes it
    into a briefing a rep can read in 10 seconds.
    """
    bank_id = bank_for(contact_name)

    # Recall raw relevant memories (good to print during the demo — it's
    # "proof" the agent isn't hallucinating, it's actually retrieving).
    raw_memories = client.recall(
        bank_id=bank_id,
        query=f"Everything relevant to my next call with {contact_name}",
    )
    print("\n--- Raw memories recalled ---")
    print(raw_memories)

    # Reflect: ask Hindsight to synthesize a disposition-aware answer.
    briefing = client.reflect(
        bank_id=bank_id,
        query=(
            f"Give me a call-prep briefing on {contact_name} before my next "
            "call. Include: objections they've raised, competitors "
            "mentioned, pricing/budget concerns, decision-making dynamics, "
            "and one suggested talking point based on past conversations."
        ),
    )
    print("\n=== CALL PREP BRIEFING ===")
    print(briefing.text if hasattr(briefing, "text") else briefing)
    return briefing


# ---------------------------------------------------------------------------
# 3. SYNTHETIC DEMO DATA — realistic fake meetings across time
#    (the hackathon doc explicitly says realistic data is what sells the demo)
# ---------------------------------------------------------------------------

DEMO_CONTACT = "Priya Sharma"

DEMO_MEETINGS = [
    "Meeting 1 (Sept 2): First discovery call with Priya Sharma, VP Engineering "
    "at Finlytics. She's evaluating our platform mainly to reduce onboarding "
    "time for new engineers. Mentioned budget is tight this quarter, capped "
    "around $2,000/month. Currently also looking at CompetitorX.",

    "Meeting 2 (Sept 9): Priya raised a concern about integration time with "
    "their existing Jenkins pipeline. She said the last vendor took 3 months "
    "to integrate and it soured the team. Wants a proof of concept within 2 "
    "weeks max. Also mentioned her director, Raj, needs to sign off on "
    "anything above $1,500/month.",

    "Meeting 3 (Sept 16): Demoed the POC. Priya was impressed by the "
    "onboarding time reduction (she said 'this could save us 2 weeks per "
    "hire'). She's now leaning towards us over CompetitorX because their "
    "onboarding felt clunkier. Still worried about the $1,500 budget "
    "ceiling from Raj.",

    "Meeting 4 (Sept 23): Priya said Raj is open to $1,800/month if we can "
    "show ROI in the first 60 days. She wants a case study or reference "
    "customer in fintech specifically, since Finlytics is a fintech company "
    "and compliance matters a lot to them.",
]

def load_demo_data(client):
    """Run once to seed the demo contact with realistic history."""
    for note in DEMO_MEETINGS:
        log_meeting(client, DEMO_CONTACT, note)
    print(f"\nSeeded {len(DEMO_MEETINGS)} meetings for {DEMO_CONTACT}.")


# ---------------------------------------------------------------------------
# 4. SIMPLE CLI — this IS your demo interface. Keep it this simple for judges.
# ---------------------------------------------------------------------------

def main():
    client = get_client()

    while True:
        print("\n=== CallMind ===")
        print("1) Load demo data (seeds 4 realistic past meetings)")
        print("2) Log a new meeting note")
        print("3) Prep for a call (this is the magic — show this to judges)")
        print("4) Quit")
        choice = input("> ").strip()

        if choice == "1":
            load_demo_data(client)
        elif choice == "2":
            name = input("Contact name: ").strip()
            notes = input("Meeting notes: ").strip()
            log_meeting(client, name, notes)
        elif choice == "3":
            name = input("Contact name (try 'Priya Sharma' after loading demo data): ").strip()
            prep_for_call(client, name)
        elif choice == "4":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
