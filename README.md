PathFinder
Offline AI-Powered Personalized Education System

PathFinder is a multilingual, multimodal educational AI system powered by Gemma 4 and deployed locally on Raspberry Pi using LiteRT-LM.

It enables students to learn through:

voice,
text,
image uploads,
adaptive quizzes,
and personalized educational support.

The system includes:

dedicated dashboards for students and teachers,
lightweight RAG-based teacher guidance retrieval,
OCR-based textbook understanding,
progress tracking,
and adaptive learning workflows.
Why PathFinder?

While the world rapidly moves toward artificial intelligence, access to quality education is still difficult for many students due to:

financial limitations,
infrastructure challenges,
transportation issues,
and lack of personalized educational support.

PathFinder was built as a low-cost offline-capable learning system that can continue functioning locally even without continuous internet connectivity after setup.

Technologies Used
Model
Gemma 4 E2B Instruct
Inference Engine
LiteRT-LM
Frameworks & Tools
Next.js
React
FastAPI
Python
Supabase
PostgreSQL
Libraries
Tesseract OCR
Pillow (PIL)
Browser Speech APIs
Hardware
Raspberry Pi 5 (4GB)
USB Microphone
Webcam
Speaker
Portable Display
Running the Project
Frontend
npm install
npm run dev
Backend
cd backend
source venv/bin/activate
python main.py

Conclusion

PathFinder is an attempt to make learning more accessible, adaptive, and connected using affordable local AI systems.

