import os
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a Label with the desired text and styling
        title_label = Label(
            text="Scan the Qr",
            font_size=24,
            halign='center',
            valign='middle'
        )

        # Get the path to the QR code image
        qr_code_path = "assets/images/qrcode.png"

        # Check if the QR code image file exists
        if os.path.exists(qr_code_path):
            # Create an Image widget to display the QR code
            self.qr_code_image = Image(source=qr_code_path, size_hint=(None, None), size=(215, 200))
        else:
            # Create a Label to display a message when no QR code is available
            self.qr_code_image = Label(text="No QR Code Generated Yet")

        # Create a BoxLayout to organize the widgets vertically
        layout = BoxLayout(orientation='vertical', spacing=10, padding=(65, 100))

        # Add the widgets to the layout
        layout.add_widget(title_label)
        layout.add_widget(self.qr_code_image)

        # Add the layout to the HomeScreen
        self.add_widget(layout)

    def update_qr_code(self, qr_code_path):
        # Update the QR code image source
        if os.path.exists(qr_code_path):
            self.qr_code_image.source = qr_code_path
        else:
            self.qr_code_image.text = "No QR Code Generated Yet"
