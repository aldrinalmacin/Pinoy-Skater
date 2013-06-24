import cocos

"""
  name: MainScene
  desc: The main screen to be shown when the game is loaded.
"""
class MainScene(cocos.scene.Scene):
  BG_IMGS = ["images/scrollingbgback.png", "images/scrollingbg.png", "images/scrollingbgfront.png", "images/scrollingbgfast.png"]
  def __init__(self, director_window):
    super(MainScene, self).__init__()

    # Create an instance of the scroller
    self.background_scroller = ParallaxScroller(director_window)

    # Call the method to set the background of the scene
    self.set_parallax_background()

    self.add(self.background_scroller)

  """
    name: set background
    desc: Sets the background image to the background layer of the scene
  """
  def set_parallax_background(self):
    # Create the background image
    scrollable_layers = []
    for i in range(0, len(MainScene.BG_IMGS)):
      scrollable_sprite = cocos.sprite.Sprite(MainScene.BG_IMGS[i], anchor=(0,0))
      scrollable_layer = cocos.layer.scrolling.ScrollableLayer(parallax=i)
      scrollable_layer.px_width = 1200
      scrollable_layer.px_height = 500
      scrollable_layer.add(scrollable_sprite)
      scrollable_layers.append(scrollable_layer)

    self.background_scroller.add_children(scrollable_layers)

class ParallaxScroller(cocos.layer.scrolling.ScrollingManager):
  PARALLAX_SPEED = 10
  WIDTH = 1200
  def __init__(self, viewport=None):
    super(ParallaxScroller, self).__init__(viewport)
    self.schedule_interval(self.start_moving, 0.1)
    self.current_x = self.viewport.width / 2

  def start_moving(self, *args, **kwargs):
    for layer in self.get_children():
      if layer.x <= -ParallaxScroller.WIDTH:
        layer.set_view(0, layer.y, 600, 500)

    if self.current_x + ParallaxScroller.PARALLAX_SPEED <= ParallaxScroller.WIDTH - (self.viewport.width / 2):
      self.current_x += ParallaxScroller.PARALLAX_SPEED
    else:
      self.current_x = self.viewport.width / 2
    self.set_focus(self.current_x, 0)

  def add_children(self, layers):
    for layer in layers:
      self.add(layer)
