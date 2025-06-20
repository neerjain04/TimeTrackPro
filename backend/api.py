import os
from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
import subprocess
import sys
import psutil
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS so React can access this API

@app.route("/api/data")
def get_data():
    try:
        date_str = request.args.get('date')
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "labeled_log.csv"))
        print(f"🔍 [Data] Trying to load CSV from: {path}")
        df = pd.read_csv(path)
        if date_str:
            df['Date'] = pd.to_datetime(df['Start Time']).dt.date
            selected_date = pd.to_datetime(date_str).date()
            df = df[df['Date'] == selected_date]
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
        date_str = request.args.get('date')
        print("📂 Reading CSV file...")
        df = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "labeled_log.csv")))
        if date_str:
            df['Date'] = pd.to_datetime(df['Start Time']).dt.date
            selected_date = pd.to_datetime(date_str).date()
            df = df[df['Date'] == selected_date]
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
    # Accept ?date=YYYY-MM-DD, default to today
    date_str = request.args.get('date')
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", f"labeled_log_{date_str}.csv"))
    if not os.path.exists(path):
        # fallback to main file for any date
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "labeled_log.csv"))
    sessions = []
    if not os.path.exists(path):
        return jsonify([])
    df = pd.read_csv(path)
    # Filter to only rows matching the selected date
    df['Date'] = pd.to_datetime(df['Start Time']).dt.date
    selected_date = pd.to_datetime(date_str).date()
    df = df[df['Date'] == selected_date]
    # Group consecutive 'Work' sessions, track indices, but only within the same day
    grouped = []
    prev_type = None
    group_start = None
    group_end = None
    group_duration = pd.Timedelta(0)
    group_indices = []
    for idx, row in df.iterrows():
        label = 'Meal' if str(row.get('Category', '')).lower() == 'meal' else 'Work'
        start = row['Start Time']
        end = row['End Time']
        duration = pd.to_timedelta(row['Duration']) if 'Duration' in row else pd.Timedelta(0)
        # Only merge if same type and same day
        if label == 'Work':
            if prev_type == 'Work' and group_end == start:
                group_end = end
                group_duration += duration
                group_indices.append(idx)
            else:
                if prev_type == 'Work':
                    grouped.append({
                        'type': 'Work',
                        'start_time': group_start,
                        'end_time': group_end,
                        'duration': str(group_duration),
                        'indices': group_indices.copy()
                    })
                group_start = start
                group_end = end
                group_duration = duration
                group_indices = [idx]
            prev_type = 'Work'
        else:
            if prev_type == 'Work':
                grouped.append({
                    'type': 'Work',
                    'start_time': group_start,
                    'end_time': group_end,
                    'duration': str(group_duration),
                    'indices': group_indices.copy()
                })
            grouped.append({
                'type': label,
                'start_time': start,
                'end_time': end,
                'duration': str(duration),
                'indices': [idx]
            })
            prev_type = label
            group_start = None
            group_end = None
            group_duration = pd.Timedelta(0)
            group_indices = []
    if prev_type == 'Work':
        grouped.append({
            'type': 'Work',
            'start_time': group_start,
            'end_time': group_end,
            'duration': str(group_duration),
            'indices': group_indices.copy()
        })
    return jsonify(grouped)

@app.route("/api/timesheet/edit", methods=["POST"])
def edit_timesheet():
    data = request.json
    indices = data.get('indices', [])
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    new_type = data.get('type')
    date_str = data.get('date')
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", f"labeled_log_{date_str}.csv"))
    if not os.path.exists(path):
        # fallback to old file for today only
        if date_str == datetime.now().strftime('%Y-%m-%d'):
            path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "labeled_log.csv"))
    if not os.path.exists(path):
        return jsonify({'success': False, 'error': 'File not found'})
    df = pd.read_csv(path)
    updated = False
    for idx in indices:
        if 0 <= idx < len(df):
            df.at[idx, 'Start Time'] = start_time
            df.at[idx, 'End Time'] = end_time
            if new_type:
                df.at[idx, 'Category'] = new_type
            # Update duration
            try:
                dt1 = pd.to_datetime(start_time)
                dt2 = pd.to_datetime(end_time)
                df.at[idx, 'Duration'] = str(dt2 - dt1)
            except Exception:
                pass
            updated = True
    if updated:
        df.to_csv(path, index=False)
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Invalid indices'})

@app.route("/api/tracking/start", methods=["POST"])
def api_start_tracking():
    try:
        # Call the tray app's start_tracking logic via a subprocess or IPC
        # For now, call tracker.py directly (assumes backend has permissions)
        tracker_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "tracker.py"))
        python_exec = sys.executable
        subprocess.Popen([python_exec, tracker_path])
        return jsonify({"success": True, "message": "Tracking started"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/tracking/stop", methods=["POST"])
def api_stop_tracking():
    try:
        # Find and terminate tracker.py process (simple version)
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['cmdline'] and 'tracker.py' in proc.info['cmdline']:
                proc.terminate()
        # After stopping tracking, run categorizer in the background to sync labeled_log.csv
        categorizer_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "categorizer.py"))
        python_exec = sys.executable
        subprocess.Popen([python_exec, categorizer_path])
        return jsonify({"success": True, "message": "Tracking stopped and logs syncing in background"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/timesheet_raw")
def get_timesheet_raw():
    date_str = request.args.get('date')
    min_duration = int(request.args.get('min_duration', 0))  # seconds
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", f"labeled_log_{date_str}.csv"))
    if not os.path.exists(path):
        # fallback to main file for any date
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "labeled_log.csv"))
    if not os.path.exists(path):
        return jsonify([])
    df = pd.read_csv(path)
    # Filter to only rows matching the selected date
    df['Date'] = pd.to_datetime(df['Start Time']).dt.date
    selected_date = pd.to_datetime(date_str).date()
    df = df[df['Date'] == selected_date]
    # Sort by start time to ensure correct merging
    df = df.sort_values(by='Start Time')
    merged = []
    work_block = None
    for idx, row in df.reset_index().iterrows():
        category = str(row.get('Category', '')).strip().lower()
        start = pd.to_datetime(row['Start Time'])
        end = pd.to_datetime(row['End Time'])
        duration = (end - start).total_seconds()
        if category == 'meal':
            # Close current work block if open
            if work_block:
                if work_block['duration'] >= min_duration:
                    merged.append(work_block)
                work_block = None
            # Add meal as its own block
            merged.append({
                'type': 'Meal',
                'start': start,
                'end': end,
                'duration': str(pd.to_timedelta(duration, unit='s')),
                'indices': [row['index']],
                'start_time': row['Start Time'],
                'end_time': row['End Time'],
                'raw_duration': row['Duration'],
                'idx': row['index']
            })
        else:
            # For any non-meal (work, idle, other), merge into work block
            if work_block is None:
                work_block = {
                    'type': 'Work',
                    'start': start,
                    'end': end,
                    'duration': duration,
                    'indices': [row['index']],
                    'start_time': row['Start Time'],
                    'end_time': row['End Time'],
                    'raw_duration': row['Duration'],
                    'idx': row['index']
                }
            else:
                work_block['end'] = end
                work_block['duration'] += duration
                work_block['indices'].append(row['index'])
                work_block['end_time'] = row['End Time']
                work_block['raw_duration'] = row['Duration']
                work_block['idx'] = row['index']
    if work_block and work_block['duration'] >= min_duration:
        merged.append(work_block)
    # Format for frontend
    for r in merged:
        if isinstance(r['duration'], (int, float)):
            r['duration'] = str(pd.to_timedelta(r['duration'], unit='s'))
    return jsonify(merged)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
