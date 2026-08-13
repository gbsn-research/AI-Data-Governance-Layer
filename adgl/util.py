from datetime import datetime, timezone
import json

def now_iso(): return datetime.now(timezone.utc).isoformat()

def get_path(obj, path, default=None):
    cur = obj
    for part in path.split('.'):
        if isinstance(cur, dict) and part in cur: cur = cur[part]
        else: return default
    return cur

def set_path(obj, path, value):
    parts = path.split('.')
    cur = obj
    for part in parts[:-1]: cur = cur.setdefault(part,{})
    cur[parts[-1]] = value

def deep_copy_json(obj): return json.loads(json.dumps(obj))
