import os
import sys
from dotenv import load_dotenv


load_dotenv()

print("🔧 Loading logging level...")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

print("🔧 Slack credentials loading...")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

print("🔧 Large Language Model provider configurations loading...")
LLM_PROVIDER = (
    os.getenv("LLM_PROVIDER", "").lower() if os.getenv("LLM_PROVIDER") else None
)
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

print("🔧 Database configurations loading...")
DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()

print("🔧 Checking required configurations...")
if not SLACK_APP_TOKEN or not SLACK_BOT_TOKEN or not LLM_PROVIDER:
    missing_vars = []

    if not SLACK_APP_TOKEN:
        missing_vars.append("SLACK_APP_TOKEN")
    if not SLACK_BOT_TOKEN:
        missing_vars.append("SLACK_BOT_TOKEN")
    if not LLM_PROVIDER:
        missing_vars.append("LLM_PROVIDER")

    print(f"Error: Required configuration are missing: {', '.join(missing_vars)}")
    print("Please set these configuration in your `.env` file.")
    sys.exit(1)

print("✅ Successfully loaded!")

summary_lines = []
summary_lines.append("=" * 50)
summary_lines.append("🔧 Configuration Summary".center(50))
summary_lines.append("=" * 50)
summary_lines.append(f"{'LOG_LEVEL'.ljust(20)}: {LOG_LEVEL}")
summary_lines.append("-" * 50)

if SLACK_APP_TOKEN:
    summary_lines.append(f"{'SLACK_APP_TOKEN'.ljust(20)}: <masked>")
if SLACK_BOT_TOKEN:
    summary_lines.append(f"{'SLACK_BOT_TOKEN'.ljust(20)}: <masked>")
summary_lines.append("-" * 50)
if LLM_PROVIDER:
    summary_lines.append(f"{'LLM_PROVIDER'.ljust(20)}: {LLM_PROVIDER}")

    if LLM_PROVIDER == "ollama" and OLLAMA_MODEL:
        summary_lines.append(f"{'MODEL'.ljust(20)}: {OLLAMA_MODEL}")
    elif LLM_PROVIDER == "openai":
        if OPENAI_MODEL:
            summary_lines.append(f"{'OPENAI_MODEL'.ljust(20)}: {OPENAI_MODEL}")
summary_lines.append("-" * 50)
if DB_TYPE:
    summary_lines.append(f"{'DATABASE'.ljust(20)}: {DB_TYPE}")

summary_lines.append("=" * 50)

print("\n" + "\n".join(summary_lines) + "\n")
