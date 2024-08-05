from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import numpy as np
import json
import os
import subprocess
import networkx as nx
import requests
from bs4 import BeautifulSoup
from tasks.task1 import process_task1
from tasks.task2 import process_task2
from tasks.task3 import process_task3
from tasks.task4 import process_task4, evaluate_command
from tasks.task5 import process_task5
from tasks.task6 import process_task6
from tasks.task7 import get_scores, format_scores
from tasks.task8 import get_combined_scores, format_scores as format_combined_scores
from tasks.task9 import create_schema, insert_data

app = Flask(__name__)

# Initialize database connection
def get_db_connection():
    conn = sqlite3.connect('book_recommendations.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Routes for tasks 1-9
@app.route('/task1', methods=['GET', 'POST'])
def task1():
    if request.method == 'POST':
        # Check if a file was uploaded
        input_file = request.files.get('input_file')
        input_data = request.form.get('input_data')

        if input_file:
            # Read the content of the file
            input_data = input_file.read().decode('utf-8')
        elif input_data:
            # Use the text area input data
            pass
        else:
            return "No input provided", 400

        # Process the input data (example processing)
        result = process_task1(input_data)

        return render_template('task1.html', result=result)

    return render_template('task1.html')

@app.route('/task2', methods=['GET', 'POST'])
def task2():
    result = None
    if request.method == 'POST':
        input_data = request.form['input_data']
        result = process_task2(input_data)
    return render_template('task2.html', result=result)

@app.route('/task3', methods=['GET', 'POST'])
def task3():
    result = None
    if request.method == 'POST':
        input_data = request.form['input_data']
        result = process_task3(input_data)
    return render_template('task3.html', result=result)

@app.route('/task4', methods=['GET', 'POST'])
def task4():
    result = None
    command_result = None
    N, M, ratings = None, None, None
    if request.method == 'POST':
        if 'input_data' in request.form:
            input_data = request.form['input_data']
            N, M, ratings = process_task4(input_data)
            ratings_json = json.dumps(ratings.tolist())
        if 'command' in request.form:
            command = request.form['command']
            N = int(request.form['N'])
            M = int(request.form['M'])
            ratings_json = request.form['ratings_json']
            ratings = np.array(json.loads(ratings_json))
            command_result = evaluate_command(command, ratings, N, M)
    return render_template('task4.html', result=result, command_result=command_result, N=N, M=M, ratings_json=ratings_json)

@app.route('/task5', methods=['GET', 'POST'])
def task5():
    result = None
    if request.method == 'POST':
        input_data = request.form['input_data']
        result = process_task5(input_data)
    return render_template('task5.html', result=result)

@app.route('/task6', methods=['GET', 'POST'])
def task6():
    result = None
    if request.method == 'POST':
        input_data = request.form['input_data']
        result = process_task6(input_data)
    return render_template('task6.html', result=result)

@app.route('/task7', methods=['GET', 'POST'])
def task7():
    result = None
    if request.method == 'POST':
        uploaded_files = request.files.getlist("files[]")
        directory = "uploads"
        os.makedirs(directory, exist_ok=True)
        for file in uploaded_files:
            file.save(os.path.join(directory, file.filename))
        scores = get_scores(directory)
        result = format_scores(scores)
    return render_template('task7.html', result=result)

@app.route('/task8', methods=['GET', 'POST'])
def task8():
    result = None
    if request.method == 'POST':
        uploaded_files = request.files.getlist("files[]")
        query = request.form['query']
        directory = "uploads_task8"
        os.makedirs(directory, exist_ok=True)
        for file in uploaded_files:
            file.save(os.path.join(directory, file.filename))
        importance_scores, relevance_scores, combined_scores = get_combined_scores(directory, query)
        result = format_combined_scores(importance_scores, relevance_scores, combined_scores)
    return render_template('task8.html', result=result)

@app.route('/task9', methods=['GET', 'POST'])
def task9():
    result = None
    if request.method == 'POST':
        urls = request.form['urls'].split(',')
        words = request.form['words'].split(',')
        links = [tuple(link.split(',')) for link in request.form['links'].split(';')]
        locations = [tuple(location.split(',')) for location in request.form['locations'].split(';')]
        pageranks = dict(item.split(':') for item in request.form['pageranks'].split(','))
        conn = sqlite3.connect('book_recommendations.db')
        cursor = conn.cursor()
        create_schema(cursor)
        insert_data(cursor, urls, words, links, locations, pageranks)
        conn.commit()
        conn.close()
        result = "Data inserted successfully."
    return render_template('task9.html', result=result)

# Users management routes
@app.route('/users')
def users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('users.html', users=users)

@app.route('/add_user', methods=('GET', 'POST'))
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        conn = get_db_connection()
        conn.execute('INSERT INTO users (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
        return redirect(url_for('users'))
    return render_template('add_user.html')

@app.route('/edit_user/<int:id>', methods=('GET', 'POST'))
def edit_user(id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        conn.execute('UPDATE users SET name = ? WHERE id = ?', (name, id))
        conn.commit()
        conn.close()
        return redirect(url_for('users'))

    conn.close()
    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:id>', methods=('POST',))
def delete_user(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('users'))

# Books management routes
@app.route('/books')
def books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('books.html', books=books)

@app.route('/add_book', methods=('GET', 'POST'))
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        conn = get_db_connection()
        conn.execute('INSERT INTO books (title, author, description) VALUES (?, ?, ?)', (title, author, description))
        conn.commit()
        conn.close()
        return redirect(url_for('books'))
    return render_template('add_book.html')

@app.route('/edit_book/<int:id>', methods=('GET', 'POST'))
def edit_book(id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        conn.execute('UPDATE books SET title = ?, author = ?, description = ? WHERE id = ?', (title, author, description, id))
        conn.commit()
        conn.close()
        return redirect(url_for('books'))

    conn.close()
    return render_template('edit_book.html', book=book)

@app.route('/delete_book/<int:id>', methods=('POST',))
def delete_book(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('books'))

# Friendships management routes
@app.route('/friendships')
def friendships():
    conn = get_db_connection()
    friendships = conn.execute('SELECT * FROM friendships').fetchall()
    conn.close()
    return render_template('friendships.html', friendships=friendships)

@app.route('/add_friendship', methods=('GET', 'POST'))
def add_friendship():
    if request.method == 'POST':
        user_id = request.form['user_id']
        friend_id = request.form['friend_id']
        conn = get_db_connection()
        conn.execute('INSERT INTO friendships (user_id, friend_id) VALUES (?, ?)', (user_id, friend_id))
        conn.commit()
        conn.close()
        return redirect(url_for('friendships'))
    return render_template('add_friendship.html')

@app.route('/edit_friendship/<int:id>', methods=('GET', 'POST'))
def edit_friendship(id):
    conn = get_db_connection()
    friendship = conn.execute('SELECT * FROM friendships WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        user_id = request.form['user_id']
        friend_id = request.form['friend_id']
        conn.execute('UPDATE friendships SET user_id = ?, friend_id = ? WHERE id = ?', (user_id, friend_id, id))
        conn.commit()
        conn.close()
        return redirect(url_for('friendships'))

    conn.close()
    return render_template('edit_friendship.html', friendship=friendship)

@app.route('/delete_friendship/<int:id>', methods=('POST',))
def delete_friendship(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM friendships WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('friendships'))

# Documents management routes
@app.route('/documents')
def documents():
    conn = get_db_connection()
    documents = conn.execute('SELECT * FROM documents').fetchall()
    conn.close()
    return render_template('documents.html', documents=documents)

@app.route('/add_document', methods=('GET', 'POST'))
def add_document():
    if request.method == 'POST':
        book_id = request.form['book_id']
        content = request.form['content']
        conn = get_db_connection()
        conn.execute('INSERT INTO documents (book_id, content) VALUES (?, ?)', (book_id, content))
        conn.commit()
        conn.close()
        return redirect(url_for('documents'))
    return render_template('add_document.html')

@app.route('/edit_document/<int:id>', methods=('GET', 'POST'))
def edit_document(id):
    conn = get_db_connection()
    document = conn.execute('SELECT * FROM documents WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        book_id = request.form['book_id']
        content = request.form['content']
        conn.execute('UPDATE documents SET book_id = ?, content = ? WHERE id = ?', (book_id, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('documents'))

    conn.close()
    return render_template('edit_document.html', document=document)

@app.route('/delete_document/<int:id>', methods=('POST',))
def delete_document(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM documents WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('documents'))

def get_recommendations(user_id, max_distance):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT books.title, books.author
        FROM friendships
        JOIN users ON users.id = friendships.friend_id
        JOIN recommendations ON recommendations.user_id = users.id
        JOIN books ON books.id = recommendations.book_id
        WHERE friendships.user_id = ? AND friendships.distance <= ?
        ORDER BY recommendations.score DESC
    ''', (user_id, max_distance))
    
    recommendations = cursor.fetchall()
    conn.close()
    return recommendations

@app.route('/recommendations/<int:user_id>')
def recommendations(user_id):
    max_distance = request.args.get('max_distance', default=3, type=int)
    recs = get_recommendations(user_id, max_distance)
    return render_template('recommendations.html', recommendations=recs)


def get_groups():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id, friend_id FROM friendships')
    edges = cursor.fetchall()
    conn.close()
    
    G = nx.DiGraph()
    G.add_edges_from(edges)
    groups = list(nx.strongly_connected_components(G))
    
    return groups

def get_recommendations_from_group(user_id):
    groups = get_groups()
    user_group = None
    for group in groups:
        if user_id in group:
            user_group = group
            break
    
    if not user_group:
        return []
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT books.title, books.author
        FROM friendships
        JOIN users ON users.id = friendships.friend_id
        JOIN recommendations ON recommendations.user_id = users.id
        JOIN books ON books.id = recommendations.book_id
        WHERE friendships.user_id = ? AND friendships.friend_id IN ({})
        ORDER BY recommendations.score DESC
    '''.format(','.join('?'*len(user_group))), (user_id, *user_group))
    
    recommendations = cursor.fetchall()
    conn.close()
    return recommendations

@app.route('/recommendations_group/<int:user_id>')
def recommendations_group(user_id):
    recs = get_recommendations_from_group(user_id)
    return render_template('recommendations.html', recommendations=recs)



def crawl(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    content = soup.get_text()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO documents (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()

    for link in soup.find_all('a'):
        link_url = link.get('href')
        if link_url:
            crawl(link_url)

# Example usage: crawl('http://example.com')

def search_phrase(phrase):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM documents WHERE content LIKE ?', ('%' + phrase + '%',))
    results = cursor.fetchall()
    conn.close()
    return results

def search_wildcard(pattern):
    pattern = pattern.replace('*', '%')
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM documents WHERE content LIKE ?', (pattern,))
    results = cursor.fetchall()
    conn.close()
    return results

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        phrase = request.form['phrase']
        results = search_phrase(phrase)
        return render_template('search_results.html', results=results)
    return render_template('search.html')

def search_wildcard(pattern):
    pattern = pattern.replace('*', '%')
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM documents WHERE content LIKE ?', (pattern,))
    results = cursor.fetchall()
    conn.close()
    return results

@app.route('/search_wildcard', methods=['GET', 'POST'])
def search_wildcard_view():
    if request.method == 'POST':
        pattern = request.form['pattern']
        results = search_wildcard(pattern)
        return render_template('search_results.html', results=results)
    return render_template('wild_search.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate_data():
    if request.method == 'POST':
        task = request.form['task']
        N = request.form.get('N')
        M = request.form.get('M')
        E = request.form.get('E')
        R = request.form.get('R')
        Q = request.form.get('Q')
        doc_count = request.form.get('doc_count')

        # Command generation based on input
        cmd = ['python3', 'generate_test_data.py', task]
        if N: cmd.extend(['--N', N])
        if M: cmd.extend(['--M', M])
        if E: cmd.extend(['--E', E])
        if R: cmd.extend(['--R', R])
        if Q: cmd.extend(['--Q', Q])
        if doc_count: cmd.extend(['--doc_count', doc_count])

        try:
            # Execute the command
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Log the output for debugging
            print("stdout:", result.stdout.decode())
            print("stderr:", result.stderr.decode())

            # Define the expected output filename
            output_filename = f"{task}_input.txt"
            output_path = os.path.join(os.getcwd(), output_filename)

            # Check if file exists
            if not os.path.exists(output_path):
                raise FileNotFoundError(f"Expected output file not found: {output_path}")

            return send_file(output_path, as_attachment=True)

        except subprocess.CalledProcessError as e:
            print(f"Command '{' '.join(cmd)}' failed with error:")
            print(e.stderr.decode())
            return f"An error occurred: {e.stderr.decode()}", 500
        except FileNotFoundError as e:
            print(f"FileNotFoundError: {e}")
            return f"An error occurred: {e}", 500
        except Exception as e:
            print(f"Unexpected error: {e}")
            return f"An unexpected error occurred: {e}", 500

    return render_template('generate.html')

if __name__ == '__main__':
    app.run(debug=True)
