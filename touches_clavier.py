from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window

class KeyCodeApp(App):
    def build(self):
        return Label(text="Appuyez sur une touche pour voir son keycode")

    def on_key_down(self, window, keycode, scancode, codepoint, modifier):
        # Affiche le keycode sous forme de tuple (scancode, keyname)
        print(f"Touche pressée: {keycode}")

if __name__ == '__main__':
    app = KeyCodeApp()
    # Attache l'événement de touche à la fenêtre
    Window.bind(on_key_down=app.on_key_down)
    app.run()
