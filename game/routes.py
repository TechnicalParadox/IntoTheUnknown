from flask import jsonify, request, render_template, Flask
from .game_logic import initialize_game_state, describe_situation, handle_action  # replace 'your_game_logic_file' with the actual name of your Python file
from . import app  # replace 'your_main_file' with the actual name of your main Python file

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/start', methods=['GET'])
def start_game():
    game_state = initialize_game_state()
    situation = describe_situation(game_state)
    return jsonfy({'game_state': game_state, 'situation': situation})

@app.route('/action', methods=['POST'])
def perform_action():
    game_state = request.json['game_state']
    action = request.json['action']
    game_state = handle_action(game_state, action)
    situation = describe_situation(game_state)
    return jsonify({'game_state': game_state, 'situation': situation})
