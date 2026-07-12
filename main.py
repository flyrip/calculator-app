"""
Зимний калькулятор на Kivy
Снег анимируется в верхней панели (там, где дисплей).
Собирается через buildozer (buildozer.spec уже должен быть в проекте).
"""

import random
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.graphics import Color, Ellipse, RoundedRectangle
from kivy.core.window import Window

Window.clearcolor = (0.04, 0.05, 0.13, 1)  # тёмно-синяя ночь

KV = """
#:import dp kivy.metrics.dp

<CalcButton@Button>:
    background_normal: ""
    background_down: ""
    background_color: 0, 0, 0, 0
    font_size: "20sp"
    color: 0.92, 0.95, 1, 1
    canvas.before:
        Color:
            rgba: self.bg_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [16]
    bg_color: 0.15, 0.18, 0.28, 1

<OpButton@CalcButton>:
    bg_color: 0.13, 0.22, 0.32, 1
    color: 0.5, 0.85, 1, 1

<EqButton@CalcButton>:
    bg_color: 0, 0, 0, 0
    color: 0.14, 0.08, 0, 1
    canvas.before:
        Color:
            rgba: 1, 0.71, 0.42, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [16]

<FuncButton@CalcButton>:
    bg_color: 0.15, 0.18, 0.28, 1
    color: 0.6, 0.68, 0.8, 1
    font_size: "18sp"

<RootWidget>:
    orientation: "vertical"

    FloatLayout:
        size_hint_y: None
        height: dp(170)
        canvas.before:
            Color:
                rgba: 0.08, 0.1, 0.24, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [0, 0, 0, 0]

        SnowWidget:
            id: snow
            size_hint: 1, 1
            pos: self.parent.pos if self.parent else (0, 0)

        BoxLayout:
            orientation: "vertical"
            padding: [dp(20), dp(14)]
            size_hint: 1, 1
            Widget:
            Label:
                text: root.expr_text
                font_size: "16sp"
                color: 0.5, 0.58, 0.72, 1
                halign: "right"
                valign: "bottom"
                text_size: self.size
                size_hint_y: None
                height: dp(20)
            Label:
                text: root.result_text
                font_size: "42sp"
                bold: True
                color: 0.93, 0.96, 1, 1
                halign: "right"
                valign: "bottom"
                text_size: self.size
                size_hint_y: None
                height: dp(56)

    GridLayout:
        cols: 4
        padding: dp(18)
        spacing: dp(12)

        FuncButton:
            text: "C"
            on_release: root.clear_all()
        FuncButton:
            text: "+/-"
            on_release: root.toggle_sign()
        FuncButton:
            text: "%"
            on_release: root.to_percent()
        OpButton:
            text: "/"
            on_release: root.choose_operator("/")

        CalcButton:
            text: "7"
            on_release: root.input_number("7")
        CalcButton:
            text: "8"
            on_release: root.input_number("8")
        CalcButton:
            text: "9"
            on_release: root.input_number("9")
        OpButton:
            text: "x"
            on_release: root.choose_operator("*")

        CalcButton:
            text: "4"
            on_release: root.input_number("4")
        CalcButton:
            text: "5"
            on_release: root.input_number("5")
        CalcButton:
            text: "6"
            on_release: root.input_number("6")
        OpButton:
            text: "-"
            on_release: root.choose_operator("-")

        CalcButton:
            text: "1"
            on_release: root.input_number("1")
        CalcButton:
            text: "2"
            on_release: root.input_number("2")
        CalcButton:
            text: "3"
            on_release: root.input_number("3")
        OpButton:
            text: "+"
            on_release: root.choose_operator("+")

        CalcButton:
            text: "0"
            on_release: root.input_number("0")
        CalcButton:
            text: "."
            on_release: root.input_number(".")
        EqButton:
            text: "="
            on_release: root.evaluate()
"""


class SnowWidget(Widget):
    """Виджет, рисующий падающий снег внутри своих границ."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flakes = []
        self.bind(size=self._init_flakes, pos=self._init_flakes)
        Clock.schedule_interval(self._update, 1 / 30)

    def _init_flakes(self, *args):
        if self.width <= 0 or self.height <= 0:
            return
        if not self.flakes:
            count = max(20, int(self.width / 12))
            self.flakes = [self._new_flake(random_y=True) for _ in range(count)]
        self._redraw()

    def _new_flake(self, random_y=False):
        return {
            "x": random.uniform(0, self.width),
            "y": random.uniform(0, self.height) if random_y else self.height,
            "r": random.uniform(2, 5),
            "speed": random.uniform(20, 55),
            "drift": random.uniform(-10, 10),
            "alpha": random.uniform(0.4, 0.9),
        }

    def _update(self, dt):
        if self.width <= 0 or self.height <= 0:
            return
        for f in self.flakes:
            f["y"] -= f["speed"] * dt
            f["x"] += f["drift"] * dt
            if f["y"] < -5:
                f.update(self._new_flake(random_y=False))
            if f["x"] > self.width:
                f["x"] = 0
            elif f["x"] < 0:
                f["x"] = self.width
        self._redraw()

    def _redraw(self):
        self.canvas.after.clear()
        with self.canvas.after:
            for f in self.flakes:
                Color(1, 1, 1, f["alpha"])
                Ellipse(
                    pos=(self.x + f["x"], self.y + f["y"]),
                    size=(f["r"], f["r"]),
                )


class RootWidget(BoxLayout):
    expr_text = StringProperty("")
    result_text = StringProperty("0")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current = "0"
        self.previous = None
        self.operator = None
        self.just_evaluated = False
        self._refresh()

    def _refresh(self):
        self.result_text = self.current
        if self.previous is not None and self.operator:
            self.expr_text = f"{self.previous} {self.operator}"
        else:
            self.expr_text = ""

    def input_number(self, n):
        if self.just_evaluated:
            self.current = "0." if n == "." else n
            self.just_evaluated = False
        elif n == "." and "." in self.current:
            return
        elif self.current == "0" and n != ".":
            self.current = n
        else:
            self.current += n
        self._refresh()

    def choose_operator(self, op):
        if self.operator and not self.just_evaluated:
            self.evaluate()
        self.previous = self.current
        self.operator = op
        self.just_evaluated = False
        self.current = "0"
        self._refresh()

    def evaluate(self):
        if self.operator is None or self.previous is None:
            return
        try:
            a = float(self.previous)
            b = float(self.current)
            if self.operator == "+":
                res = a + b
            elif self.operator == "-":
                res = a - b
            elif self.operator == "*":
                res = a * b
            elif self.operator == "/":
                res = a / b if b != 0 else float("nan")
            else:
                return
            self.current = "Ошибка" if res != res else self._format(res)
        except (ValueError, ZeroDivisionError):
            self.current = "Ошибка"
        self.operator = None
        self.previous = None
        self.just_evaluated = True
        self._refresh()

    @staticmethod
    def _format(value):
        rounded = round(value, 10)
        if rounded == int(rounded):
            return str(int(rounded))
        return str(rounded)

    def clear_all(self):
        self.current = "0"
        self.previous = None
        self.operator = None
        self.just_evaluated = False
        self._refresh()

    def toggle_sign(self):
        if self.current == "0":
            return
        self.current = self.current[1:] if self.current.startswith("-") else "-" + self.current
        self._refresh()

    def to_percent(self):
        try:
            self.current = self._format(float(self.current) / 100)
        except ValueError:
            pass
        self._refresh()


class WinterCalculatorApp(App):
    def build(self):
        Builder.load_string(KV)
        return RootWidget()


if __name__ == "__main__":
    WinterCalculatorApp().run()
