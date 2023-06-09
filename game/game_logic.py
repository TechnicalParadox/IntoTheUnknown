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
        "chat_history": [],
        "id_generator": 0 # Will be incremented as each object is created. For example, the player will become a Captain(CrewMember) with id 0, the ship will become a Ship with id 1, the first discovered location will become a POI with id 2, a new crew member will become a CrewMember with id 3. An easy way to ensure IDs are unique in a player's instance of the game.
    }


def describe_situation(game_state):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.5,
        messages=
        [
            {
                "role": "system",
                "content": f"You are the main ship AI. The spaceship is currently at {game_state['location']}. Your spaceship is in {game_state['ship_condition']} condition. Your resources: {', '.join(game_state['resources']) if game_state['resources'] else 'none'}."
            },
            {
                "role": "user",
                "content": "AI, provide a status report of the ship and its current location."
            }
        ]
        # TODO: revise prompt to get more detailed responses from the AI.
    )
    
    game_state['ai_response_prev'] = response['choices'][0]['message']['content']
    
    # Keep 5 previous AI responses/5 previous user inputs in chat_history array.
    game_state['chat_history'].append(response['choices'][0]['message']['content'])

    return response['choices'][0]['message']['content']

def handle_action(game_state, action):
    # TODO: revise prompt to get more detailed responses from the AI.
    chat_history = game_state['chat_history'][-5:]
    chat_history_formatted = ' '.join(chat_history)

    m = [
        {
            "role": "system",
            "content": f"You are the main ship AI. The spaceship is currently at {game_state['location']}. Your spaceship is in {game_state['ship_condition']} condition. Your resources: {', '.join(game_state['resources']) if game_state['resources'] else 'none'}. Recent chat history: {chat_history_formatted}"
        },
        {
            "role": "user",
            "content": f"AI, {action}."
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=1,
        messages=m
    )

    print(m)

    # Extract the AI's response from the chat completion.
    ai_response = response['choices'][0]['message']['content']

    # Keep 5 previous AI responses/5 previous user inputs in chat_history array.
    game_state['chat_history'].append('USER INPUT: '+action)
    game_state['chat_history'].append('SHIP AI: '+ai_response)
    if len(game_state['chat_history']) > 10:
        game_state['chat_history'] = game_state['chat_history'][-6:]
    history = ''
    for i in range(len(game_state['chat_history'])):
        history += game_state['chat_history'][i] + '\n'
    print ('\nGAME STATE CHAT HISTORY\n' + history + '\n')

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

    game_state['ai_response_prev'] = ai_response

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