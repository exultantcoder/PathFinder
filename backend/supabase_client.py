from supabase import create_client

SUPABASE_URL = "https://vqtizamzszufnqilezju.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZxdGl6YW16c3p1Zm5xaWxlemp1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3ODc0MzUzNCwiZXhwIjoyMDk0MzE5NTM0fQ.G5SPvbYUWEMadQbnmAYrAuVBzN7uIra0zyE5Ex1kx4M"

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
