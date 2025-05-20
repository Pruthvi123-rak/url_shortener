from flask import Flask, request, redirect, render_template
import sqlite3
import string, random

app = Flask(__name__)

# DB Init
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    short TEXT UNIQUE,
                    original TEXT
                )''')
    conn.commit()
    conn.close()

# Generate random short code
def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['url']
        short = generate_short_url()

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO urls (short, original) VALUES (?, ?)", (short, original_url))
        conn.commit()
        conn.close()

        short_url = request.host_url + short
        return f'Shortened URL: <a href="{short_url}">{short_url}</a>'
    
    return render_template('index.html')

# Redirect short URL to original
@app.route('/<short>')
def redirect_url(short):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT original FROM urls WHERE short = ?", (short,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return redirect(result[0])
    return 'URL not found', 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
