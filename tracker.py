import json
from dotenv import load_dotenv
import os
import anthropic

load_dotenv()
# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

COURSES = [
    "Agent Skills",
    "Claude API",
    "MCP",
    "Claude Code"
]

MEMBERS = [
    "Abhilash",
    "Abhishek",
    "Chaitanya",
    "Charles",
    "Daiva",
    "Deepika",
    "Eram",
    "Japanya",
    "Joel",
    "Keerthi",
    "Kishore",
    "Madhu",
    "Praful",
    "Pramod",
    "Sathya",
    "Shruti",
    "Sunil",
    "Uday",
    "Varun"
]

DATA_FILE = "data.json"

# --------------------------------------------------
# CLAUDE CLIENT
# --------------------------------------------------

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_data():

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    data = {
        member: {
            course: False for course in COURSES
        }
        for member in MEMBERS
    }

    save_data(data)
    return data


# --------------------------------------------------
# SAVE DATA
# --------------------------------------------------

def save_data(data):

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# --------------------------------------------------
# AI INSIGHTS
# --------------------------------------------------

def get_insights(data):

    prompt = f"""
You are a Learning & Development manager.

IMPORTANT RULES:
- Do NOT mention any employee names
- Do NOT refer to individuals
- Only provide group-level analysis

Analyze this training data:
{json.dumps(data, indent=2)}

Return ONLY the following:
1. Overall team summary
2. Team completion percentage (estimate if needed)
3. Most incomplete course

Keep it concise, factual, and professional.
"""

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text
