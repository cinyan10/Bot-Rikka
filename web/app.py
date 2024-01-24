from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from config import *
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        steamid = request.form['steamid']
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        try:
            cursor.execute("UPDATE firstjoin.firstjoin SET whitelist = 1 WHERE auth = %s", (steamid,))
            db.commit()
            message = "Whitelist updated successfully."
        except mysql.connector.Error as err:
            message = f"Error: {err}"
        finally:
            cursor.close()
            db.close()
        return render_template('index.html', message=message)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
