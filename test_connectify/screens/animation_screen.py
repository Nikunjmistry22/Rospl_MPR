from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.clock import Clock
# from test_connectify.app_main import NavigationBar
#
class AnimationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a BoxLayout to organize the animation content vertically
        layout = BoxLayout(orientation='vertical', spacing=10)

        # Create an Image widget for the logo
        logo = Image(source='assets/images/logo.png', size_hint=(None, 1), size=(200, 200), pos_hint={'center_x': 0.5})

        # Create a Label for the text
        self.text_label = Label(text='', font_size=24, halign='center', opacity=0)

        # Add the logo and text to the layout
        layout.add_widget(self.text_label)
        layout.add_widget(logo)

        # Add the layout to the AnimationScreen
        self.add_widget(layout)

        # Initialize the text for animation
        self.animation_text = "Welcome to Connectify"
        self.animation_index = 0

        # Schedule a function to start the animation
        Clock.schedule_once(self.start_animation, 1)

    def start_animation(self, dt):
        self.animate_text()

    def animate_text(self, *args):
        # Check if we've reached the end of the text
        if self.animation_index >= len(self.animation_text):
            # Create the animation to change the text to "Have Fun"
            have_fun_animation = Animation(opacity=1, duration=2)


            # Start the "Have Fun" animation
            have_fun_animation.start(self.text_label)
            have_fun_animation.bind(on_complete=self.go_to_home)
        else:
            # Add the next letter to the text and create a fade-in animation
            letter = self.animation_text[self.animation_index]
            self.text_label.text += letter

            fade_in_animation = Animation(opacity=1, duration=0.5)

            # Start the letter fade-in animation
            fade_in_animation.start(self.text_label)
            fade_in_animation.bind(on_complete=self.animate_text)

            self.animation_index += 1

    def go_to_home(self, *args):
        # Use App.get_running_app() to access the Connectify app instance
        app = App.get_running_app()
        screen_manager = app.root

        # Transition to the home screen
        screen_manager.current = 'home'  # Assuming 'home' is the name of your HomeScreen
