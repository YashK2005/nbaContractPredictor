import json
import os
from leaderboard_calculator import calculate_salary_differences

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_salary_differences():
    """Get salary differences from bundled data, with a database fallback."""
    data_path = os.path.join(BASE_DIR, 'data', 'leaderboard_data.json')
    try:
        with open(data_path, 'r') as f:
            data = json.load(f)
            return data['overpaid'], data['underpaid']
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading leaderboard data: {str(e)}")
        return calculate_salary_differences()

def format_salary(salary):
    """Format salary with commas and dollar sign."""
    return f"${salary:,.0f}"

if __name__ == "__main__":
    overpaid, underpaid = get_salary_differences()
    
    print("\nMost Overpaid Players:")
    print("-" * 50)
    for player in overpaid:
        print(f"{player['name']}: {format_salary(player['actual_salary'])} (Predicted: {format_salary(player['predicted_salary'])})")
    
    print("\nMost Underpaid Players:")
    print("-" * 50)
    for player in underpaid:
        print(f"{player['name']}: {format_salary(player['actual_salary'])} (Predicted: {format_salary(player['predicted_salary'])})") 
