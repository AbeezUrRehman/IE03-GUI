from flask import Flask, json, render_template, request, redirect, url_for
import numpy as np
import os
from tasks.task1 import process_task1
from tasks.task2 import process_task2
from tasks.task3 import process_task3
from tasks.task4 import process_task4, evaluate_command
from tasks.task5 import process_task5
from tasks.task6 import process_task6
from tasks.task7 import get_scores, format_scores
from tasks.task8 import get_combined_scores, format_scores as format_combined_scores

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Routes for tasks 1-8
@app.route('/task1', methods=['GET', 'POST'])
def task1():
    result = None
    if request.method == 'POST':
        input_data = request.form['input_data']
        result = process_task1(input_data)
    return render_template('task1.html', result=result)

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
    N, M, ratings = None, None, None
    command_result = None
    ratings_json = None  # Initialize with None
    if request.method == 'POST':
        input_data = request.form['input_data']
        try:
            N, M, ratings = process_task4(input_data)
            ratings_json = json.dumps(ratings.tolist())  # Convert to JSON string for passing in URL
            command = request.form.get('command')
            if command:
                command_result = evaluate_command(command, ratings, N, M)
        except ValueError as e:
            result = str(e)

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

if __name__ == '__main__':
    app.run(debug=True)
