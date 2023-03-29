"""
Platformer Game
"""
import arcade
import time

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.2
TILE_SCALING = 0.6

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 15
CROUCH_OFFSET = 30

# set a variable that is equal to one quarter of a second using the time module


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player1_sprite = None
        self.player2_sprite = None


        # Our physics engine
        self.physics_engine = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.character1_state = None
        self.character2_state = None

        self.character1_direction = None
        self.character2_direction = None

        self.p1startime = 0
        self.p2startime = 0
        self.p1checktime = 0
        self.p2checktime = 0

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Initialize Scene
        self.scene = arcade.Scene()

        # Set up the player, specifically placing it at these coordinates.
        t1 = arcade.load_texture("player1files/guyside.png", hit_box_algorithm="Simple")
        t2 = arcade.load_texture("player1files/guyjump.png", hit_box_algorithm="Simple")
        t3 = arcade.load_texture("player1files/guycrouch3.png", hit_box_algorithm="Simple")
        t4 = arcade.load_texture("player1files/standpunch.png", hit_box_algorithm="Simple")
        t5 = arcade.load_texture("player1files/jumppunch.png", hit_box_algorithm="Simple")
        t6 = arcade.load_texture("player1files/crouchpunch.png", hit_box_algorithm="Simple")
        t1m = arcade.load_texture("player1files/guyside.png", hit_box_algorithm="Simple", mirrored=True)
        t2m = arcade.load_texture("player1files/guyjump.png", hit_box_algorithm="Simple", mirrored=True)
        t3m = arcade.load_texture("player1files/guycrouch3.png", hit_box_algorithm="Simple", mirrored=True)
        t4m = arcade.load_texture("player1files/standpunch.png", hit_box_algorithm="Simple", mirrored=True)
        t5m = arcade.load_texture("player1files/jumppunch.png", hit_box_algorithm="Simple", mirrored=True)
        t6m = arcade.load_texture("player1files/crouchpunch.png", hit_box_algorithm="Simple", mirrored=True)

        s1 = arcade.load_texture("player2files/guyside.png", hit_box_algorithm="Simple")
        s2 = arcade.load_texture("player2files/guyjump.png", hit_box_algorithm="Simple")
        s3 = arcade.load_texture("player2files/guycrouch3.png", hit_box_algorithm="Simple")
        s4 = arcade.load_texture("player2files/standpunch.png", hit_box_algorithm="Simple")
        s5 = arcade.load_texture("player2files/jumppunch.png", hit_box_algorithm="Simple")
        s6 = arcade.load_texture("player2files/crouchpunch.png", hit_box_algorithm="Simple")
        s1m = arcade.load_texture("player2files/guyside.png", hit_box_algorithm="Simple", mirrored=True)
        s2m = arcade.load_texture("player2files/guyjump.png", hit_box_algorithm="Simple", mirrored=True)
        s3m = arcade.load_texture("player2files/guycrouch3.png", hit_box_algorithm="Simple", mirrored=True)
        s4m = arcade.load_texture("player2files/standpunch.png", hit_box_algorithm="Simple", mirrored=True)
        s5m = arcade.load_texture("player2files/jumppunch.png", hit_box_algorithm="Simple", mirrored=True)
        s6m = arcade.load_texture("player2files/crouchpunch.png", hit_box_algorithm="Simple", mirrored=True)


        self.player1_sprite = arcade.Sprite(scale=CHARACTER_SCALING)
        self.player1_sprite.center_x = 64
        self.player1_sprite.center_y = 128
        self.scene.add_sprite("Player1", self.player1_sprite)

        self.player1_sprite.append_texture(t1)
        self.player1_sprite.append_texture(t2)
        self.player1_sprite.append_texture(t3)
        self.player1_sprite.append_texture(t4)
        self.player1_sprite.append_texture(t5)
        self.player1_sprite.append_texture(t6)
        self.player1_sprite.append_texture(t1m)
        self.player1_sprite.append_texture(t2m)
        self.player1_sprite.append_texture(t3m)
        self.player1_sprite.append_texture(t4m)
        self.player1_sprite.append_texture(t5m)
        self.player1_sprite.append_texture(t6m)

        self.player1_sprite.set_texture(0)

        self.character1_state = "stand"
        self.character1_direction = "right"

        self.player2_sprite = arcade.Sprite(scale=CHARACTER_SCALING)
        self.player2_sprite.center_x = 564
        self.player2_sprite.center_y = 200
        self.scene.add_sprite("Player2", self.player2_sprite)

        self.player2_sprite.append_texture(s1)
        self.player2_sprite.append_texture(s2)
        self.player2_sprite.append_texture(s3)
        self.player2_sprite.append_texture(s4)
        self.player2_sprite.append_texture(s5)
        self.player2_sprite.append_texture(s6)
        self.player2_sprite.append_texture(s1m)
        self.player2_sprite.append_texture(s2m)
        self.player2_sprite.append_texture(s3m)
        self.player2_sprite.append_texture(s4m)
        self.player2_sprite.append_texture(s5m)
        self.player2_sprite.append_texture(s6m)

        self.player2_sprite.set_texture(0)

        self.character2_state = "stand"
        self.character2_direction = "left"



        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 100, 100):
            wall = arcade.Sprite("groundfloor.png", TILE_SCALING)
            wall.center_x = 500
            wall.center_y = -200
            self.scene.add_sprite("Walls", wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[512, 96], [256, 96], [768, 96]]

        # Create the 'physics engine' for both player characters
        self.physics_engine1 = arcade.PhysicsEnginePlatformer(
            self.player1_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"]
        )

        # create the 'physics engine' for player 2
        self.physics_engine2 = arcade.PhysicsEnginePlatformer(
            self.player2_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"]
        )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our Scene
        self.scene.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        # Player 1 controls
        if key == arcade.key.W:
            if self.physics_engine1.can_jump():
                self.player1_sprite.change_y = PLAYER_JUMP_SPEED
                self.character1_state = "jump"
        elif key == arcade.key.A:
            self.player1_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            # change player sprite to face left
        elif key == arcade.key.D:
            self.player1_sprite.change_x = PLAYER_MOVEMENT_SPEED
            # change player sprite to face right
        elif key == arcade.key.S:
            # self.player_sprite.center_y -= CROUCH_OFFSET
            self.character1_state = "crouch"
        if key == arcade.key.G:
            self.p1punch()

        # Player 2 controls
        if key == arcade.key.UP:
            if self.physics_engine2.can_jump():
                self.player2_sprite.change_y = PLAYER_JUMP_SPEED
                self.character2_state = "jump"
        elif key == arcade.key.LEFT:
            self.player2_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            # change player sprite to face left
        elif key == arcade.key.RIGHT:
            self.player2_sprite.change_x = PLAYER_MOVEMENT_SPEED
            # change player sprite to face right
        elif key == arcade.key.DOWN:
            # self.player2_sprite.center_y -= CROUCH_OFFSET
            self.character2_state = "crouch"
        if key == arcade.key.M:
            self.p2punch()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        # Player 1 controls
        if key == arcade.key.W:
            self.player1_sprite.change_x = 0
        elif key == arcade.key.A:
            self.player1_sprite.change_x = 0
        elif key == arcade.key.D:
            self.player1_sprite.change_x = 0
        elif key == arcade.key.S:
            # lower player sprite when crouching
            self.character1_state = "stand"

        # Player 2 controls
        if key == arcade.key.UP:
            self.player2_sprite.change_x = 0
        elif key == arcade.key.LEFT:
            self.player2_sprite.change_x = 0
        elif key == arcade.key.RIGHT:
            self.player2_sprite.change_x = 0
        elif key == arcade.key.DOWN:
            # lower player sprite when crouching
            self.character2_state = "stand"

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine1.update()
        self.physics_engine2.update()

        # flip player direction if they have crossed sides with each other
        if self.player1_sprite.center_x < self.player2_sprite.center_x:
            self.character1_direction = "right"
            self.character2_direction = "left"

        elif self.player1_sprite.center_x > self.player2_sprite.center_x:
            self.character1_direction = "left"
            self.character2_direction = "right"


        self.p1checktime = time.time()
        if self.p1checktime - self.p1startime > 0.125:
            if self.character1_state == "standpunch":
                self.character1_state = "stand"
            elif self.character1_state == "crouchpunch":
                self.character1_state = "crouch"
            elif self.character1_state == "jumppunch":
                self.character1_state = "jump"

        self.p2checktime = time.time()
        if self.p2checktime - self.p2startime > 0.125:
            if self.character2_state == "standpunch":
                self.character2_state = "stand"
            elif self.character2_state == "crouchpunch":
                self.character2_state = "crouch"
            elif self.character2_state == "jumppunch":
                self.character2_state = "jump"


        side = 0
        if self.character1_direction == "left":
            side = 6

        if self.character1_state == "jump" and self.physics_engine1.can_jump():
            self.character1_state = "stand"
        elif self.character1_state == "jumppunch" and self.physics_engine1.can_jump():
            self.character1_state = "stand"
        elif self.character1_state == "stand":
            self.player1_sprite.set_texture(0+side)
        elif self.character1_state == "jump":
            self.player1_sprite.set_texture(1+side)
        elif self.character1_state == "crouch":
            self.player1_sprite.set_texture(2+side)
        elif self.character1_state == "standpunch":
            self.player1_sprite.set_texture(3+side)
        elif self.character1_state == "jumppunch":
            self.player1_sprite.set_texture(4+side)
        elif self.character1_state == "crouchpunch":
            self.player1_sprite.set_texture(5+side)

        side = 0
        if self.character2_direction == "right":
            side = 6

        if self.character2_state == "jump" and self.physics_engine2.can_jump():
            self.character2_state = "stand"
        elif self.character2_state == "jumppunch" and self.physics_engine2.can_jump():
            self.character2_state = "stand"
        elif self.character2_state == "stand":
            self.player2_sprite.set_texture(0+side)
        elif self.character2_state == "jump":
            self.player2_sprite.set_texture(1+side)
        elif self.character2_state == "crouch":
            self.player2_sprite.set_texture(2+side)
        elif self.character2_state == "standpunch":
            self.player2_sprite.set_texture(3+side)
        elif self.character2_state == "jumppunch":
            self.player2_sprite.set_texture(4+side)
        elif self.character2_state == "crouchpunch":
            self.player2_sprite.set_texture(5+side)

    def p1punch(self):
        # start a timer to change the state back to stand
        self.p1startime = time.time()
        if self.character1_state == "stand":
            self.character1_state = "standpunch"
        elif self.character1_state == "crouch":
            self.character1_state = "crouchpunch"
        elif self.character1_state == "jump":
            self.character1_state = "jumppunch"

    def p2punch(self):
        #start a timer to change the state back to stand
        self.p2startime = time.time()
        if self.character2_state == "stand":
            self.character2_state = "standpunch"
        elif self.character2_state == "crouch":
            self.character2_state = "crouchpunch"
        elif self.character2_state == "jump":
            self.character2_state = "jumppunch"


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()