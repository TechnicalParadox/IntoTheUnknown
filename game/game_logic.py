from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def initialize_game_state():
    return {
        "location": "Earth",
        "ship_condition": "Good",
        "resources": [],
    }

def game_loop():
    game_state = initialize_game_state()

    while True:
        situation = describe_situation(game_state)
        print(situation)

        # TODO: Use GPT-3.5-turbo to generate a description of the current situation.

        action = input("What do you want to do? ")
        game_state = handle_action(game_state, action)

        if check_game_end(game_state):
            print("You've reached the end of your journey...")
            break

def check_game_end(game_state):
    return game_state["location"] == "edge of the galaxy" and game_state["ship_condition"] == "Good" and game_state["resources"]

def describe_situation(game_state):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=
        [
            {
                "role": "system",
                "content": f"You are piloting a spaceship through the galaxy. You are currently at {game_state['location']}. Your spaceship is in {game_state['ship_condition']} condition. Your resources: {', '.join(game_state['resources']) if game_state['resources'] else 'none'}."
            },
            {
                "role": "user",
                "content": "Describe my situation."
            }
        ]
    )
    
    return response['choices'][0]['message']['content']

def handle_action(game_state, action):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=
        [
            {
                "role": "system",
                "content": f"You are piloting a spaceship through the galaxy. You are currently at {game_state['location']}. Your spaceship is in {game_state['ship_condition']} condition. Your resources: {', '.join(game_state['resources']) if game_state['resources'] else 'none'}."
            },
            {
                "role": "user",
                "content": action
            }
        ]
    )

    if action.startswith("move to "):
        new_location = action[len("move to "):]
        game_state['location'] = new_location

    # TODO: Update the game state based on the action.
    return game_state