from flask import Flask, render_template, request
import datetime
from datetime import timedelta
import sqlite3

app = Flask(__name__)

DATABASE = "/home/nick/programming/networklogger/internet_dropouts.db"

def get_dropouts(min_duration=None, max_duration=None):
	conn = sqlite3.connect(DATABASE)
	cursor = conn.cursor()
	
	query = 'SELECT * FROM dropouts WHERE 1=1'
	params = []

	if min_duration:
		query += ' AND duration >= ?'
		params.append(min_duration)
	if max_duration:
		query += ' AND duration <= ?'
		params.append(max_duration)

	query += ' ORDER BY start_time DESC'

	cursor.execute(query, params)
	dropouts = cursor.fetchall()
	conn.close()
	return dropouts

@app.route("/")
def index():
	min_duration = request.args.get('min_duration', type=str)
	max_duration = request.args.get('max_duration', type=str)

	dropouts = get_dropouts(min_duration, max_duration)
	return render_template("index.html", dropouts=dropouts)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080)
