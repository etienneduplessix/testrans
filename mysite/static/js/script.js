/*
// TODO
	- midline across the board would be cool. css?
	- add user dialogue for username
	- add user scores
*/
var canvas = document.querySelector("canvas");
var ctx = canvas.getContext('2d');
var docHeight = window.innerHeight;
var docWidth = window.innerWidth;
var requestFrame = false;
canvas.height = docHeight;
canvas.width = docWidth;

var leftPad_up, leftPad_down, rightPad_up, rightPad_down = false;

var ball_speed = 7;
var paddle_speed = 10;

class Obj
{
	constructor (ctx, x, y, fullsize = false)
	{
		this.ctx = ctx;
		this.x = x;
		this.y = y;
		this.color = "lightgreen";
		this.ballSize = 15;
		this.Xdir = false;
		this.Ydir = false;
		this.paddleWidth = 25;
		this.paddleHeight = (fullsize ? docHeight : 100);
		this.ctx.fillStyle = this.color;
	}

	moveBall ()
	{
		this.ctx.clearRect(this.x - (this.ballSize),
				this.y - (this.ballSize), this.ballSize * 2 + .5, this.ballSize * 2 + .5);

		if (this.Xdir) this.x += ball_speed;
		if (!this.Xdir) this.x -= ball_speed;
		if (this.Ydir) this.y += ball_speed;
		if (!this.Ydir) this.y -= ball_speed;

		this.drawBall();

	}

	drawBall (xchange = 0, ychange = 0)
	{
		this.x += xchange;
		this.y += ychange;


		this.ctx.fillStyle = this.color;
		this.ctx.beginPath();
		this.ctx.arc(this.x, this.y, this.ballSize, 0, Math.PI * 2, false);
		this.ctx.fill();
		this.ctx.closePath();

/// added stuff

		this.ctx.fillStyle = "red";
		this.ctx.beginPath();
		this.ctx.arc(this.x, this.y, 5, 0, Math.PI * 2, false);
		this.ctx.fill();
		this.ctx.closePath();


		var yu = ball.y - ball.ballSize;
		var yd = ball.y + ball.ballSize;
		var xl = ball.x - ball.ballSize;
		var xr = ball.x + ball.ballSize;

		this.ctx.beginPath();
		this.ctx.arc(this.x, yu, 2, 0, Math.PI * 2, false);
		this.ctx.fill();
		this.ctx.closePath();
		this.ctx.beginPath();
		this.ctx.arc(this.x, yd, 2, 0, Math.PI * 2, false);
		this.ctx.fill();
		this.ctx.closePath();
		this.ctx.beginPath();
		this.ctx.arc(xl, this.y, 2, 0, Math.PI * 2, false);
		this.ctx.fill();
		this.ctx.closePath();
		this.ctx.beginPath();
		this.ctx.arc(xr, this.y, 2, 0, Math.PI * 2, false);
		this.ctx.fill();
		this.ctx.closePath();

	}

	drawPaddle (ychange = 0)
	{
		// this.ctx.clearRect(this.x - this.ballSize, this.y - this.ballSize,
		// 	this.paddleWidth + 2 * this.ballSize, this.paddleHeight + 2 * this.ballSize);

		if (ychange)
			this.ctx.clearRect(this.x -.5 , this.y -.5, this.paddleWidth + 1, this.paddleHeight + 1);
		if (this.y + ychange <= 0)
			ychange = this.y * -1;
		if (this.y + ychange + this.paddleHeight >= docHeight)
			ychange = docHeight - this.paddleHeight - this.y;

		this.y += ychange;
/* 		this.ctx.fillStyle = "red";
		this.ctx.fillRect(this.x - this.ballSize, this.y - this.ballSize,
			 this.paddleWidth + 2 * this.ballSize, this.paddleHeight + 2 * this.ballSize);
 */
		this.ctx.fillStyle = this.color;
		this.ctx.fillRect(this.x, this.y, this.paddleWidth, this.paddleHeight);
	}
}



// var paddle_left = new Obj (ctx, 50, 0, true); //to make wall
var paddle_left = new Obj (ctx, 50, docHeight / 2);
var paddle_right = new Obj (ctx, docWidth - 50 - paddle_left.paddleWidth, 0, true); //to make wall
// var paddle_right = new Obj (ctx, docWidth - 50 - paddle_left.paddleWidth, docHeight / 2);
var ball = new Obj (ctx, docWidth / 2,docHeight / 2);

paddle_left.drawPaddle();
paddle_right.drawPaddle();

ball.drawBall();



////FUNCTIONS
	function getRandomInt(min, max) {
		min = Math.ceil(min);
		max = Math.floor(max);
		return Math.floor(Math.random() * (max - min + 1)) + min;
	}

	function MoveBallLoop(ball) {
		checkCollision();
		ball.moveBall();

		if (rightPad_up) paddle_right.drawPaddle(-paddle_speed);
		if (rightPad_down) paddle_right.drawPaddle(paddle_speed);
		if (leftPad_up) paddle_left.drawPaddle(-paddle_speed);
		if (leftPad_down) paddle_left.drawPaddle(paddle_speed);

		paddle_left.drawPaddle();
		paddle_right.drawPaddle();
		if (requestFrame)
			requestAnimationFrame(() => { MoveBallLoop(ball) });
	}

	function checkCollision()
	{
		if (ball.y - ball.ballSize <= 0)
			ball.Ydir = true;
		if (ball.y + ball.ballSize >= docHeight)
			ball.Ydir = false;

			var yu = ball.y - ball.ballSize;
			var yd = ball.y + ball.ballSize;
			var xl = ball.x - ball.ballSize;
			var xr = ball.x + ball.ballSize;

		if (((yu >= paddle_right.y && yu <= paddle_right.y + paddle_right.paddleHeight)
			|| (yd >= paddle_right.y && yd <= paddle_right.y + paddle_right.paddleHeight))
		&& (xr >= paddle_right.x))
			{
				// console.log ("ballx " + ball.x + "; ball.width " + ball.ballSize + "; paddle x " + paddle_right.x + "; paddle w " + paddle_right.paddleWidth);
				if (ball.y > paddle_right.y + paddle_right.paddleHeight)
				{
					// console.log ("y switch");
					ball.Ydir = true;
				}
				else if (ball.y < paddle_right.y)
				{
					// console.log ("y switch");
					ball.Ydir = false;
				}

				else //if the ball is touching the paddle face
				{
					// console.log ("x => false");
					ball.Xdir = false;
				}
			}
		if (((yu >= paddle_left.y && yu <= paddle_left.y + paddle_left.paddleHeight)
			|| (yd >= paddle_left.y && yd <= paddle_left.y + paddle_left.paddleHeight))
			&& (xl <= paddle_left.x + paddle_left.paddleWidth))
			{
				// console.log ("ballx " + ball.x + "; ball.width " + ball.ballSize + "; paddle x " + paddle_left.x + "; paddle w " + paddle_left.paddleWidth);
				if (ball.y > paddle_left.y + paddle_left.paddleHeight)
				{
					// console.log ("y switch");
					ball.Ydir = true;
				}
				else if (ball.y < paddle_left.y)
				{
					// console.log ("y switch");
					ball.Ydir = false;
				}

				else //if the ball ids touching the paddle face
				{
					// console.log ("x => truue");
					ball.Xdir = true;
				}
			}

		//hitting left wall
		if (ball.x - ball.ballSize <= 0)
		{
			requestFrame = false;
			alert ("left player lost :(");
		}
		if (ball.x + ball.ballSize >= docWidth)
		{
			requestFrame = false;
			alert ("right player lost :(");
		}
	}

	function reset_screen()
	{
		ctx.clearRect(0, 0, docWidth, docHeight);
		paddle_left.y = paddle_right.y = ball.y = docHeight / 2;
		ball.x = docWidth / 2;
		leftPad_up = false;
		leftPad_down = false;
		rightPad_up = false;
		rightPad_down = false;
		var dir = getRandomInt(1, 4);
		switch (dir) {
			case 1:
				ball.Xdir = true;
				ball.Ydir = true;
				break;
			case 2:
				ball.Xdir = true;
				ball.Ydir = false;
				break;
			case 3:
				ball.Xdir = false;
				ball.Ydir = true;
				break;
			case 4:
				ball.Xdir = false;
				ball.Ydir = false;
				break;
		}

		paddle_left.drawPaddle();
		paddle_right.drawPaddle();
		ball.drawBall();



		requestFrame = true;
		MoveBallLoop(ball);
	}

	addEventListener("keydown", (KeyboardEvent) =>
	{

		if (KeyboardEvent.key == "ArrowUp")
			rightPad_up = true;
		if (KeyboardEvent.key == "ArrowDown")
			rightPad_down = true;

		if (KeyboardEvent.key == "w")
			leftPad_up = true;
		if (KeyboardEvent.key == "s")
			leftPad_down = true;

		if (KeyboardEvent.key == " ")
		{
			if (requestFrame == false)
				reset_screen();
		}
	});

	addEventListener("keyup", (KeyboardEvent) =>
	{
		if (KeyboardEvent.key == "ArrowUp")
			rightPad_up = false;
		if (KeyboardEvent.key == "ArrowDown")
			rightPad_down = false;

		if (KeyboardEvent.key == "w")
			leftPad_up = false;
		if (KeyboardEvent.key == "s")
			leftPad_down = false;
	});

	/////////////

  loginButton1.addEventListener('click', () => {
    window.location.href = "/api/";
});

loginButton2.addEventListener('click', () => {
    window.location.href = "/api/";
});

