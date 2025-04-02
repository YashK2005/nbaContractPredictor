import json
import os

def get_salary_differences():
    """Get salary differences from the static JSON file."""
    try:
        with open('static/leaderboard_data.json', 'r') as f:
            data = json.load(f)
            return data['overpaid'], data['underpaid']
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading leaderboard data: {str(e)}")
        return [], []

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
