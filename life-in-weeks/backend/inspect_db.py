import sqlite3
import sys

def print_table(table_name, connection):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        if not rows:
            print(f"\n{table_name} table is empty")
            return
            
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        print(f"\n{table_name} table:")
        print("-" * 80)
        print(" | ".join(columns))
        print("-" * 80)
        
        for row in rows:
            # Format each value as string and truncate long values
            formatted_row = []
            for value in row:
                if value is None:
                    formatted_value = "NULL"
                elif isinstance(value, str):
                    if len(value) > 50:
                        formatted_value = value[:47] + "..."
                    else:
                        formatted_value = value
                else:
                    formatted_value = str(value)
                formatted_row.append(formatted_value)
                
            print(" | ".join(formatted_row))
        
        print("-" * 80)
        print(f"Total rows: {len(rows)}")
        
    except sqlite3.OperationalError as e:
        print(f"Error accessing {table_name}: {str(e)}")

if __name__ == "__main__":
    db_path = "app.db"
    
    if not sys.platform.startswith('win'):
        db_path = "./" + db_path
    
    try:
        conn = sqlite3.connect(db_path)
        print(f"Connected to database: {db_path}")
        
        # Print users table
        print_table("users", conn)
        
        # Print events table
        print_table("events", conn)
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database connection error: {str(e)}")
        print("Make sure the database file exists in the backend directory")