# 💼 Salary Prediction System

An intelligent **Machine Learning web application** that predicts employee salaries based on inputs like age, department, experience, and education.  
It also provides **AI-generated insights** using **Google Gemini** (or any other LLM API key configured by the user).

---

## 🚀 Live Demo
👉 [https://salary-prediction-gi9d.onrender.com/]()

---

## 🧠 Project Overview

The project allows both **manual** and **bulk (CSV)** salary predictions, supported by:

- 🤖 **AI-powered salary insights** using Gemini API  
- 🎨 **Beautiful Bootstrap UI**  
- ⏳ **Real-time “Predicting… Please wait” status**  
- ☁️ **Deployed on Render for public access**

---

## 🧩 Features

| Feature | Description |
|----------|--------------|
| 💡 **AI Insights** | Powered by Google Gemini |
| 📄 **Bulk Upload** | Upload CSV for multiple predictions |
| 🧮 **ML Model** | Trained using Scikit-learn |
| 🌐 **Responsive UI** | Built with Flask + Bootstrap |
| ☁️ **Cloud Deployment** | Hosted on Render |

---

## 🛠️ Tech Stack

| Category | Tools / Libraries |
|-----------|------------------|
| **Frontend** | HTML5, CSS3, Bootstrap 5 |
| **Backend** | Python, Flask |
| **Machine Learning** | Scikit-learn, Pandas, NumPy |
| **AI Integration** | Google Gemini API (`google-generativeai`) |
| **Deployment** | Render |
| **Version Control** | Git, GitHub |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/nithish1921/salary-prediction-system.git
cd salary-prediction-system
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate      # On Windows
# or
source venv/bin/activate   # On macOS/Linux
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Setting Up the API Key (LLM AI Insight)

The project uses **Google Gemini** for generating AI insights about predicted salaries.

### ➤ Option 1: Using `.env` file (Recommended)
Create a file named `.env` in your project folder and add:
```
GEMINI_API_KEY=your_actual_api_key_here
```

In your `app.py`, ensure you have the following:
```python
from dotenv import load_dotenv
import os, google.generativeai as genai

load_dotenv()  # Load environment variables

def llm_call(prediction, params):
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-2.5-flash")
        # ... your model logic here ...
    except Exception as e:
        print("LLM Error:", e)
```

---

### ➤ Option 2: Using a Different API (e.g., OpenAI, Claude)
If you’re using another AI provider, replace your `.env` content with:
```
OPENAI_API_KEY=your_openai_key_here
```

Then modify your configuration in `app.py`:
```python
# Replace Gemini config with your preferred API
genai.configure(api_key=os.getenv("OPENAI_API_KEY"))
model = genai.GenerativeModel("your-model-name-here")
```

⚠️ **Important:**  
Make sure you update **both**:
1. The `.env` variable name  
2. The corresponding `os.getenv()` call in your code

---

## ▶️ Running the Application

### For local testing:
```python
if __name__ == '__main__':
    app.run(debug=True)
```

### For production (Render deployment):
Uncomment the `serve()` line:
```python
if __name__ == '__main__':
    # serve(app, host='0.0.0.0', port=8080)  # For production (Render)
    app.run(debug=True)  # For local testing only
```

---

## 📚 Future Enhancements

- 🔐 Add user authentication  
- 📊 Data visualization for salary trends  
- 🧠 Support multiple AI models (Gemini / OpenAI / Claude)  
- 💾 Database storage for previous predictions  

---

## 🧑‍💻 Author

**Your Name**  
📧 your.email@example.com  
🌐 [LinkedIn](https://linkedin.com/in/yourprofile) | [GitHub](https://github.com/yourusername)

---

⭐ **If you like this project, don’t forget to give it a star on GitHub!**
