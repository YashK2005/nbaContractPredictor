import sqlite3
from database_setup import create_connection, database
from predicting_salary import predictor

def calculate_salary_differences():
    """Calculate salary differences for all players and return sorted lists of overpaid and underpaid players."""
    conn = create_connection(database)
    cur = conn.cursor()
    
    # Get all players
    cur.execute('SELECT first_name, last_name, salary FROM combined_table')
    players = cur.fetchall()
    
    # Calculate differences for each player
    player_differences = []
    for player in players:
        first_name, last_name, actual_salary = player
        full_name = f"{first_name} {last_name}"
        
        try:
            predicted_salary, _, _ = predictor(full_name)
            difference = actual_salary - predicted_salary
            player_differences.append({
                'name': full_name,
                'actual_salary': actual_salary,
                'predicted_salary': predicted_salary,
                'difference': difference
            })
        except Exception as e:
            print(f"Error processing {full_name}: {str(e)}")
            continue
    
    # Sort players by difference
    overpaid = sorted(player_differences, key=lambda x: x['difference'], reverse=True)[:20]
    underpaid = sorted(player_differences, key=lambda x: x['difference'])[:20]
    
    return overpaid, underpaid 
