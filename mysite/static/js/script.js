
document.addEventListener('DOMContentLoaded', () => {
      const ball = document.querySelector('.ball');
      const paddle1 = document.getElementById('paddle1');
      const paddle2 = document.getElementById('paddle2');
      const gameArea = document.querySelector('.game-area');
      const startButton = document.getElementById('startButton');
    
      let ballX = 290;
      let ballY = 190;
      let ballSpeedX = 0;
      let ballSpeedY = 0;
    
      let paddle1Y = 160;
      let paddle2Y = 160;
      const paddleSpeed = 20;
    
      const update = () => {
        // Update ball position
        ballX += ballSpeedX;
        ballY += ballSpeedY;
    
        // Check collision with top and bottom walls
        if (ballY <= 0 || ballY >= 380) {
          ballSpeedY = -ballSpeedY;
        }
    
        // Check collision with paddles
        checkPaddleCollision();
    
        // Update ball position
        ball.style.left = ballX + 'px';
        ball.style.top = ballY + 'px';
    
        // Update paddle positions (for demo purposes)
        paddle1.style.top = paddle1Y + 'px';
        paddle2.style.top = paddle2Y + 'px';
    
        requestAnimationFrame(update);
      };
    
      const checkPaddleCollision = () => {
        if (ballX <= 20) {
          if (isCollision(paddle1Y, ballY, 80)) {
            ballSpeedX = -ballSpeedX;
          } else {
            // Player 2 scores
            resetBall();
          }
        } else if (ballX >= 560) {
          if (isCollision(paddle2Y, ballY, 80)) {
            ballSpeedX = -ballSpeedX;
          } else {
            // Player 1 scores
            resetBall();
          }
        }
      };
    
      const isCollision = (paddleY, ballY, paddleHeight) => {
        return ballY >= paddleY && ballY <= paddleY + paddleHeight;
      };
    
      const resetBall = () => {
        ballX = 290;
        ballY = 190;
        ballSpeedX = 0;
        ballSpeedY = 0;
      };
    
      const startBall = () => {
        ballSpeedX = 1;
        ballSpeedY = 2 ;
        update();
      };
    
      startButton.addEventListener('click', startBall);
    
      // Keyboard controls for paddles (for demo purposes)
      document.addEventListener('keydown', (event) => {
        if (event.key === 'w' && paddle1Y > 0) {
          paddle1Y -= paddleSpeed;
        }
        if (event.key === 's' && paddle1Y < 320) {
          paddle1Y += paddleSpeed;
        }
        if (event.key === 'ArrowUp' && paddle2Y > 0) {
          paddle2Y -= paddleSpeed;
        }
        if (event.key === 'ArrowDown' && paddle2Y < 320) {
          paddle2Y += paddleSpeed;
        }
      });
    });
    
   update();
 