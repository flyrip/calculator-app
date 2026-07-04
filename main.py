from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class CalculatorApp(App):
    def build(self):
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None
        
        # Главный вертикальный контейнер
        main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        
        # Поле вывода результата
        self.solution = TextInput(
            multiline=False, readonly=True, halign="right", font_size=55,
            background_color=(0.1, 0.1, 0.1, 1), foreground_color=(1, 1, 1, 1)
        )
        main_layout.add_widget(self.solution)
        
        # Сетка кнопок
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"],
        ]
        
        for row in buttons:
            h_layout = BoxLayout(spacing=10)
            for label in row:
                button = Button(
                    text=label,
                    font_size=30,
                    background_color=(0.2, 0.2, 0.2, 1) if label not in self.operators else (0.9, 0.5, 0.1, 1)
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)
            
        # Кнопка "Равно"
        equals_button = Button(
            text="=", font_size=30, background_color=(0.1, 0.7, 0.3, 1)
        )
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)
        
        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            self.solution.text = ""
        else:
            if current and (self.last_was_operator and button_text in self.operators):
                return
            elif current == "" and button_text in self.operators:
                return
            else:
                self.solution.text = current + button_text
        
        self.last_button = instance
        self.last_was_operator = button_text in self.operators

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            try:
                self.solution.text = str(eval(self.solution.text))
            except Exception:
                self.solution.text = "Ошибка"

if __name__ == "__main__":
    CalculatorApp().run()
