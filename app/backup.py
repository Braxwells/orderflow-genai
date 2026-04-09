import os
import shutil
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

DB_PATH     = os.getenv("DATABASE_URL", "sqlite:///./orderflow.db").replace("sqlite:///", "")
BACKUP_DIR  = os.getenv("BACKUP_DIR", "./backups")
MAX_BACKUPS = 30


def run_backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = os.path.join(BACKUP_DIR, f"orderflow_{timestamp}.db")
    if os.path.exists(DB_PATH):
        shutil.copy2(DB_PATH, dest)
        print(f"[Backup] Guardado: {dest}")
        _rotate_backups()
    else:
        print(f"[Backup] BD no encontrada en {DB_PATH}")


def _rotate_backups():
    backups = sorted([
        os.path.join(BACKUP_DIR, f)
        for f in os.listdir(BACKUP_DIR)
        if f.startswith("orderflow_") and f.endswith(".db")
    ])
    while len(backups) > MAX_BACKUPS:
        os.remove(backups.pop(0))


def start_backup_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_backup, "interval", hours=24)
    scheduler.start()
    print("[Backup] Scheduler iniciado — backup cada 24h")