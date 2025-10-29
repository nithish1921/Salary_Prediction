# 💼 Salary Prediction System

An intelligent **Machine Learning web application** that predicts employee salaries based on inputs like age, department, experience, and education.  
It also provides **AI-generated insights** using **Google Gemini** (or any other LLM API key configured by the user).

---

## 🚀 Live Demo
👉 **[View on Render](https://salary-prediction-gi9d.onrender.com/)**

---

## 🧠 Project Overview
The project allows both **manual** and **bulk (CSV)** salary predictions, supported by:
- 💡 AI-powered salary insights using API  
- 📄 Bulk Upload option for CSV files  
- 🧮 Trained ML Model using Scikit-learn  
- 🌐 Interactive Bootstrap-based web interface  
- ☁️ Fully deployed on Render  

---

## 🧩 Features
- 💬 **AI Insight Generation** using Gemini  
- 🧠 **ML Model** trained for salary prediction  
- 📂 **Bulk CSV Upload** for multi-record predictions  
- ⚙️ **Flask Web Framework** for backend  
- 💻 **Bootstrap 5 UI** for responsive design  
- 🌍 **Render Deployment** for global access  

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
git clone https://github.com/yourusername/salary-prediction-system.git
cd salary-prediction-system

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate      # On Windows
# or
source venv/bin/activate   # On macOS/Linux

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt

## 🔑 Setting Up the API Key (LLM AI Insight)
The project uses Google Gemini API for generating AI insights about predicted salaries.

### ➤ Option 1: Using .env file (Recommended)
- Create a file named .env in your project root directory.
- Add your Gemini API key inside .env as follows:
```ini
GEMINI_API_KEY=your_actual_api_key_here
- Ensure your app.py contains this code:
```python
from dotenv import load_dotenv
import os, google.generativeai as genai

load_dotenv()  # Load environment variables

def llm_call(prediction, params):
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-2.5-flash")
        # your logic for AI insight generation here
    except Exception as e:
        print("LLM Error:", e)

### ➤ Option 1: Using .env file (Recommended)
If you are using a different AI provider, follow these steps:
- Replace your .env content completely with your custom key, for example:
```ini
OPENAI_API_KEY=your_openai_key_here
- Then modify your app.py code:
```python
import os, openai
from dotenv import load_dotenv

load_dotenv()

def llm_call(prediction, params):
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        # Replace with your model and logic
        response = openai.Completion.create(
            model="gpt-4-turbo",
            prompt=f"Explain this salary prediction: {prediction}, {params}"
        )
        return response.choices[0].text
    except Exception as e:
        print("LLM Error:", e)
### ⚠️ Important:
Always match your .env variable name and the key name in your code.

## ▶️ Running the Application

### For local testing, use:
```python
if __name__ == '__main__':
    app.run(debug=True)

### For production (Render deployment), uncomment the serve() line:
Uncomment the serve() line in app.py:
```python
if __name__ == '__main__':
    # serve(app, host='0.0.0.0', port=8080)  # For production (Render)
    app.run(debug=True)  # For local testing only

## 📚 Future Enhancements

- 🔐 **Add user authentication**  
  Implement login and registration functionality for secure user access.

- 📊 **Data visualization for salary trends**  
  Integrate interactive charts to show salary distributions and trends.

- 🧠 **Multi-model AI support (Gemini / OpenAI / Claude)**  
  Allow users to choose between multiple LLM providers for generating insights.

- 🗄️ **Database integration for history tracking**  
  Store previous predictions and AI insights for future reference.