import os
from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS so React can access this API

@app.route("/api/data")
def get_data():
    try:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "labeled_log.csv"))
        print(f"🔍 [Data] Trying to load CSV from: {path}")
        df = pd.read_csv(path)
        df["Duration"] = pd.to_timedelta(df["Duration"])
        df["Duration (Minutes)"] = df["Duration"].dt.total_seconds() / 60
        # Convert Timedelta to string for JSON serialization
        df["Duration"] = df["Duration"].astype(str)
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        print("❌ [Data] ERROR:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/api/usage")
def get_usage():
    print("🔄 /api/usage called")
    try:
        print("📂 Reading CSV file...")
        df = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "labeled_log.csv")))
        print("✅ CSV loaded")

        df["Duration"] = pd.to_timedelta(df["Duration"])
        df["Duration (Minutes)"] = df["Duration"].dt.total_seconds() / 60
        category_summary = df.groupby("Category")["Duration (Minutes)"].sum().reset_index()
        print("📊 Data processed successfully")
        return jsonify(category_summary.to_dict(orient="records"))
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
