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
        messages=[
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

    # Extract the AI's response from the chat completion.
    ai_response = response['choices'][0]['message']['content']

    # List of phrases that might indicate a successful move.
    success_phrases = [
        "I will set the course for",
        "we begin our journey",
        "heading to",
        "you successfully moved to",
        "Initiating travel to",
        "Initiating jump to",
        "Initiating warp to",
        "Initiating hyperspace jump to",
        "Initiating hyperspace travel to",
        "Initiating hyperspace warp to",
        "Warping to",
        "Jumping to",
        "Hyperspace jumping to",
        "Hyperspace traveling to",
        "Hyperspace warping to",
        "Traveling to",
        "Moving to"
        # Add more phrases as needed.
    ]

    # List of phrases that might indicate the move is not possible.
    failure_phrases = [
        "I cannot perform such actions",
        "we need to consider several factors",
        "we must make sure that"
        # Add more phrases as needed.
    ]

    # Check if any of the failure phrases are in the AI's response.
    for phrase in failure_phrases:
        if phrase in ai_response:
            # If a failure phrase is found, do not update the location and return immediately.
            return game_state, ai_response

    # Check if any of the success phrases are in the AI's response.
    for phrase in success_phrases:
        if phrase in ai_response:
            new_location = ai_response.split(phrase)[1].split(".")[0].strip()
            game_state['location'] = new_location
            break

    # TODO: Update the game state based on the action and the AI's response.
    # This might involve parsing the AI's response to understand what happened,
    # and updating the game state accordingly.

    # For example, if the AI says that you successfully moved to a new location,
    # you could update the location in the game state.

    return game_state, ai_response