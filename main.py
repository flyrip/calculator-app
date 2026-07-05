import random
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

class SnowBackground(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flakes = []
        # Запускаем обновление анимации 60 раз в секунду
        Clock.schedule_interval(self.update_snow, 1.0 / 60.0)

    def update_snow(self, dt):
        # Если снежинки еще не созданы и размер экрана определился
        if not self.flakes and self.width > 100:
            for _ in range(60):  # Количество снежинок на экране
                self.flakes.append({
                    'x': random.uniform(0, self.width),
                    'y': random.uniform(0, self.height),
                    'size': random.uniform(3, 8),          # Случайный размер снежинки
                    'speed': random.uniform(40, 120) * dt  # Скорость падения
                })

        # Очищаем холст перед новой отрисовкой
        self.canvas.clear()
        
        with self.canvas:
            for flake in self.flakes:
                # Двигаем снежинку вниз
                flake['y'] -= flake['speed']
                # Добавляем легкое покачивание из стороны в сторону
                flake['x'] += random.uniform(-15, 15) * dt

                # Если снежинка упала за нижний край, возвращаем её наверх
                if flake['y'] < 0:
                    flake['y'] = self.height
                    flake['x'] = random.uniform(0, self.width)
                
                # Ограничиваем по бокам экрана
                if flake['x'] < 0: flake['x'] = self.width
                if flake['x'] > self.width: flake['x'] = 0

                # Рисуем белую полупрозрачную снежинку
                Color(1, 1, 1, 0.65)
                Ellipse(pos=(flake['x'], flake['y']), size=(flake['size'], flake['size']))

class CalculatorApp(App):
    def build(self):
        self.title = "Калькулятор со снегом"
        
        # Глубокий темный фон заднего плана
        Window.clearcolor = (0.05, 0.05, 0.06, 1)
        
        # Корневой слой, который позволяет накладывать виджеты друг на друга
        root = FloatLayout()
        
        # Слой 1: Наша анимация падающего снега
        self.snow_bg = SnowBackground()
        root.add_widget(self.snow_bg)
        
        # Слой 2: Основной интерфейс калькулятора (поверх снега)
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        
        # Дисплей калькулятора
        self.display = Label(
            text="0",
            font_size='56sp',
            bold=True,
            halign='right',
            valign='bottom',
            size_hint=(1, 0.3),
            color=(1, 1, 1, 1)
        )
        self.display.bind(size=self.display._update_text_size)
        main_layout.add_widget(self.display)
        
        # Сетка кнопок
        buttons_layout = GridLayout(cols=4, spacing=12)
        
        # Красивые цвета с прозрачностью 0.85 (четвертая цифра в RGBA)
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
        
        # Добавляем калькулятор на корневой FloatLayout
        root.add_widget(main_layout)
        
        return root
        
    def on_button_press(self, instance):
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
