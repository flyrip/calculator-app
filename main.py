import random
import traceback
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock

# Переменная, куда запишется ошибка анимации, если она случится
error_log = ""

class SnowBackground(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flakes = []
        Clock.schedule_interval(self.update_snow, 1.0 / 60.0)

    def update_snow(self, dt):
        global error_log
        try:
            if self.width <= 100:
                return
                
            if not self.flakes:
                for _ in range(40):  # Оптимизировали до 40 снежинок
                    self.flakes.append({
                        'x': random.uniform(0, self.width),
                        'y': random.uniform(0, self.height),
                        'size': random.uniform(3, 6),
                        'speed': random.uniform(40, 90) * dt
                    })

            self.canvas.clear()
            with self.canvas:
                for flake in self.flakes:
                    flake['y'] -= flake['speed']
                    flake['x'] += random.uniform(-8, 8) * dt

                    if flake['y'] < 0:
                        flake['y'] = self.height
                        flake['x'] = random.uniform(0, self.width)
                    
                    if flake['x'] < 0: flake['x'] = self.width
                    if flake['x'] > self.width: flake['x'] = 0

                    Color(1, 1, 1, 0.6)
                    Ellipse(pos=(flake['x'], flake['y']), size=(flake['size'], flake['size']))
        except Exception as e:
            error_log = f"Ошибка анимации:\n{traceback.format_exc()}"

class CalculatorApp(App):
    def build(self):
        try:
            Window.clearcolor = (0.05, 0.05, 0.06, 1)
            root = FloatLayout()
            
            # Слой 1: Снег
            self.snow_bg = SnowBackground()
            root.add_widget(self.snow_bg)
            
            # Слой 2: Интерфейс калькулятора
            main_layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
            
            # Дисплей
            self.display = Label(
                text="0",
                font_size='56sp',
                bold=True,
                halign='right',
                valign='bottom',
                size_hint=(1, 0.3),
                color=(1, 1, 1, 1)
            )
            # Безопасное выравнивание для мобилок
            self.display.bind(size=lambda instance, size: setattr(instance, 'text_size', size))
            main_layout.add_widget(self.display)
            
            # Сетка кнопок
            buttons_layout = GridLayout(cols=4, spacing=12)
            
            color_digit = (0.21, 0.21, 0.23, 0.85)  
            color_op = (1, 0.62, 0.04, 0.85)     
            color_spec = (0.65, 0.65, 0.65, 0.85)   
            
            buttons = [
                ('C', color_spec, (0, 0, 0, 1)),    ('(', color_spec, (0, 0, 0, 1)),    (')', color_spec, (0, 0, 0, 1)),    ('/', color_op, (1, 1, 1, 1)),
                ('7', color_digit, (1, 1, 1, 1)),   ('8', color_digit, (1, 1, 1, 1)),   ('9', color_digit, (1, 1, 1, 1)),   ('*', color_op, (1, 1, 1, 1)),
                ('4', color_digit, (1, 1, 1, 1)),   ('5', color_digit, (1, 1, 1, 1)),   ('6', color_digit, (1, 1, 1, 1)),   ('-', color_op, (1, 1, 1, 1)),
                ('1', color_digit, (1, 1, 1, 1)),   ('2', color_digit, (1, 1, 1, 1)),   ('3', color_digit, (1, 1, 1, 1)),   ('+', color_op, (1, 1, 1, 1)),
                ('0', color_digit, (1, 1, 1, 1)),   ('.', color_digit, (1, 1, 1, 1)),   ('<', color_digit, (1, 1, 1, 1)),   ('=', color_op, (1, 1, 1, 1))
            ]
            
            for text, bg_color, text_color in buttons:
                btn = Button(
                    text=text,
                    font_size='32sp',
                    bold=True,
                    background_normal='',
                    background_color=bg_color,
                    color=text_color,
                    on_press=self.on_button_press
                )
                buttons_layout.add_widget(btn)
                
            main_layout.add_widget(buttons_layout)
            root.add_widget(main_layout)
            
            # Проверка: если анимация успела выдать ошибку при старте, покажем её вместо калькулятора
            if error_log:
                return Label(text=error_log, font_size='14sp', color=(1, 0, 0, 1))
                
            return root
        except Exception as e:
            # Если упал сам калькулятор, выводим лог критической ошибки
            return Label(text=f"Крит при запуске:\n{traceback.format_exc()}", font_size='14sp', color=(1, 0, 0, 1))
            
    def on_button_press(self, instance):
        global error_log
        # Если в процессе работы упала анимация, выведем это на дисплей
        if error_log:
            self.display.text = "Ошибка анимации!"
            return

        current = self.display.text
        button_text = instance.text
        
        if button_text == 'C':
            self.display.text = '0'
        elif button_text == '=':
            try:
                self.display.text = str(eval(current))
            except Exception:
                self.display.text = 'Ошибка'
        elif button_text == '<':
            if len(current) > 1 and current != 'Ошибка':
                self.display.text = current[:-1]
            else:
                self.display.text = '0'
        else:
            if current == '0' or current == 'Ошибка':
                self.display.text = button_text
            else:
                self.display.text += button_text

if __name__ == '__main__':
    CalculatorApp().run()
