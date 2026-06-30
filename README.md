# PathFinder  
### Offline AI-Powered Personalized Education System

Live Demo: https://path-finder-5mgvxy61c-exultantcoders-projects.vercel.app/
PathFinder is a multilingual, multimodal educational AI system powered by Gemma 4 and deployed locally on Raspberry Pi using LiteRT-LM.

It enables students to learn through:
- Voice interaction
- Text-based tutoring
- Image uploads
- Adaptive quizzes
- Personalized educational support

The system includes:
- Dedicated dashboards for students and teachers
- Lightweight RAG-based teacher guidance retrieval
- OCR-based textbook understanding
- Progress tracking
- Adaptive learning workflows

  
<img width="1536" height="1024" alt="ChatGPT Image Jun 30, 2026, 11_01_47 AM" src="https://github.com/user-attachments/assets/88f06186-7a75-487e-9b90-cc0fb8b238f3" />


## Why PathFinder?

While the world rapidly moves toward artificial intelligence, access to quality education is still difficult for many students due to:
- Financial limitations
- Infrastructure challenges
- Transportation issues
- Lack of personalized educational support

PathFinder was built as a low-cost offline-capable learning system that can continue functioning locally even without continuous internet connectivity after setup.

---

## Technologies Used

### Model
- Gemma 4 E2B Instruct

### Inference Engine
- LiteRT-LM

### Frameworks & Tools
- Next.js
- React
- FastAPI
- Python
- Supabase
- PostgreSQL

### Libraries
- Tesseract OCR
- Pillow (PIL)
- Browser Speech APIs

### Hardware
- Raspberry Pi 5 (4GB)
- USB Microphone
- Webcam
- Speaker
- Portable Display

---

## How PathFinder Works

- Students interact using voice, text, and image uploads
- OCR extracts text from textbook images and handwritten notes
- Gemma 4 processes requests locally using LiteRT-LM
- Adaptive responses generated using learning history and weak topics
- Personalized quizzes and recommendations generated automatically
- Teachers monitor student progress through dedicated dashboards
- Teacher notes retrieved using lightweight RAG workflows

---

## Running the Project

```bash
npm install
npm run dev
cd backend
source venv/bin/activate
python main.py
```
### Conclusion

PathFinder is an attempt to make learning more accessible, adaptive, and connected using affordable local AI systems.
Sometimes meaningful technology begins with a small device, a local AI model, and the intention to help students find their path toward knowlege.
