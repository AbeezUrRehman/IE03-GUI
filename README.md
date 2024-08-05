# Book Recommendation System

## Overview
This project is a book recommendation system implemented using Flask. The system allows users to input data either through text or file uploads to receive book recommendations. It also includes a test data generator for generating sample data for various tasks.

## Features
- **Task 1-6**: Each task provides a different functionality related to book recommendations, such as rating books, recommending books based on user ratings, etc.
- **File Upload**: Supports file uploads for input data, making it easy to test with large datasets.
- **Test Data Generator**: A script to generate test data for all tasks.

## Setup Instructions

### Prerequisites
- **Python**: Make sure you have Python installed. You can download it from [Python's official website](https://www.python.org/).
- **Pip**: The Python package installer. It usually comes with Python, but you can also install it separately.

### Installation

1. **Clone the Repository**: Clone the project repository to your local machine.
    ```sh
    git clone https://github.com/AbeezUrRehman/IE03-GUI/tree/Database-integration-all-tasks
    cd book-recommendation-system
    ```

2. **Create a Virtual Environment**: (Optional but recommended)
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Required Packages**:
    ```sh
    pip install -r requirements.txt
    ```
    If the `requirements.txt` file is not provided, install the following packages:
    ```sh
    pip install flask
    ```

### Running the Application

1. **Start the Flask Application**:
    ```sh
    python app.py
    ```

2. **Access the Web Interface**: Open your browser and go to [http://localhost:5000/](http://localhost:5000/) to use the application.

## Usage

- **Task Pages**: Navigate to specific task pages (e.g., `/task1`, `/task2`, etc.) to perform various book recommendation tasks. Each task page allows you to input data either through a text area or by uploading a file.

- **Input Data**: The input data can be provided as plain text or uploaded as a file. The format of the input data may vary depending on the task.

## Test Data Generator

A test data generator script (`generate_test_data.py`) is provided to generate sample data for testing purposes.

### Usage
To generate test data for a specific task, use the following command:
```sh
python generate_test_data.py task --N <number> --M <number> --E <number> --R <number> --Q <number> --doc_count <number>
```