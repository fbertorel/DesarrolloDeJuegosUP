var game = new Phaser.Game(640, 640, Phaser.AUTO, '');

game.state.add('Menu', Menu);
game.state.add('Game', Game);
game.state.add('Game_Over', Game_Over);


game.state.start('Menu')