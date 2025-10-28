from flask import Flask, request, render_template, flash
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
app.secret_key = "secret"

# ======== CONFIG ========
MODEL_PATH = "rf_model.pkl"
DATA_PATH = "Employers_data.csv"  # used to auto-generate dropdowns
FEATURE_COLUMNS = ['Age', 'Gender', 'Department', 'Job_Title',
                   'Years_of_Experience', 'Education_Level', 'Location']

# ======== LOAD MODEL ========
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# ======== LOAD CSV TO EXTRACT UNIQUE VALUES ========
df_ref = pd.read_csv(DATA_PATH)

# Standardize Education_Level
df_ref['Education_Level'] = df_ref['Education_Level'].replace({
    "Bachelor": "Bachelor's Degree",
    "Master": "Master's Degree",
    "PhD": "PhD"
})

# Auto-generate dropdown options
dropdowns = {
    'Gender': sorted(df_ref['Gender'].dropna().unique().tolist()),
    'Department': sorted(df_ref['Department'].dropna().unique().tolist()),
    'Job_Title': sorted(df_ref['Job_Title'].dropna().unique().tolist()),
    'Education_Level': sorted(df_ref['Education_Level'].dropna().unique().tolist()),
    'Location': sorted(df_ref['Location'].dropna().unique().tolist())
}

# ======== FIT ENCODERS BASED ON THE DATASET ========
encoders = {}
for col in ['Gender', 'Department', 'Job_Title', 'Education_Level', 'Location']:
    le = LabelEncoder()
    df_ref[col] = df_ref[col].astype(str)
    le.fit(df_ref[col])
    encoders[col] = le


def encode_input(data_row):
    """Encode a single row DataFrame for prediction."""
    df = data_row.copy()
    for col in encoders:
        df[col] = encoders[col].transform(df[col].astype(str))
    return df[FEATURE_COLUMNS]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # -------- MANUAL INPUT --------
        if 'predict_manual' in request.form:
            try:
                age = float(request.form.get("Age"))
                gender = request.form.get("Gender")
                department = request.form.get("Department")
                job = request.form.get("Job_Title")
                exp = float(request.form.get("Years_of_Experience"))
                edu = request.form.get("Education_Level")
                loc = request.form.get("Location")

                # Validate dropdowns not left at placeholder
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
                label = "<120K" if pred == 0 else ">=120K"

                return render_template("index.html",
                                       dropdowns=dropdowns,
                                       prediction=f"Predicted Salary: {label}")
            except Exception as e:
                flash(f"Error: {e}", "danger")

        # -------- BULK PREDICTION --------
        elif 'predict_csv' in request.form:
            try:
                file = request.files['file']
                df = pd.read_csv(file)

                # Standardize education naming
                df['Education_Level'] = df['Education_Level'].replace({
                    "Bachelor": "Bachelor's Degree",
                    "Master": "Master's Degree",
                    "PhD": "PhD"
                })

                # Keep a copy of original (for user display)
                df_display = df.copy()

                # Encode only for prediction
                df_encoded = df.copy()
                for col in encoders:
                    df_encoded[col] = encoders[col].transform(df_encoded[col].astype(str))

                preds = model.predict(df_encoded[FEATURE_COLUMNS])
                df_display['Predicted_Salary'] = np.where(preds == 0, '<120K', '>=120K')

                # Show human-readable version
                table_html = df_display.to_html(classes='table table-striped', index=False)

                return render_template("index.html",
                                       dropdowns=dropdowns,
                                       result_table=table_html)
            except Exception as e:
                flash(f"Error reading or processing file: {e}", "danger")

    return render_template("index.html", dropdowns=dropdowns)


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)