using System;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;

namespace Project1
{
    public class Game1 : Game   //Game1 hereda de Game con :
    {
        private GraphicsDeviceManager _graphics;        //Game y GraphicsDeviceManager se encargan de renderizar
        private SpriteBatch spriteBatch;
        private int score;
        private int maxScore;
        private SpriteFont font;

        private Texture2D ball10;
        private Vector2 ballPos;

        private Random random;

        public Game1()          //Constructor
        {
            _graphics = new GraphicsDeviceManager(this);
            this.Content.RootDirectory = "Content";          //Define donde estara el contenido
            this.IsMouseVisible = true;
        }

        protected override void Initialize()
        {
            // TODO: Add your initialization logic here
            this.random = new Random();
            this.score = 0;
            this.maxScore = 0;
            this.ballPos = new Vector2(0, 0);

            base.Initialize();                              //base es como usar super en java. 
        }

        protected override void LoadContent()               //loading de un juego
        {
            spriteBatch = new SpriteBatch(GraphicsDevice);     //se usa para ayudar a hacer los dibujos (que se hacen dentro de Draw)

            ball10 = Content.Load<Texture2D>("10");        //cargue la imagen en el objeto

            font = Content.Load<SpriteFont>("textoNormal");

            // TODO: use this.Content to load your game content here
        }

        protected override void Update(GameTime gameTime)
        {
            if (GamePad.GetState(PlayerIndex.One).Buttons.Back == ButtonState.Pressed || Keyboard.GetState().IsKeyDown(Keys.Escape))
                Exit();

            // TODO: Add your update logic here
            if((long)gameTime.TotalGameTime.TotalSeconds % 5 == 0)        //si pasan mas de 5 seg. actualiza
            {
                int x = random.Next(0, this._graphics.GraphicsDevice.Viewport.Width - 50);      //se resta en ancho de la imagen para que no se vaya de la pantalla.
                int y = random.Next(0, this._graphics.GraphicsDevice.Viewport.Height - 50);
                this.ballPos = new Vector2(x, y);
            }

            if (Mouse.GetState().LeftButton == ButtonState.Pressed)
            {
                var posMouse = Mouse.GetState().Position;   //var es una forma abreviada de definir variables. Asigna el tipo segun el contexto.
                var recMouse = new Rectangle(posMouse.X, posMouse.Y, 1, 1);

                var recBall = new Rectangle((int)ballPos.X, (int)ballPos.Y, 50, 50);


                if (recBall.Intersects(recMouse))
                {
                    this.score += 1;
                }
            }

            base.Update(gameTime);
        }

        protected override void Draw(GameTime gameTime)
        {
            GraphicsDevice.Clear(Color.CornflowerBlue);

            // TODO: Add your drawing code here

            spriteBatch.Begin();
            spriteBatch.Draw(ball10, new Rectangle((int)this.ballPos.X, (int)this.ballPos.Y, 50, 50), Color.White);      //con esto dibujo el yoda. El vector es 0,0 es abajo a la izq.

            //spriteBatch.Draw(ball10, this.ballPos, null, Color.White, 0, this.ballPos, .1f, SpriteEffects.None, 0);

            spriteBatch.DrawString(font, "Puntaje: " + this.score, new Vector2(0, 0), Color.Green);

            spriteBatch.End();

            base.Draw(gameTime);
        }
    }
}
