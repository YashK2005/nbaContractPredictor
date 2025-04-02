from leaderboard_calculator import calculate_salary_differences
from salary_analysis import format_salary
import json
from datetime import datetime

def generate_leaderboard():
    """Generate leaderboard data and save it to a JSON file."""
    print("Generating leaderboard data...")
    overpaid, underpaid = calculate_salary_differences()
    
    data = {
        'generated_at': datetime.now().isoformat(),
        'overpaid': [
            {
                'name': player['name'],
                'actual_salary': player['actual_salary'],
                'predicted_salary': player['predicted_salary'],
                'difference': player['difference']
            } for player in overpaid
        ],
        'underpaid': [
            {
                'name': player['name'],
                'actual_salary': player['actual_salary'],
                'predicted_salary': player['predicted_salary'],
                'difference': player['difference']
            } for player in underpaid
        ]
    }
    
    with open('static/leaderboard_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("\nLeaderboard data generated successfully!")
    print("\nMost Overpaid Players:")
    print("-" * 50)
    for player in overpaid:
        print(f"{player['name']}: {format_salary(player['actual_salary'])} (Predicted: {format_salary(player['predicted_salary'])})")
    
    print("\nMost Underpaid Players:")
    print("-" * 50)
    for player in underpaid:
        print(f"{player['name']}: {format_salary(player['actual_salary'])} (Predicted: {format_salary(player['predicted_salary'])})")

if __name__ == "__main__":
    generate_leaderboard() 
