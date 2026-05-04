import random
import json
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation

# ---------------- GAME DATA ----------------
RARITIES = [
    ("Common", 60),
    ("Uncommon", 25),
    ("Rare", 10),
    ("Epic", 4),
    ("Legendary", 0.9),
    ("Mythic", 0.1)
]

ITEMS = {
    "Common": ["Rock"],
    "Uncommon": ["Iron"],
    "Rare": ["Gem"],
    "Epic": ["Dragon Scale"],
    "Legendary": ["Excalibur"],
    "Mythic": ["Infinity Core"]
}

PET_MULT = {
    "Dog": 1.1,
    "Dragon": 2.0,
    "Void Cat": 5.0
}

MUTATION_MULT = {
    "Lucky": 1.2,
    "Blessed": 2.0,
    "Corrupted": 4.0
}

SAVE_FILE = "save.json"

# ---------------- STATE ----------------
coins = 0
luck = 1.0
inventory = []
pets = []
mutations = []

# ---------------- SAVE SYSTEM ----------------
def save():
    data = {
        "coins": coins,
        "luck": luck,
        "inventory": inventory,
        "pets": pets,
        "mutations": mutations
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load():
    global coins, luck, inventory, pets, mutations
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            d = json.load(f)
            coins = d.get("coins", 0)
            luck = d.get("luck", 1.0)
            inventory = d.get("inventory", [])
            pets = d.get("pets", [])
            mutations = d.get("mutations", [])

# ---------------- MULTIPLIERS ----------------
def pet_mult():
    return max([PET_MULT.get(p, 1) for p in pets], default=1)

def mutation_mult():
    m = 1
    for x in mutations:
        m *= MUTATION_MULT.get(x, 1)
    return m

# ---------------- RNG SYSTEM ----------------
def roll():
    global coins

    total_mult = luck * pet_mult() * mutation_mult()

    roll_val = random.uniform(0, 100) / total_mult
    current = 0

    for rarity, chance in RARITIES:
        current += chance
        if roll_val <= current:
            item = random.choice(ITEMS[rarity])
            inventory.append(f"{item} [{rarity}]")
            coins += int(10 * (1 / (chance + 0.01)))

            # mutation chance
            if random.randint(1, 40) == 1:
                m = random.choice(list(MUTATION_MULT.keys()))
                if m not in mutations:
                    mutations.append(m)

            return f"{item} [{rarity}]"

    return "Nothing"

# ---------------- UI ----------------
class Game(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        Window.clearcolor = (0.06, 0.06, 0.08, 1)

        # TOP BAR
        self.top = BoxLayout(size_hint_y=0.15)
        self.stats = Label(text="Coins: 0 | Luck: 1.0", font_size=18)
        self.top.add_widget(self.stats)
        self.add_widget(self.top)

        # CENTER CARD
        self.center = BoxLayout()

        self.card = BoxLayout(orientation="vertical", padding=25, spacing=10)

        self.result = Label(text="Tap ROLL", font_size=30)

        self.roll_btn = Button(
            text="ROLL",
            font_size=24,
            background_normal="",
            background_color=(0.2, 0.6, 1, 1)
        )

        self.roll_btn.bind(on_press=self.start_roll_animation)

        self.card.add_widget(self.result)
        self.card.add_widget(self.roll_btn)

        self.center.add_widget(self.card)
        self.add_widget(self.center)

        # BOTTOM BAR
        self.bottom = GridLayout(cols=3, size_hint_y=0.2)

        self.shop_btn = Button(text="SHOP")
        self.inv_btn = Button(text="INV")
        self.save_btn = Button(text="SAVE")

        self.shop_btn.bind(on_press=self.shop)
        self.inv_btn.bind(on_press=self.show_inv)
        self.save_btn.bind(on_press=lambda x: save())

        self.bottom.add_widget(self.shop_btn)
        self.bottom.add_widget(self.inv_btn)
        self.bottom.add_widget(self.save_btn)

        self.add_widget(self.bottom)

        load()
        self.update_ui("Loaded Game")

    # ---------------- UI UPDATE ----------------
    def update_ui(self, msg=""):
        self.stats.text = f"Coins: {coins} | Luck: {round(luck,2)}"
        self.result.text = msg

    # ---------------- ROLL ANIMATION ----------------
    def start_roll_animation(self, _):
        self.roll_btn.disabled = True

        self.frames = ["Rolling.", "Rolling..", "Rolling...", "Calculating...", "Almost..."]
        self.i = 0

        self.event = Clock.schedule_interval(self.spin, 0.15)

    def spin(self, dt):
        self.result.text = self.frames[self.i % len(self.frames)]
        self.i += 1

        if self.i > 10:
            self.event.cancel()
            self.finish_roll()

    # ---------------- FINAL RESULT ----------------
    def finish_roll(self):
        result = roll()

        rarity = result.split("[")[-1].replace("]", "")

        colors = {
            "Common": (1,1,1,1),
            "Uncommon": (0.4,1,0.4,1),
            "Rare": (0.3,0.6,1,1),
            "Epic": (0.8,0.3,1,1),
            "Legendary": (1,0.8,0.2,1),
            "Mythic": (1,0.2,0.2,1)
        }

        self.result.color = colors.get(rarity, (1,1,1,1))

        anim = Animation(font_size=40, duration=0.1) + Animation(font_size=30, duration=0.1)
        anim.start(self.result)

        self.update_ui(result)
        self.roll_btn.disabled = False
        save()

    # ---------------- SHOP ----------------
    def shop(self, _):
        global coins, luck

        if coins >= 100:
            coins -= 100
            luck += 0.2
            self.update_ui("Bought Luck Upgrade")

    # ---------------- INVENTORY ----------------
    def show_inv(self, _):
        self.update_ui("Inventory:\n" + "\n".join(inventory[-6:]))

# ---------------- APP ----------------
class RNGApp(App):
    def build(self):
        return Game()

RNGApp().run()
