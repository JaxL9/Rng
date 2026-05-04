import random
import math
import json
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import Color, Ellipse, Rectangle

# ---------------- SAVE FILE ----------------
SAVE_FILE = "save.json"

# ---------------- RARITIES ----------------
RARITIES = [
    ("Common", 65, (1,1,1,1)),
    ("Uncommon", 20, (0.4,1,0.4,1)),
    ("Rare", 10, (0.3,0.6,1,1)),
    ("Epic", 3, (0.8,0.3,1,1)),
    ("Legendary", 1.5, (1,0.8,0.2,1)),
    ("Mythic", 0.5, (1,0.2,0.2,1))
]

ITEMS = {
    "Common": "Rock",
    "Uncommon": "Iron",
    "Rare": "Crystal",
    "Epic": "Dragon Core",
    "Legendary": "Excalibur",
    "Mythic": "Infinity Relic"
}

# ---------------- SAVE SYSTEM ----------------
def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {"rolls": 0, "mythics": 0, "legendaries": 0}

def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

# ---------------- PARTICLE SYSTEM ----------------
class Particle(Widget):
    def __init__(self, x, y, color, **kwargs):
        super().__init__(**kwargs)

        self.vx = random.uniform(-6, 6)
        self.vy = random.uniform(2, 8)
        self.life = 1

        with self.canvas:
            Color(*color)
            self.rect = Rectangle(pos=(x, y), size=(6,6))

        self.x = x
        self.y = y

        Clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        self.life -= 0.03

        self.x += self.vx
        self.y += self.vy
        self.vy -= 0.25

        self.rect.pos = (self.x, self.y)

        if self.life <= 0:
            self.parent.remove_widget(self)
            return False

# ---------------- WHEEL ----------------
class Wheel(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.angle = 0
        self.callback = None

        Clock.schedule_interval(self.draw, 1/60)

    def draw(self, dt):
        self.canvas.clear()

        with self.canvas:
            # OUTER RING (multi-layer wheel feel)
            Color(0.15,0.15,0.25,1)
            Ellipse(pos=(self.center_x-160, self.center_y-160), size=(320,320))

            # INNER RING
            Color(0.1,0.1,0.18,1)
            Ellipse(pos=(self.center_x-110, self.center_y-110), size=(220,220))

            # SEGMENTS (fake visual wheel)
            for i, (name, _, color) in enumerate(RARITIES):
                Color(*color)
                Ellipse(
                    pos=(self.center_x-150, self.center_y-150),
                    size=(300,300),
                    angle_start=i*60 + self.angle,
                    angle_end=(i+1)*60 + self.angle
                )

    # 🎰 SPIN
    def spin(self, callback):
        self.callback = callback

        target = random.randint(720, 1440)

        anim = Animation(angle=self.angle + target, duration=2.5, t="out_cubic")
        anim.bind(on_complete=lambda *a: self.callback())
        anim.start(self)

# ---------------- MAIN GAME ----------------
class Game(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.data = load_data()

        # TITLE
        self.title = Label(text="RNG LEGENDS", font_size=28, size_hint_y=0.15)
        self.add_widget(self.title)

        # RESULT
        self.result = Label(text="Tap SPIN", font_size=30, size_hint_y=0.15)
        self.add_widget(self.result)

        # WHEEL
        self.wheel = Wheel(size_hint_y=0.5)
        self.add_widget(self.wheel)

        # BUTTON
        self.btn = Button(text="SPIN", size_hint_y=0.2)
        self.btn.bind(on_press=self.start_spin)
        self.add_widget(self.btn)

        # STATS
        self.stats = Label(
            text=self.get_stats(),
            font_size=16,
            size_hint_y=0.1
        )
        self.add_widget(self.stats)

    # ---------------- SPIN ----------------
    def start_spin(self, _):
        self.btn.disabled = True
        self.result.text = "Spinning..."

        self.wheel.spin(self.finish)

    # ---------------- FINISH ----------------
    def finish(self):
        rarity = self.pick_rarity()
        item = ITEMS[rarity]

        self.result.text = f"{item} [{rarity}]"

        color = next(c for n,_,c in RARITIES if n == rarity)
        self.result.color = color

        # update stats
        self.data["rolls"] += 1

        if rarity == "Legendary":
            self.data["legendaries"] += 1

        if rarity == "Mythic":
            self.data["mythics"] += 1

        save_data(self.data)
        self.stats.text = self.get_stats()

        # effects
        self.pop_effect()
        self.particles(rarity)
        self.flash(rarity)

        self.btn.disabled = False

    # ---------------- RNG ----------------
    def pick_rarity(self):
        r = random.uniform(0,100)
        total = 0

        for name, chance, _ in RARITIES:
            total += chance
            if r <= total:
                return name

        return "Common"

    # ---------------- EFFECTS ----------------
    def pop_effect(self):
        anim = Animation(font_size=38, duration=0.08) + Animation(font_size=30, duration=0.08)
        anim.start(self.result)

    def flash(self, rarity):
        if rarity in ["Epic","Legendary","Mythic"]:
            with self.canvas.before:
                Color(1,1,1,0.2 if rarity!="Mythic" else 0.4)
                self.flash_rect = Rectangle(pos=self.pos, size=self.size)

            Clock.schedule_once(self.clear_flash, 0.15)

    def clear_flash(self, dt):
        self.canvas.before.clear()

    def particles(self, rarity):
        if rarity in ["Epic","Legendary","Mythic"]:
            count = 20 if rarity != "Mythic" else 50

            base = {
                "Epic": (0.8,0.3,1),
                "Legendary": (1,0.8,0.2),
                "Mythic": (1,0.2,0.2)
            }[rarity]

            for _ in range(count):
                p = Particle(
                    self.center_x,
                    self.center_y,
                    (*base,1)
                )
                self.add_widget(p)

    # ---------------- STATS ----------------
    def get_stats(self):
        return f"Rolls: {self.data['rolls']} | Mythics: {self.data['mythics']} | Legendaries: {self.data['legendaries']}"

# ---------------- APP ----------------
class RNGApp(App):
    def build(self):
        return Game()

RNGApp().run()
