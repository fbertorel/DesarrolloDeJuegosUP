var Game_Over = {

    preload : function() {
        game.load.image('gameover', './assets/img/gameover.png');
    },

    create : function() {
        this.add.button(0, 0, 'gameover', this.startGame, this);
        game.add.text(480, 300, "SCORE", { font: "bolder 24px monospace", fill: "#ff993c", align: "center"}); 
        game.add.text(560, 300, score.toString(), { font: "bolder 24px monospace", fill: "#ff993c", align: "center" });
    },

    startGame: function () {
        this.state.start('Game');
    }
};