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

@app.route("/api/timesheet")
def get_timesheet():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "labeled_log.csv"))
    sessions = []
    if not os.path.exists(path):
        return jsonify([])
    df = pd.read_csv(path)
    # Group consecutive 'Work' sessions
    grouped = []
    prev_type = None
    group_start = None
    group_end = None
    group_duration = pd.Timedelta(0)
    for idx, row in df.iterrows():
        label = 'Meal' if str(row.get('Category', '')).lower() == 'meal' else 'Work'
        start = row['Start Time']
        end = row['End Time']
        duration = pd.to_timedelta(row['Duration']) if 'Duration' in row else pd.Timedelta(0)
        if label == 'Work':
            if prev_type == 'Work' and group_end == start:
                # Extend current group
                group_end = end
                group_duration += duration
            else:
                # Save previous group
                if prev_type == 'Work':
                    grouped.append({
                        'type': 'Work',
                        'start_time': group_start,
                        'end_time': group_end,
                        'duration': str(group_duration)
                    })
                # Start new group
                group_start = start
                group_end = end
                group_duration = duration
            prev_type = 'Work'
        else:
            # Save previous work group
            if prev_type == 'Work':
                grouped.append({
                    'type': 'Work',
                    'start_time': group_start,
                    'end_time': group_end,
                    'duration': str(group_duration)
                })
            # Add meal as its own session
            grouped.append({
                'type': 'Meal',
                'start_time': start,
                'end_time': end,
                'duration': str(duration)
            })
            prev_type = 'Meal'
            group_start = None
            group_end = None
            group_duration = pd.Timedelta(0)
    # Save last group if needed
    if prev_type == 'Work':
        grouped.append({
            'type': 'Work',
            'start_time': group_start,
            'end_time': group_end,
            'duration': str(group_duration)
        })
    return jsonify(grouped)

@app.route("/api/timesheet/edit", methods=["POST"])
def edit_timesheet():
    from flask import request
    data = request.json
    idx = data.get('idx')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "labeled_log.csv"))
    df = pd.read_csv(path)
    if 0 <= idx < len(df):
        df.at[idx, 'Start Time'] = start_time
        df.at[idx, 'End Time'] = end_time
        # Update duration
        try:
            dt1 = pd.to_datetime(start_time)
            dt2 = pd.to_datetime(end_time)
            df.at[idx, 'Duration'] = str(dt2 - dt1)
        except Exception:
            pass
        df.to_csv(path, index=False)
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Invalid index'})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
