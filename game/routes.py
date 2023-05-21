from flask import render_template, Flask, jsonify, request
from game import app
from game_logic import initialize_game_state, describe_situation, handle_action

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/start', methods=['GET'])
def start_game():
    game_state = initialize_game_state()
    situation = describe_situation(game_state)
    return jsonify({'game_state': game_state, 'situation': situation})

@app.route('/action', methods=['POST'])
def handle_action_route():
    game_state = request.json['game_state']
    action = request.json['action']
    game_state = handle_action(game_state, action)
    situation = describe_situation(game_state)
    return jsonify({'game_state': game_state, 'situation': situation})