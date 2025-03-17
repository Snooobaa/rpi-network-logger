import sqlite3
import time
import subprocess
import datetime
import os
from dotenv import load_dotenv

load_dotenv(override=True)

PING_TARGET = "8.8.8.8"
CHECK_INTERVAL = 0.5

conn = sqlite3.connect(os.getenv("DATABASE_PATH"))
cursor = conn.cursor()

cursor.execute('''
	CREATE TABLE IF NOT EXISTS dropouts (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		start_time TEXT NOT NULL,
		end_time TEXT NOT NULL,
		duration TEXT NOT NULL,
		duration_seconds REAL NOT NULL
	)
''')
conn.commit()

def log_dropout(start_time, end_time):
	duration = end_time - start_time
	duration_seconds = duration.total_seconds()
	cursor.execute('''
		INSERT INTO dropouts (start_time, end_time, duration, duration_seconds)
		VALUES (?, ?, ?, ?)
	''', (start_time.isoformat(), end_time.isoformat(), str(duration), duration_seconds))
	conn.commit()

def check_internet():
	try:
		output = subprocess.check_output(["ping", "-c", "1", PING_TARGET], stderr=subprocess.STDOUT, universal_newlines=True)
		return True
	except subprocess.CalledProcessError:
		return False

def main():
	dropout_start = None

	while True:
		if not check_internet():
			if dropout_start is None:
				dropout_start = datetime.datetime.now()
				print("Internet dropout detected. Logging...")
		else:
			if dropout_start is not None:
				dropout_end = datetime.datetime.now()
				log_dropout(dropout_start,  dropout_end)
				dropout_start = None
				print("Internet restored. Logged.")

		time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
	main()

