import random
import math

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.clock import Clock
from kivy.animation import Animation

from kivy.graphics import Color, Ellipse, Line, Rectangle

# ---------------- RARITY WHEEL ----------------
RARITIES = [
    ("Common", 60, (1,1,1,1)),
    ("Uncommon", 25, (0.4,1,0.4,1)),
    ("Rare", 10, (0.3,0.6,1,1)),
    ("Epic", 4, (0.8,0.3,1,1)),
    ("Legendary", 0.9, (1,0.8,0.2,1)),
    ("Mythic", 0.1, (1,0.2,0.2,1))
]

ITEMS = {
    "Common": "Rock",
    "Uncommon": "Iron",
    "Rare": "Gem",
    "Epic": "Dragon Scale",
    "Legendary": "Excalibur",
    "Mythic": "Infinity Core"
}

# ---------------- PARTICLE ----------------
class Particle(Widget):
    def __init__(self, x, y, color, **kwargs):
        super().__init__(**kwargs)
        self.x_speed = random.uniform(-6, 6)
        self.y_speed = random.uniform(3, 8)
        self.life = 1.0

        with self.canvas:
            Color(*color)
            self.dot = Rectangle(pos=(x, y), size=(6,6))

        self.pos_x = x
        self.pos_y = y

        Clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        self.life -= 0.03
        self.pos_x += self.x_speed
        self.pos_y += self.y_speed
        self.y_speed -= 0.2

        self.dot.pos = (self.pos_x, self.pos_y)

        if self.life <= 0:
            self.parent.remove_widget(self)
            return False

# ---------------- WHEEL ----------------
class Wheel(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.angle = 0
        self.result = None

        with self.canvas:
            self.circle_color = Color(0.2, 0.2, 0.3, 1)
            self.circle = Ellipse(pos=self.center, size=(300,300))

            self.line_color = Color(1,1,1,1)
            self.line = Line(circle=(0,0,140), width=2)

        Clock.schedule_interval(self.draw, 1/60)

    def draw(self, dt):
        self.circle.pos = (self.center_x - 150, self.center_y - 150)

    def spin(self, callback):
        self.result = callback

        target_rotation = random.randint(720, 1440)

        anim = Animation(angle=self.angle + target_rotation, duration=2.5, t="out_cubic")
        anim.bind(on_progress=self.update_rotation)
        anim.bind(on_complete=self.finish_spin)
        anim.start(self)

    def update_rotation(self, anim, widget, progress):
        self.canvas.clear()

        with self.canvas:
            Color(0.15,0.15,0.2,1)
            Ellipse(pos=(self.center_x-150,self.center_y-150), size=(300,300))

            # wheel segments
            for i, (name, _, color) in enumerate(RARITIES):
                start = i * 60
                Color(*color)
                Ellipse(
                    pos=(self.center_x-150,self.center_y-150),
                    size=(300,300),
                    angle_start=start + self.angle,
                    angle_end=start + 60 + self.angle
                )

    def finish_spin(self, *args):
        rarity = self.pick_rarity()
        self.result(rarity)

    def pick_rarity(self):
        roll = random.uniform(0,100)
        total = 0

        for name, chance, _ in RARITIES:
            total += chance
            if roll <= total:
                return name

        return "Common"

# ---------------- GAME ----------------
class Game(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.result = Label(text="Tap to Spin", font_size=32, size_hint_y=0.2)
        self.add_widget(self.result)

        self.wheel = Wheel()
        self.add_widget(self.wheel)

        self.btn = Button(text="SPIN", size_hint_y=0.2)
        self.btn.bind(on_press=self.spin)
        self.add_widget(self.btn)

    # ---------------- SPIN ----------------
    def spin(self, _):
        self.btn.disabled = True

        self.wheel.spin(self.show_result)

    # ---------------- RESULT ----------------
    def show_result(self, rarity):
        item = ITEMS[rarity]

        self.result.text = f"{item} [{rarity}]"

        color = {
            "Common": (1,1,1,1),
            "Uncommon": (0.4,1,0.4,1),
            "Rare": (0.3,0.6,1,1),
            "Epic": (0.8,0.3,1,1),
            "Legendary": (1,0.8,0.2,1),
            "Mythic": (1,0.2,0.2,1)
        }[rarity]

        self.result.color = color

        self.pop_effect()
        self.particles(rarity)

        self.btn.disabled = False

    # ---------------- POP ----------------
    def pop_effect(self):
        anim = Animation(font_size=40, duration=0.1) + Animation(font_size=32, duration=0.1)
        anim.start(self.result)

    # ---------------- PARTICLES ----------------
    def particles(self, rarity):
        if rarity in ["Epic","Legendary","Mythic"]:
            count = 25 if rarity != "Mythic" else 60

            color = {
                "Epic": (0.8,0.3,1),
                "Legendary": (1,0.8,0.2),
                "Mythic": (1,0.2,0.2)
            }[rarity]

            for _ in range(count):
                p = Particle(
                    self.center_x,
                    self.center_y,
                    (*color,1)
                )
                self.add_widget(p)

# ---------------- APP ----------------
class RNGApp(App):
    def build(self):
        return Game()

RNGApp().run()
