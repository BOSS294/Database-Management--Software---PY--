# TableSavvy

**TableSavvy** is a user-friendly Python application designed for easy management and visualization of database tables. Built with PyQt5 and MySQL, TableSavvy provides an intuitive graphical interface to connect to MySQL databases, view tables, and manage data seamlessly. This tool is ideal for database administrators, developers, and anyone who needs an efficient way to interact with their database tables.

## Features

- **Easy Database Connection**: Connect to MySQL databases with a straightforward interface. Just enter your host, username, password, and database name.
- **Table Management**: View and select tables from the connected database.
- **Data Visualization**: Load and display table data in a clean and organized table view.
- **Column Information**: See column names and structure for selected tables.
- **Progress Feedback**: Visual feedback of connection status through a progress bar.
- **Error Handling**: Alerts on connection failures with error messages.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/TableSavvy.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd TableSavvy
   ```

3. **Install Dependencies**

   Ensure you have Python installed, then install the required packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` file should include:

   ```
   PyQt5
   mysql-connector-python
   ```

## Usage

1. **Run the Application**

   ```bash
   python main.py
   ```

2. **Connect to a Database**

   - Enter the host, username, password, and database name in the respective fields.
   - Click on the "Connect" button to establish the connection.

3. **Manage Tables**

   - Once connected, select a table from the dropdown menu to view its columns and data.

## Code Overview

### `main.py`

The main application file uses PyQt5 to create a graphical interface for interacting with MySQL databases.

- **DatabaseViewer**: Main widget class handling the UI and database operations.
- **connect_to_database()**: Initiates the connection process and updates UI based on connection status.
- **load_tables()**: Fetches and displays database tables.
- **load_columns()**: Retrieves and shows columns of the selected table.
- **load_data()**: Loads and displays data from the selected table.

### `db_connector.py`

Handles MySQL database connections and queries.

- **connect(host, user, password, database)**: Connects to the MySQL database.
- **get_tables()**: Retrieves all tables from the database.
- **get_columns(table_name)**: Retrieves column information for a specified table.
- **disconnect()**: Closes the database connection.

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.


## Contact

For any issues or suggestions, please open an issue on the GitHub repository or contact [mayankchawdhari@gmail.com](mailto:mayankchawdhari@gmail.com).
