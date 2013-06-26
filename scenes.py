import cocos
from cocos.actions.interval_actions import *
from cocos.sprite import *
import time

"""
  name: MainScene
  desc: The main screen to be shown when the game is loaded.
"""
class MainScene(cocos.scene.Scene):
  BG_IMGS = ["images/scrollingbgback.png", "images/scrollingbg.png", "images/scrollingbgfront.png", "images/scrollingbgfast.png"]
  WIDTH = 1200
  HEIGHT = 500
  def __init__(self, director_window):
    super(MainScene, self).__init__()

    # Create an instance of the scroller
    self.background_scroller = ParallaxScroller(director_window)

    # Call the method to set the background of the scene
    self.set_parallax_background()

    self.game_layer = GameLayer()

    self.add(self.background_scroller, z=1)
    self.add(self.game_layer, z=2)

  """
    name: set background
    desc: Sets the background image to the background layer of the scene
  """
  def set_parallax_background(self):
    # Create the background image
    scrollable_layers = []
    for i in range(0, len(MainScene.BG_IMGS)):
      scrollable_sprite = Sprite(MainScene.BG_IMGS[i], anchor=(0,0))
      scrollable_layer = cocos.layer.scrolling.ScrollableLayer(parallax=i)
      scrollable_layer.px_width = MainScene.WIDTH
      scrollable_layer.px_height = MainScene.HEIGHT
      scrollable_layer.add(scrollable_sprite)
      scrollable_layers.append(scrollable_layer)

    self.background_scroller.add_children(scrollable_layers)

class ParallaxScroller(cocos.layer.scrolling.ScrollingManager):
  PARALLAX_SPEED = 10
  PARALLAX_INTERVAL = 0.1
  def __init__(self, viewport=None):
    super(ParallaxScroller, self).__init__(viewport)
    self.schedule_interval(self.start_moving, ParallaxScroller.PARALLAX_INTERVAL)
    self.current_x = self.viewport.width / 2

  def start_moving(self, *args, **kwargs):
    for layer in self.get_children():
      if layer.x <= -MainScene.WIDTH:
        layer.set_view(0, layer.y, MainScene.WIDTH / 2, MainScene.HEIGHT)

    if self.current_x + ParallaxScroller.PARALLAX_SPEED <= MainScene.WIDTH - (self.viewport.width / 2):
      self.current_x += ParallaxScroller.PARALLAX_SPEED
    else:
      self.current_x = self.viewport.width / 2
    self.set_focus(self.current_x, 0)

  def add_children(self, layers):
    for layer in layers:
      self.add(layer)

class GameLayer(cocos.layer.base_layers.Layer):
  UP = 119
  DOWN = 115
  is_event_handler = True
  HEIGHT = 200
  def __init__(self):
    super(GameLayer, self).__init__()
    self.size = (MainScene.WIDTH / 2, GameLayer.HEIGHT)
    self.hero = Hero()
    self.add(self.hero)

  def on_key_press(self, key, modifiers):
    if GameLayer.UP == key:
      self.hero.hero_action(Hero.JUMPING)
    elif GameLayer.DOWN == key:
      self.hero.hero_action(Hero.SLIDING)

class Hero(cocos.cocosnode.CocosNode):
  IMAGE_RUN1 = "images/katipunero.png"
  IMAGE_RUN2 = "images/katipunero_run.png"
  SLIDE_NAME = "images/katipunero_slide.png"
  JUMP_NAME = "images/katipunero_jump.png"
  JUMPING = "Jumping"
  SLIDING = "Sliding"
  X = 100
  Y = 100
  RUNNING_CHANGE = .25
  ACTION_DURATION = 0.5

  def __init__(self):
    super(Hero, self).__init__()
    self.hero_running_1 = Sprite(Hero.IMAGE_RUN1)
    self.hero_running_2 = Sprite(Hero.IMAGE_RUN2)
    self.hero_slide = Sprite(Hero.SLIDE_NAME)
    self.hero_jump = Sprite(Hero.JUMP_NAME)

    self.add(self.hero_slide)
    self.add(self.hero_running_1)
    self.add(self.hero_running_2)
    self.add(self.hero_jump)

    self.hero_running_2.visible = False
    self.hero_slide.visible = False
    self.hero_jump.visible = False
    self.sliding = False
    self.jumping = False
    self.position = (Hero.X, Hero.Y)

    self.schedule_interval(self.animate_running, Hero.RUNNING_CHANGE)

  def hero_action(self, action_type):
    if not self.jumping and not self.sliding:
      self.hero_running_1.visible = False
      self.hero_running_2.visible = False

      delay = Delay(0.5)

      hide_and_show = Lerp("visible", False, True, Hero.ACTION_DURATION)
      show_and_hide = Lerp("visible", True, False, Hero.ACTION_DURATION)

      if action_type == Hero.JUMPING:
        self.jumping = True
        jump = Jump(x=0, y=Hero.Y, duration=Hero.ACTION_DURATION)
        self.do(jump)
        state_change = Lerp("jumping", self.jumping, not self.jumping, Hero.ACTION_DURATION)
        self.hero_jump.do(show_and_hide)
      elif action_type == Hero.SLIDING:
        self.sliding = True
        state_change = Lerp("sliding", self.sliding, not self.sliding, Hero.ACTION_DURATION)
        self.hero_slide.do(show_and_hide)

      self.do(delay + state_change)
      self.hero_running_1.do(delay + hide_and_show)

  def animate_running(self, *args, **kwargs):
    if not self.sliding and not self.jumping:
      self.hero_running_1.visible = not self.hero_running_1.visible
      self.hero_running_2.visible = not self.hero_running_2.visible
