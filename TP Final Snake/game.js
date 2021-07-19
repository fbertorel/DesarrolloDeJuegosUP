var snake, apple, blockSize, intervalVar, score, speed, updateDelay, direction, 
newdirection, appleEaten, keys, scoreText, speedText, 
width, heigth, randomtimeGap;

var Game = {
    
    preload : function() {
        game.load.image('snake', 'assets/img/snake.png');
        game.load.image('apple', 'assets/img/apple.png');
    },

    randomIntervalApple : function(){
        intervalVar = setInterval(function(){
            apple.destroy();                                               
            let randomX = Math.floor(Math.random() * 40 ) * blockSize,
            randomY = Math.floor(Math.random() * 30 ) * blockSize;
            apple = game.add.sprite(randomX, randomY, 'apple');
        },randomtimeGap);
    },

    create : function() {
        snake = [];
        apple = {};
        blockSize = 16;
        score = 0;
        speed = 0;
        updateDelay = 0;
        direction = 'right';
        newdirection = null;
        appleEaten = false;
        width = 640;
        heigth = 640;
        randomtimeGap = Math.floor(Math.random() * (11000 - 4000)) + 4000;
        keys = game.input.keyboard.createCursorKeys();

        game.stage.backgroundColor = '#000';             
 
        for(var i = 0; i < 1; i++){                                    
            snake[i] = game.add.sprite(160 + i*blockSize, 160, 'snake');  // se crea el primer bloque de la vibora
        }

        this.generateApple(); 
        this.randomIntervalApple();
        
        game.add.text(540, 50, "SCORE", { font: "bolder 14px monospace", fill: "#c155ff", align: "center" });
        scoreText = game.add.text(598, 50, score.toString(), { font: "bolder 14px monospace", fill: "#fff", align: "center" });      // Puntaje
        game.add.text(540, 20, "SPEED", { font: "bolder 14px monospace", fill: "#e5b849", align: "center" });
        speedText = game.add.text(598, 20, speed.toString(), { font: "bolder 14px monospace", fill: "#fff", align: "center" });      // Velocidad
        
    },

    update: function() {     
        if (keys.right.isDown && direction != 'left')
        {
            newdirection = 'right';
        }
        else if (keys.left.isDown && direction != 'right')
        {
            newdirection = 'left';
        }
        else if (keys.up.isDown && direction != 'down')
        {
            newdirection = 'up';
        }
        else if (keys.down.isDown && direction != 'up')
        {
            newdirection = 'down';
        }
     
        speed = Math.min(10, Math.floor(score/5));  // calcula la velocidad basado en los puntos.
        speedText.text = '' + speed;           // actualizo el texto con la velocidad.

        updateDelay++;

        if (updateDelay % (10 - speed) == 0) {  

            var firstPos = snake[snake.length - 1],
                lastPos = snake.shift(),
                prevLastPosx = lastPos.x,
                prevLastPosy = lastPos.y;

            if(newdirection){
                direction = newdirection;
                newdirection = null;
            }

            if(direction == 'right'){

                lastPos.x = firstPos.x + 16;
                lastPos.y = firstPos.y;
            }
            else if(direction == 'left'){
                lastPos.x = firstPos.x - 16;
                lastPos.y = firstPos.y;
            }
            else if(direction == 'up'){
                lastPos.x = firstPos.x;
                lastPos.y = firstPos.y - 16;
            }
            else if(direction == 'down'){
                lastPos.x = firstPos.x;
                lastPos.y = firstPos.y + 16;
            }

            snake.push(lastPos);
            firstPos = lastPos;

            if(appleEaten){
                snake.unshift(game.add.sprite(prevLastPosx, prevLastPosy, 'snake'));    //agrego un bloque nuevo si se comio una manzana (appleEaten = true)
                appleEaten = false;
            }

            this.appleCollision();
            this.selfCollision(firstPos);
            this.wallCollision(firstPos);
        }
    },

    generateApple: function(){        
        randomX = Math.floor(Math.random() * 40 ) * blockSize,
        randomY = Math.floor(Math.random() * 30 ) * blockSize;
        apple = game.add.sprite(randomX, randomY, 'apple');
    },

    appleCollision: function() {
        for(var i = 0; i < snake.length; i++){
            if(snake[i].x == apple.x && snake[i].y == apple.y){
                appleEaten = true;
                apple.destroy();
                this.generateApple();
                score++;
                scoreText.text = score.toString();               
                randomtimeGap = Math.floor(Math.random() * (11000 - 4000)) + 4000;
            }
        }
    },

    selfCollision: function(head) {
        for(var i = 0; i < snake.length - 1; i++){
            if(head.x == snake[i].x && head.y == snake[i].y){
                clearInterval(intervalVar);
                game.state.start('Game_Over');
            }
        }
    },

    wallCollision: function(head) {
        if(head.x >= heigth || head.x < 0 || head.y >= width || head.y < 0){
            clearInterval(intervalVar);
            game.state.start('Game_Over');
        }
    }
};