import kivy
print("Kivy version:", kivy.__version__)

# Try importing some basic Kivy components
from kivy.app import App
from kivy.uix.label import Label

class TestApp(App):
    def build(self):
        return Label(text='Kivy Installation Test Successful!')

if __name__ == '__main__':
    print("Testing Kivy import and basic app creation...")
    try:
        app = TestApp()
        print("Kivy imported successfully!")
    except Exception as e:
        print(f"Error importing Kivy: {e}")