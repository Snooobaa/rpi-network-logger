from flask import Flask, render_template, request
from dotenv import load_dotenv
import datetime
from datetime import timedelta
import sqlite3
import os

app = Flask(__name__)

load_dotenv(override=True)

DATABASE = os.getenv("DATABASE_PATH")

def get_dropouts(min_duration=None, max_duration=None):
	conn = sqlite3.connect(DATABASE)
	cursor = conn.cursor()
	
	query = 'SELECT * FROM dropouts WHERE 1=1'
	params = []

	if min_duration:
		query += ' AND duration_seconds >= ?'
		params.append(float(min_duration))
	if max_duration:
		query += ' AND duration_seconds <= ?'
		params.append(float(max_duration))

	query += ' ORDER BY start_time DESC'

	cursor.execute(query, params)
	dropouts = cursor.fetchall()
	conn.close()
	return dropouts

@app.route("/")
def index():
	min_duration = request.args.get('min_duration', type=float)
	max_duration = request.args.get('max_duration', type=float)

	dropouts = get_dropouts(min_duration, max_duration)
	return render_template("index.html", dropouts=dropouts)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080)
