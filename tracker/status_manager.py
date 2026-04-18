import os
import json
import datetime
from .log_reader import get_all_log_files, invalidate_applications_cache

APPLICATION_STATUSES = {
    "not_applied": {"label": "Not Applied Yet", "emoji": "⏳"},
    "applied": {"label": "Applied", "emoji": "✅"},
    "interviewing": {"label": "Interviewing", "emoji": "🗣️"},
    "offer_received": {"label": "Offer Received", "emoji": "🎉"},
    "rejected": {"label": "Rejected", "emoji": "❌"},
    "withdrawn": {"label": "Withdrawn", "emoji": "🛑"}
}

def get_status_file_path():
    return os.path.join('logs', 'application_statuses.json')

def load_all_statuses():
    file_path = get_status_file_path()
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_status(log_id, status_key, notes=""):
    if status_key not in APPLICATION_STATUSES:
        raise ValueError(f"Invalid status_key: {status_key}")
        
    statuses = load_all_statuses()
    statuses[log_id] = {
        "status_key": status_key,
        "notes": notes,
        "updated_at": datetime.datetime.now().isoformat()
    }
    
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    with open(get_status_file_path(), "w", encoding="utf-8") as f:
        json.dump(statuses, f, indent=2)
    invalidate_applications_cache()

def get_status(log_id):
    statuses = load_all_statuses()
    return statuses.get(log_id, {
        "status_key": "not_applied",
        "notes": "",
        "updated_at": None
    })

def get_status_label(log_id):
    status = get_status(log_id)
    key = status.get("status_key", "not_applied")
    info = APPLICATION_STATUSES.get(key, APPLICATION_STATUSES["not_applied"])
    return f"{info['emoji']} {info['label']}"

def get_applications_by_status(status_key):
    statuses = load_all_statuses()
    return [log_id for log_id, data in statuses.items() if data.get("status_key") == status_key]

def get_status_statistics():
    statuses = load_all_statuses()
    stats = {k: 0 for k in APPLICATION_STATUSES.keys()}
    
    all_files = get_all_log_files()
    all_log_ids = [os.path.splitext(os.path.basename(f))[0] for f in all_files]
    
    for log_id in all_log_ids:
        st = statuses.get(log_id, {}).get("status_key", "not_applied")
        if st in stats:
            stats[st] += 1
            
    return stats
