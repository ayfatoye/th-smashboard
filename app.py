from flask import Flask, request, jsonify
from models import db, Record, Leaderboard
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db.init_app(app)

@app.route('/update_leaderboard', methods=['POST'])
def update_leaderboard():
    data = request.get_json()
    player_one = data['player_one']
    player_two = data['player_two']
    winner = data['winner']

    winner_entry = Leaderboard.query.filter_by(name=winner).first()
    if winner_entry:
        winner_entry.wins = str(int(winner_entry.wins) + 1)
    else:
        winner_entry = Leaderboard(name=winner, wins='1', losses='0')
        db.session.add(winner_entry)

    loser = player_one if winner == player_two else player_two
    loser_entry = Leaderboard.query.filter_by(name=loser).first()
    if loser_entry:
        loser_entry.losses = str(int(loser_entry.losses) + 1)
    else:
        loser_entry = Leaderboard(name=loser, wins='0', losses='1')
        db.session.add(loser_entry)

    record_entry_winner = Record(vs=loser, player=winner, won='true')
    record_entry_loser = Record(vs=winner, player=loser, won='false')
    db.session.add(record_entry_winner)
    db.session.add(record_entry_loser)

    db.session.commit()

    return jsonify({'message': 'Leaderboard updated successfully'})

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    leaderboard_entries = Leaderboard.query.all()

    leaderboard_data = []

    for entry in leaderboard_entries:
        player_data = {
            'name': entry.name,
            'wins': entry.wins,
            'losses': entry.losses
        }
        leaderboard_data.append(player_data)

    return jsonify(leaderboard_data)

if __name__ == '__main__':
    app.run(debug=True)


# if __name__ == '__main__':
#     # Create tables
#     with app.app_context():
#         db.create_all()
#         # add_test_table_entry('Hello, this is a test message!')\
#         app.run(debug=True)