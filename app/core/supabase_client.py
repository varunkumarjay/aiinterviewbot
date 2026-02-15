import os
from supabase import create_client
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load root .env
env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print("Loaded SUPABASE_URL:", SUPABASE_URL)

if not SUPABASE_URL:
    raise Exception("SUPABASE_URL not found in environment variables")

if not SUPABASE_KEY:
    raise Exception("SUPABASE_SERVICE_ROLE_KEY not found in environment variables")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
