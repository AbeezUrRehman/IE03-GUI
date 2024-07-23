import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Database interaction functions
def connect_db():
    conn = sqlite3.connect('db/book_recommendations.db')
    return conn

def execute_query(query, params=()):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def fetch_query(query, params=()):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

# Initialize the main window
class LibraryManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Library Management System")
        self.geometry("600x600")

        # Create a notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Create tabs
        self.create_books_tab()
        self.create_users_tab()
        self.create_recommendations_tab()
        self.create_search_tab()
        self.create_task_buttons()

    def create_books_tab(self):
        books_tab = ttk.Frame(self.notebook)
        self.notebook.add(books_tab, text="Books")

        # Add form fields for book management
        ttk.Label(books_tab, text="Title:").grid(row=0, column=0, padx=10, pady=5)
        self.book_title_entry = ttk.Entry(books_tab)
        self.book_title_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(books_tab, text="Author:").grid(row=1, column=0, padx=10, pady=5)
        self.book_author_entry = ttk.Entry(books_tab)
        self.book_author_entry.grid(row=1, column=1, padx=10, pady=5)

        # Add buttons for book management
        ttk.Button(books_tab, text="Add Book", command=self.add_book).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(books_tab, text="Update Book", command=self.update_book).grid(row=2, column=1, padx=10, pady=10)
        ttk.Button(books_tab, text="Delete Book", command=self.delete_book).grid(row=2, column=2, padx=10, pady=10)

    def create_users_tab(self):
        users_tab = ttk.Frame(self.notebook)
        self.notebook.add(users_tab, text="Users")

        # Add form fields for user management
        ttk.Label(users_tab, text="User Name:").grid(row=0, column=0, padx=10, pady=5)
        self.user_name_entry = ttk.Entry(users_tab)
        self.user_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Add buttons for user management
        ttk.Button(users_tab, text="Add User", command=self.add_user).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(users_tab, text="Update User", command=self.update_user).grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(users_tab, text="Delete User", command=self.delete_user).grid(row=1, column=2, padx=10, pady=10)

    def create_recommendations_tab(self):
        recommendations_tab = ttk.Frame(self.notebook)
        self.notebook.add(recommendations_tab, text="Recommendations")

        # Add field for recommendations
        ttk.Label(recommendations_tab, text="Keywords:").grid(row=0, column=0, padx=10, pady=5)
        self.recommendation_keywords_entry = ttk.Entry(recommendations_tab)
        self.recommendation_keywords_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Button(recommendations_tab, text="Get Recommendations", command=self.get_recommendations).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.recommendations_list = tk.Listbox(recommendations_tab)
        self.recommendations_list.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

    def create_search_tab(self):
        search_tab = ttk.Frame(self.notebook)
        self.notebook.add(search_tab, text="Search")

        # Add field for search
        ttk.Label(search_tab, text="Search Query:").grid(row=0, column=0, padx=10, pady=5)
        self.search_query_entry = ttk.Entry(search_tab)
        self.search_query_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Button(search_tab, text="Search", command=self.search_books).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.search_results_list = tk.Listbox(search_tab)
        self.search_results_list.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

    def create_task_buttons(self):
        # Add task buttons to the main window
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(side=tk.RIGHT, padx=20, pady=20)

        ttk.Button(buttons_frame, text="Task 1", command=lambda: self.open_task_window(1)).pack(pady=5)
        ttk.Button(buttons_frame, text="Task 2", command=lambda: self.open_task_window(2)).pack(pady=5)
        ttk.Button(buttons_frame, text="Task 3", command=lambda: self.open_task_window(3)).pack(pady=5)
        ttk.Button(buttons_frame, text="Task 4", command=lambda: self.open_task_window(4)).pack(pady=5)
        ttk.Button(buttons_frame, text="Task 5", command=lambda: self.open_task_window(5)).pack(pady=5)
        ttk.Button(buttons_frame, text="Task 6", command=lambda: self.open_task_window(6)).pack(pady=5)
        ttk.Button(buttons_frame, text="Task 7", command=lambda: self.open_task_window(7)).pack(pady=5)
        ttk.Button(buttons_frame, text="Task 8", command=lambda: self.open_task_window(8)).pack(pady=5)
        ttk.Button(buttons_frame, text="Generate Test Data", command=self.generate_test_data).pack(pady=5)

    def open_task_window(self, task_number):
        task_window = tk.Toplevel(self)
        task_window.title(f"Task {task_number}")

        ttk.Label(task_window, text=f"Enter data for Task {task_number}:").pack(padx=10, pady=10)
        task_entry = tk.Text(task_window, height=10, width=40)
        task_entry.pack(padx=10, pady=10)

        submit_button = ttk.Button(task_window, text="Submit", command=lambda: self.submit_task_data(task_number, task_entry.get("1.0", tk.END), task_window))
        submit_button.pack(pady=10)

    def submit_task_data(self, task_number, data, task_window):
        # Process the data for the specified task number
        lines = data.strip().split('\n')
        if task_number == 1:
            output = self.process_task1(lines)
        elif task_number == 2:
            output = self.process_task2(lines)
        elif task_number == 3:
            output = self.process_task3(lines)
        elif task_number == 4:
            output = self.process_task4(lines)
        elif task_number == 5:
            output = self.process_task5(lines)
        # Add additional elif blocks for other tasks as needed

        # Display the output in a new window
        self.display_output(output, task_window)

        messagebox.showinfo("Info", f"Data for Task {task_number} submitted.")

    def process_task1(self, lines):
        # Parse and process task 1 data
        n, m = map(int, lines[0].split())
        matrix = [list(map(float, line.split())) for line in lines[1:]]
        # Implement the specific logic for task 1
        return f"Task 1 processed: {n} {m} {matrix}"

    def process_task2(self, lines):
        # Parse and process task 2 data
        n, m = map(int, lines[0].split())
        matrix = [list(map(float, line.split())) for line in lines[1:]]
        # Implement the specific logic for task 2
        return f"Task 2 processed: {n} {m} {matrix}"

    def process_task3(self, lines):
        # Parse and process task 3 data
        n, m, k = map(int, lines[0].split())
        entries = [list(map(float, line.split())) for line in lines[1:]]
        # Implement the specific logic for task 3
        return f"Task 3 processed: {n} {m} {k} {entries}"

    def process_task4(self, lines):
        # Parse and process task 4 data
        n, m, k = map(int, lines[0].split())
        entries = [list(map(float, line.split())) for line in lines[1:]]
        # Implement the specific logic for task 4
        return f"Task 4 processed: {n} {m} {k} {entries}"

    def process_task5(self, lines):
        # Parse and process task 5 data
        n, m = map(int, lines[0].split())
        edges = [list(map(int, line.split())) for line in lines[1:]]
        # Implement the specific logic for task 5
        return f"Task 5 processed: {n} {m} {edges}"

    def display_output(self, output, parent_window):
        output_window = tk.Toplevel(parent_window)
        output_window.title("Task Output")
        output_text = tk.Text(output_window, height=10, width=40)
        output_text.pack(padx=10, pady=10)
        output_text.insert(tk.END, output)
        output_text.config(state=tk.DISABLED)

    def add_book(self):
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()
        query = "INSERT INTO books (title, author) VALUES (?, ?)"
        execute_query(query, (title, author))
        messagebox.showinfo("Info", f"Book '{title}' by '{author}' added.")

    def update_book(self):
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()
        # Assuming there's a way to identify which book to update, such as book ID or selection from a list
        # This is a placeholder query, it should be adapted based on the actual schema and requirements
        query = "UPDATE books SET title = ?, author = ? WHERE id = ?"
        book_id = 1  # Replace with actual book ID
        execute_query(query, (title, author, book_id))
        messagebox.showinfo("Info", "Book updated.")

    def delete_book(self):
        title = self.book_title_entry.get()
        # Assuming there's a way to identify which book to delete, such as book ID or selection from a list
        # This is a placeholder query, it should be adapted based on the actual schema and requirements
        query = "DELETE FROM books WHERE title = ?"
        execute_query(query, (title,))
        messagebox.showinfo("Info", "Book deleted.")

    def add_user(self):
        user_name = self.user_name_entry.get()
        query = "INSERT INTO users (id) VALUES (?)"
        execute_query(query, (user_name,))
        messagebox.showinfo("Info", f"User '{user_name}' added.")

    def update_user(self):
        user_name = self.user_name_entry.get()
        # Assuming there's a way to identify which user to update, such as user ID or selection from a list
        # This is a placeholder query, it should be adapted based on the actual schema and requirements
        query = "UPDATE users SET id = ? WHERE id = ?"
        user_id = 1  # Replace with actual user ID
        execute_query(query, (user_name, user_id))
        messagebox.showinfo("Info", "User updated.")

    def delete_user(self):
        user_name = self.user_name_entry.get()
        # Assuming there's a way to identify which user to delete, such as user ID or selection from a list
        # This is a placeholder query, it should be adapted based on the actual schema and requirements
        query = "DELETE FROM users WHERE name = ?"
        execute_query(query, (user_name,))
        messagebox.showinfo("Info", "User deleted.")

    def get_recommendations(self):
        keywords = self.recommendation_keywords_entry.get()
        query = """SELECT url.url, pagerank.rank 
                FROM location 
                JOIN word ON location.wordid = word.rowid 
                JOIN url ON location.urlid = url.rowid 
                JOIN pagerank ON url.rowid = pagerank.urlid 
                WHERE word.word IN ({}) 
                ORDER BY pagerank.rank DESC""".format(','.join('?'*len(keywords.split())))
        recommendations = fetch_query(query, keywords.split())
        self.recommendations_list.delete(0, tk.END)
        for recommendation in recommendations:
            self.recommendations_list.insert(tk.END, f"{recommendation[0]} (Rank: {recommendation[1]})")

    def search_books(self):
        query = self.search_query_entry.get()
        sql_query = """SELECT url.url 
                    FROM location 
                    JOIN word ON location.wordid = word.rowid 
                    JOIN url ON location.urlid = url.rowid 
                    WHERE word.word IN ({})""".format(','.join('?'*len(query.split())))
        results = fetch_query(sql_query, query.split())
        self.search_results_list.delete(0, tk.END)
        for result in results:
            self.search_results_list.insert(tk.END, result[0])

    def generate_test_data(self):
        # Example test data generation function
        query = "INSERT INTO books (title, author) VALUES (?, ?)"
        test_data = [
            ("Book 1", "Author 1"),
            ("Book 2", "Author 2"),
            ("Book 3", "Author 3")
        ]
        for data in test_data:
            execute_query(query, data)
        messagebox.showinfo("Info", "Test data generated.")

if __name__ == "__main__":
    app = LibraryManagementSystem()
    app.mainloop()