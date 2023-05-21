let gameState = null;  // add this line

window.onload = startGame;

function startGame() {
    document.getElementById('loading').style.display = 'block';
    fetch('/start')
        .then(response => response.json())
        .then(data => {
            document.getElementById('situation').textContent = data.situation;
            gameState = data.game_state;
            document.getElementById('loading').style.display = 'none';
        });
}

document.getElementById('submit').onclick = submitAction;

function submitAction() {
    const action = document.getElementById('action').value;

    document.getElementById('loading').style.display = 'block';
    fetch('/action', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ game_state: gameState, action: action })  // modify this line
    })
        .then(response => {
            if (!response.ok) {
                console.error("Error status:", response.status);
                return;
            }
            return response.json();
        })
        .then(data => {
            if (data) {
                document.getElementById('situation').textContent = data.situation;
                gameState = data.game_state;  // add this line
            }
            document.getElementById('loading').style.display = 'none';
        })
        .catch(error => console.error("Error:", error));
}
