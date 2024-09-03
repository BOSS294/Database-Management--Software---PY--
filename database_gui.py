import customtkinter as ctk
import time
from db_connector import DatabaseConnector

class DatabaseViewer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Database Viewer")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(pady=20, padx=20, sticky="nsew")

        # Title
        self.title_label = ctk.CTkLabel(self.frame, text="Database Connection", font=("Arial", 24))
        self.title_label.grid(row=0, column=0, columnspan=4, pady=20)

        # Input fields (side by side)
        self.host_input = ctk.CTkEntry(self.frame, placeholder_text="Host", width=150)
        self.host_input.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.user_input = ctk.CTkEntry(self.frame, placeholder_text="Username", width=150)
        self.user_input.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.password_input = ctk.CTkEntry(self.frame, placeholder_text="Password", show="*", width=150)
        self.password_input.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        self.database_input = ctk.CTkEntry(self.frame, placeholder_text="Database Name", width=150)
        self.database_input.grid(row=1, column=3, padx=10, pady=10, sticky="ew")

        # Connect button
        self.connect_button = ctk.CTkButton(self.frame, text="Connect", command=self.connect_to_database, width=150)
        self.connect_button.grid(row=2, column=0, columnspan=1, padx=10, pady=20)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.frame)
        self.progress_bar.grid(row=2, column=2, columnspan=2, padx=10, pady=20, sticky="ew")
        self.progress_bar.set(0)

        # Output field
        self.output_label = ctk.CTkLabel(self.frame, text="", font=("Arial", 14), wraplength=400, justify="left")
        self.output_label.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        # Table selection
        self.tables_combo = ctk.CTkComboBox(self.frame, values=["No tables available"], state="readonly", width=300)
        self.tables_combo.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.tables_combo.bind("<<ComboboxSelected>>", self.load_columns)

        # Data table area
        self.table_frame = ctk.CTkFrame(self.frame)
        self.table_frame.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Error and reset buttons
        self.error_button = ctk.CTkButton(self.frame, text="Show Error", command=self.show_error, width=150, fg_color="red")
        self.reset_button = ctk.CTkButton(self.frame, text="Reset", command=self.reset_fields, width=150)

        self.error_button.grid_remove()  # Hide error button initially
        self.reset_button.grid_remove()  # Hide reset button initially

        # Configuring grid for dynamic resizing
        self.frame.grid_rowconfigure(5, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)

        self.db = DatabaseConnector()
        self.error_message = ""

    def connect_to_database(self):
        self.progress_bar.set(0.2)
        self.after(500, self.complete_connection)

    def complete_connection(self):
        try:
            connected = self.db.connect(
                self.host_input.get(),
                self.user_input.get(),
                self.password_input.get(),
                self.database_input.get()
            )
            if connected:
                self.progress_bar.set(1.0)
                self.title_label.configure(text="Connection Successful", fg_color="green")
                self.load_tables()
                self.output_label.configure(text="Connected to the database successfully.", text_color="green")
                self.animate_message(self.output_label)
                self.error_button.grid_remove()  # Hide error button on successful connection
            else:
                raise Exception("Failed to connect to the database.")
        except Exception as e:
            self.progress_bar.set(0)
            self.title_label.configure(text="Connection Failed", fg_color="red")
            self.output_label.configure(text="Connection failed. Please check your credentials.", text_color="red")
            self.animate_message(self.output_label)
            self.error_message = str(e)
            self.error_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
            self.reset_button.grid(row=6, column=2, columnspan=2, padx=10, pady=10, sticky="ew")

    def load_tables(self):
        tables = self.db.get_tables()
        if tables:
            self.tables_combo.configure(values=[table[0] for table in tables])
            self.tables_combo.set(tables[0][0])  # Select the first table by default
            self.load_columns()
            self.output_label.configure(text="")
        else:
            self.tables_combo.configure(values=["No tables available"])
            self.tables_combo.set("No tables available")
            self.output_label.configure(text="No tables found in the database.")
            self.clear_table()

    def load_columns(self, event=None):
        table_name = self.tables_combo.get()
        if table_name == "No tables available":
            return
        
        columns = self.db.get_columns(table_name)
        
        self.clear_table()

        if columns:
            for col, column_name in enumerate(columns):
                header = ctk.CTkLabel(self.table_frame, text=column_name[0])
                header.grid(row=0, column=col, padx=5, pady=5)

            self.load_data(table_name)

    def load_data(self, table_name):
        cursor = self.db.connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        if rows:
            self.output_label.configure(text="Data from table: " + table_name, text_color="blue")
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    cell = ctk.CTkLabel(self.table_frame, text=str(value))
                    cell.grid(row=i + 1, column=j, padx=5, pady=5)
        else:
            self.output_label.configure(text="No data available in the selected table.", text_color="orange")

    def clear_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

    def show_error(self):
        self.output_label.configure(text=self.error_message, text_color="red")
        self.animate_message(self.output_label)

    def reset_fields(self):
        self.host_input.delete(0, "end")
        self.user_input.delete(0, "end")
        self.password_input.delete(0, "end")
        self.database_input.delete(0, "end")
        self.output_label.configure(text="")
        self.title_label.configure(text="Database Connection", fg_color=None)
        self.progress_bar.set(0)
        self.error_button.grid_remove()
        self.reset_button.grid_remove()
        self.tables_combo.configure(values=["No tables available"])
        self.clear_table()

    def animate_message(self, label):
        initial_color = label.cget("text_color")
        fade_steps = 10
        for i in range(fade_steps):
            alpha = i / fade_steps
            new_color = self.fade_color(initial_color, alpha)
            label.configure(text_color=new_color)
            self.update_idletasks()
            time.sleep(0.05)
        label.configure(text_color=initial_color)

    def fade_color(self, color, alpha):
        if isinstance(color, str):
            # Convert named color to RGB tuple
            color = self.winfo_rgb(color)
            color = tuple([x // 256 for x in color])
        
        # Calculate faded color
        faded_color = tuple(int(c * alpha) for c in color)
        return f"#{faded_color[0]:02x}{faded_color[1]:02x}{faded_color[2]:02x}"

if __name__ == "__main__":
    app = DatabaseViewer()
    app.mainloop()
