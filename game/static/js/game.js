window.onload = startGame;

function startGame() {
    fetch('/start')
        .then(response => response.json())
        .then(data => {
            document.getElementById('situation').textContent = data.situation;
        });
}

document.getElementById('submit').onclick = submitAction;

function submitAction() {
    const action = document.getElementById('action').value;
    fetch('/action', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: action })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('situation').textContent = data.situation;
        });
}
