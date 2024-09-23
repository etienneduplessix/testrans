var canvas;
var ctx;
var docHeight;
var docWidth;
var gameon = false;

class Obj {
    constructor(ctx, x, y, fullsize = false) {
        this.ctx = ctx;
        this.x = x;
        this.y = y;
        this.color = "lightgreen";
        this.ballSize = docHeight / 20;
        this.paddleWidth = docWidth / 25;
        this.paddleHeight = docHeight / 5;
    }

    moveBall(x, y) {
        this.ctx.clearRect(this.x - this.ballSize, this.y - this.ballSize, this.ballSize * 2 + 0.5, this.ballSize * 2 + 0.5);
        this.x = x;
        this.y = y;
        this.drawBall();
    }

    drawBall() {
        this.ctx.fillStyle = this.color;
        this.ctx.beginPath();
        this.ctx.arc(this.x, this.y, this.ballSize, 0, Math.PI * 2, false);
        this.ctx.fill();
        this.ctx.closePath();
    }

    drawPaddle(y) {
        this.ctx.clearRect(this.x - 0.5, this.y - 0.5, this.paddleWidth + 1, this.paddleHeight + 1);
        this.y = y;
        this.ctx.fillStyle = this.color;
        this.ctx.fillRect(this.x, this.y, this.paddleWidth, this.paddleHeight);
    }
}

var paddle_left;
var paddle_right;
var ball;
var game_page = false;

function setupgame(pageName) {

    let page = page_game();
    console.log(page); 
    pageName = "game"   
    if (pageName == "game")
        game_page = true;
    console.log(game_page);
    canvas = document.querySelector("canvas");
    if (!canvas) {
        console.error('Failed to get canvas');
        return;
    }
    ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error('Failed to get canvas context');
        return;
    }
    docHeight = canvas.clientHeight;
    docWidth = canvas.clientWidth;

    canvas.height = docHeight;
    canvas.width = docWidth;

    // Adjust x-coordinates for paddles closer to the walls
    paddle_left = new Obj(ctx, 10, docHeight / 2 - docHeight / 10);
    paddle_right = new Obj(ctx, docWidth - 20, docHeight / 2 - docHeight / 10);
    ball = new Obj(ctx, docWidth / 2, docHeight / 2);

    reset_screen();
}

function get_rat() {
    return 1000 / docWidth;
}

function reset_screen() {
    ctx.clearRect(0, 0, docWidth, docHeight);
    paddle_left.y = paddle_right.y = ball.y = docHeight / 2 - docHeight / 10;
    ball.x = docWidth / 2;
    paddle_left.drawPaddle(paddle_left.y);
    paddle_right.drawPaddle(paddle_right.y);
    ball.drawBall();
}

async function gameLoop() {
    if (gameon) {
        
        await updateGameState();
        requestAnimationFrame(gameLoop);
    }
}

async function updateGameState() {
    const csrfToken = getCookie('csrftoken');
    try {
    let response = await fetch('/game_api/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        });

        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        let state = await response.json();
        var rat = get_rat();
        ball.moveBall(state.ball_position[0] / rat, state.ball_position[1] / rat);
        paddle_left.drawPaddle(state.paddle1_position / rat);
        paddle_right.drawPaddle(state.paddle2_position / rat);

    } catch (error) {
        console.error('Error updating game state:', error);
    }
}

function movePaddle(paddle, direction) {
    const csrfToken = getCookie('csrftoken');
    fetch('/game_api/move/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ paddle, direction }),
    })
    .then(response => response.json())
    .then(data => console.log('Paddle moved:', data))
    .catch(error => console.error('Error moving paddle:', error));
}

function pre_start(){
    let date = Date.now();
    console.log(date);
    console.log ("sending start game message");
    web_socket.send(
        JSON.stringify({
            'type': 'send_game_start',
            'message': "starting game!"
        }
    ));
} 

function startGame() {
    const csrfToken = getCookie('csrftoken');
    fetch('/game_api/start/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
    .then(data => {
        gameon = true;
        console.log('Game started:', data);
        gameLoop();

        
    })
    .catch(error => console.error('Error starting game:', error));
}

document.addEventListener('keydown', (event) => {
    const paddle_speed = 20; // Adjust as necessary
    if (game_page == true) {
    switch (event.key) {
        case 'w':
            movePaddle(1, -paddle_speed);
            break;
        case 's':
            movePaddle(1, paddle_speed);
            break;
        case 'ArrowUp':
            movePaddle(2, -paddle_speed);
            break;
        case 'ArrowDown':
            movePaddle(2, paddle_speed);
            break;
        case ' ':
            pre_start();
            break;
    }}
});
