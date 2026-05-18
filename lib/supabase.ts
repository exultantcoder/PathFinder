import { createClient } from "@supabase/supabase-js";

const supabaseUrl = "https://supabase.com/dashboard/project/vqtizamzszufnqilezju";
const supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZxdGl6YW16c3p1Zm5xaWxlemp1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg3NDM1MzQsImV4cCI6MjA5NDMxOTUzNH0.AiWrM6_EqAdIfH31PU3fkGTxG7-jNv32jQ9ICQC0FUM";

export const supabase = createClient(
  supabaseUrl,
  supabaseKey
);
