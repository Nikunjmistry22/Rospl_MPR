from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager,SlideTransition
from screens.home_screen import HomeScreen
from screens.qr_code_scanner import QRScannerScreen
from screens.user_profile import UserProfileScreen
from screens.animation_screen import AnimationScreen
import db
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class NavigationBar(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.orientation = 'horizontal'

        home_button = Button(text='Home', on_release=self.go_to_home)
        qr_button = Button(text='QR Scanner', on_release=self.go_to_qr_scanner)
        profile_button = Button(text='User Profile', on_release=self.go_to_user_profile)

        self.add_widget(home_button)
        self.add_widget(qr_button)
        self.add_widget(profile_button)

    def go_to_home(self, instance):
        self.screen_manager.current = 'home'

    def go_to_qr_scanner(self, instance):
        self.screen_manager.current = 'qr_scanner'

    def go_to_user_profile(self, instance):
        self.screen_manager.current = 'user_profile'


class Connectify(App):
    def build(self):
        # Create a ScreenManager
        Window.size = (350, 550)
        sm = ScreenManager(transition=SlideTransition())

        # Add screens to the ScreenManager
        sm.add_widget(AnimationScreen(name='animation_screen'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(QRScannerScreen(name='qr_scanner'))
        sm.add_widget(UserProfileScreen(name='user_profile'))

        # Create the navigation bar and pass the ScreenManager to it
        nav_bar = NavigationBar(screen_manager=sm)

        # Create a layout for the changing screens (95% of the space)
        screens_layout = BoxLayout(orientation='vertical')
        screens_layout.add_widget(sm)

        # Create the main layout with the changing screens layout and the navigation bar (2% of the space)
        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(screens_layout)
        main_layout.add_widget(nav_bar)

        # Set the size hints to allocate 95% and 5% of the space respectively
        screens_layout.size_hint = (1, 0.95)
        nav_bar.size_hint = (1, 0.05)
        return main_layout


if __name__ == '__main__':
    Connectify().run()
