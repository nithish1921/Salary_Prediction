from flask import Flask, request, render_template, flash
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from waitress import serve
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.secret_key = "secret"

# ======== CONFIG ========
MODEL_PATH = "rf_model.pkl"
DATA_PATH = "Employers_data.csv"
FEATURE_COLUMNS = ['Age', 'Gender', 'Department', 'Job_Title',
                   'Years_of_Experience', 'Education_Level', 'Location']

# ======== LOAD MODEL ========
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# ======== LOAD CSV TO EXTRACT UNIQUE VALUES ========
df_ref = pd.read_csv(DATA_PATH)

df_ref['Education_Level'] = df_ref['Education_Level'].replace({
    "Bachelor": "Bachelor's Degree",
    "Master": "Master's Degree",
    "PhD": "PhD"
})

dropdowns = {
    'Gender': sorted(df_ref['Gender'].dropna().unique().tolist()),
    'Department': sorted(df_ref['Department'].dropna().unique().tolist()),
    'Job_Title': sorted(df_ref['Job_Title'].dropna().unique().tolist()),
    'Education_Level': sorted(df_ref['Education_Level'].dropna().unique().tolist()),
    'Location': sorted(df_ref['Location'].dropna().unique().tolist())
}

encoders = {}
for col in ['Gender', 'Department', 'Job_Title', 'Education_Level', 'Location']:
    le = LabelEncoder()
    df_ref[col] = df_ref[col].astype(str)
    le.fit(df_ref[col])
    encoders[col] = le


def encode_input(data_row):
    df = data_row.copy()
    for col in encoders:
        df[col] = encoders[col].transform(df[col].astype(str))
    return df[FEATURE_COLUMNS]


# ======== GEMINI LLM FUNCTION ========
def llm_call(prediction, params):
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        You are a friendly AI salary advisor.
        The ML model predicted: {prediction}.
        Here are the input details:
        {params}

        Write a short, human-friendly reasoning message (2-3 sentences)
        explaining why this salary prediction makes sense, mentioning
        relevant factors like education, experience, location, department or job role.
        Keep it engaging and conversational.
        """

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"(LLM explanation unavailable: {e})"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Manual Prediction
        if 'predict_manual' in request.form:
            try:
                age = float(request.form.get("Age"))
                gender = request.form.get("Gender")
                department = request.form.get("Department")
                job = request.form.get("Job_Title")
                exp = float(request.form.get("Years_of_Experience"))
                edu = request.form.get("Education_Level")
                loc = request.form.get("Location")

                if any(v.startswith("Select") for v in [gender, department, job, edu, loc]):
                    flash("Please select valid options for all dropdowns.", "danger")
                    return render_template("index.html", dropdowns=dropdowns)

                data = pd.DataFrame([{
                    'Age': age,
                    'Gender': gender,
                    'Department': department,
                    'Job_Title': job,
                    'Years_of_Experience': exp,
                    'Education_Level': edu,
                    'Location': loc
                }])

                encoded = encode_input(data)
                pred = model.predict(encoded)[0]
                label = "< $120K" if pred == 0 else ">= $120K"

                # LLM Reasoning
                llm_message = llm_call(label, data.to_dict(orient='records')[0])

                return render_template("index.html",
                                       dropdowns=dropdowns,
                                       prediction=f"Predicted Salary: {label}",
                                       llm_message=llm_message)
            except Exception as e:
                flash(f"Error: {e}", "danger")

        elif 'predict_csv' in request.form:
            try:
                file = request.files['file']
                df = pd.read_csv(file)

                df['Education_Level'] = df['Education_Level'].replace({
                    "Bachelor": "Bachelor's Degree",
                    "Master": "Master's Degree",
                    "PhD": "PhD"
                })

                df_display = df.copy()
                df_encoded = df.copy()

                for col in encoders:
                    df_encoded[col] = encoders[col].transform(df_encoded[col].astype(str))

                preds = model.predict(df_encoded[FEATURE_COLUMNS])
                df_display['Predicted_Salary'] = np.where(preds == 0, '<120K', '>=120K')

                table_html = df_display.to_html(classes='table table-striped', index=False)
                return render_template("index.html", dropdowns=dropdowns, result_table=table_html)
            except Exception as e:
                flash(f"Error reading or processing file: {e}", "danger")

    return render_template("index.html", dropdowns=dropdowns)


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080) # For production
    #app.run(debug=True)  # (For local testing only)