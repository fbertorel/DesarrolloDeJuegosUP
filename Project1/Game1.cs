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

        private Texture2D yoda;

        public Game1()          //Constructor
        {
            _graphics = new GraphicsDeviceManager(this);
            this.Content.RootDirectory = "Content";          //Define donde estara el contenido
            this.IsMouseVisible = true;
        }

        protected override void Initialize()
        {
            // TODO: Add your initialization logic here
            this.score = 0;
            this.maxScore = 0;

            base.Initialize();                              //base es como usar super en java. 
        }

        protected override void LoadContent()               //loading de un juego
        {
            spriteBatch = new SpriteBatch(GraphicsDevice);     //se usa para ayudar a hacer los dibujos (que se hacen dentro de Draw)

            yoda = Content.Load<Texture2D>("dark yoda");        //cargue la imagen en el objeto


            // TODO: use this.Content to load your game content here
        }

        protected override void Update(GameTime gameTime)
        {
            if (GamePad.GetState(PlayerIndex.One).Buttons.Back == ButtonState.Pressed || Keyboard.GetState().IsKeyDown(Keys.Escape))
                Exit();

            // TODO: Add your update logic here

            base.Update(gameTime);
        }

        protected override void Draw(GameTime gameTime)
        {
            GraphicsDevice.Clear(Color.CornflowerBlue);

            // TODO: Add your drawing code here

            spriteBatch.Begin();
            spriteBatch.Draw(yoda, new Rectangle(0,0, _graphics.GraphicsDevice.Viewport.Width, _graphics.GraphicsDevice.Viewport.Height), Color.White);      //con esto dibujo el yoda. El vector es 0,0 es abajo a la izq.

            spriteBatch.End();

            base.Draw(gameTime);
        }
    }
}
