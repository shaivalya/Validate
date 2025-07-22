from flask import Flask, request, send_file, render_template
import pandas as pd
import io
import json

app = Flask(__name__)

def is_valid_json(value):
    try:
        if isinstance(value, str) and value.strip().startswith("{") and value.strip().endswith("}"):
            json.loads(value)
            return True
    except:
        return False
    return False

def clean_dataframe(df):
    report = {
        "original_rows": len(df),
        "original_cols": len(df.columns),
        "removed_null_rows": 0,
        "removed_json_errors": 0,
        "removed_duplicate_ids": 0
    }

    # Standardize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Remove null rows
    null_mask = df.isnull().any(axis=1)
    report["removed_null_rows"] = null_mask.sum()
    df = df[~null_mask]

    # Remove invalid JSON rows
    json_errors = pd.Series([False]*len(df))
    for col in df.columns:
        if df[col].astype(str).str.startswith('{').any():
            json_errors |= ~df[col].apply(is_valid_json)
    report["removed_json_errors"] = json_errors.sum()
    df = df[~json_errors]

    # Drop duplicates by clientid (keep first)
    if "clientid" in df.columns:
        dup_mask = df.duplicated(subset="clientid", keep='first')
        report["removed_duplicate_ids"] = dup_mask.sum()
        df = df[~dup_mask]

    # Final shape
    report["cleaned_rows"] = len(df)
    report["cleaned_cols"] = len(df.columns)

    return df, report

@app.route("/")
def home():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == "":
        return "No selected file", 400

    try:
        df = pd.read_csv(file)
        cleaned_df, report = clean_dataframe(df)

        buffer = io.StringIO()
        cleaned_df.to_csv(buffer, index=False)
        buffer.seek(0)

        # Convert report to basic Python types
        safe_report = {k: int(v) for k, v in report.items()}
        response = send_file(
            io.BytesIO(buffer.getvalue().encode()),
            mimetype='text/csv',
            download_name="cleaned_data.csv",
            as_attachment=True
        )
        response.headers["X-Cleaning-Report"] = json.dumps(safe_report)
        return response

    except Exception as e:
        return f"❌ Error processing file: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)


