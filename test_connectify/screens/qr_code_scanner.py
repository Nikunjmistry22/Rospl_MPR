import cv2
import numpy as np
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from pyzbar.pyzbar import decode
import webbrowser

class QRScannerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a BoxLayout to organize the UI elements vertically with different height percentages
        layout = BoxLayout(orientation='vertical', spacing=10, padding=0)

        # Create a BoxLayout for the camera with 25% of the height
        camera_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.45))

        # Create a Camera widget with play=False initially
        self.camera = Camera(play=False, resolution=(350, 400), size_hint=(None, None), size=(350, 400))

        # Create a BoxLayout for the text label and "Start Camera" button with 5% and 70% of the height respectively
        text_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.5))

        # Create a label to display the QR code message
        self.qr_code_label = Label(text='', font_size=16, halign='center')

        # Create a button to start the camera scanning
        start_camera_button = Button(text='Start Camera', on_release=self.start_camera, size_hint=(1, 0.2))

        # Add the camera to the camera layout
        camera_layout.add_widget(self.camera)
        # Add the camera layout to the main layout
        layout.add_widget(camera_layout)

        # Add the label and button to the text layout
        text_layout.add_widget(self.qr_code_label)
        text_layout.add_widget(start_camera_button)

        # Add the text layout to the main layout
        layout.add_widget(text_layout)

        # Add the layout to the QRScannerScreen
        self.add_widget(layout)

        # Flag to indicate if the camera is active
        self.camera_active = False

    def start_camera(self, instance):
        if not self.camera_active:
            # Start the camera and schedule the QR code scanning
            self.camera.play = True
            Clock.schedule_interval(self.scan_qr_code, 1.0 / 30)  # Schedule scanning every frame
            self.camera_active = True

    def on_leave(self):
        # Stop the camera when leaving the screen
        if self.camera_active:
            self.camera.play = False
            self.camera_active = False

    def scan_qr_code(self, dt):
        # Capture an image from the camera
        camera_texture = self.camera.texture

        if camera_texture is None:
            return

        # Convert the camera frame to a numpy array
        img_data = np.frombuffer(camera_texture.pixels, dtype=np.uint8)
        img_data = img_data.reshape(camera_texture.height, camera_texture.width, -1)

        # Convert to grayscale
        gray = cv2.cvtColor(img_data, cv2.COLOR_RGB2GRAY)

        # Decode QR codes using pyzbar
        decoded_objects = decode(gray)

        if decoded_objects:
            # Stop the camera
            self.camera.play = False

            # Display the QR code message
            message = decoded_objects[0].data.decode('utf-8')


            lines = message.splitlines()
            # print(lines)
            new_message_lines = []

            for line in lines:
                if not line:
                    continue
                parts = line.split(': ')
                key, value = parts[0], parts[1]

                if key == "Instagram":
                    value = "https://www.instagram.com/" + value
                elif key == "Facebook":
                    value = "https://www.facebook.com/" + value
                elif key == "Twitter":
                    value = "https://twitter.com/" + value
                elif key == "Snapchat":
                    value = "https://www.snapchat.com/add/" + value

                new_line = f"{key}: {value}"
                new_message_lines.append(new_line)

            new_message = '\n'.join(new_message_lines)
            # print(new_message)
            button_layout = GridLayout(cols=2, rows=len(new_message_lines))

            for line in new_message.splitlines():
                # Split the line into social media name and username
                social_media_name, username = line.split(': ')

                # Create a button with the social media name as text
                button = Button(text=social_media_name,size_hint=(1, 0.05))

                # Add an action to the button, e.g., open a link
                # Here, we just print the username as an example
                def on_button_click(instance, social_media_name=social_media_name, username=username):
                   webbrowser.open(username)



                button.bind(on_release=on_button_click)

                # Add the button to the layout
                button_layout.add_widget(button)

            # Add the GridLayout to your Kivy layout
            # For example, if your Kivy layout is a BoxLayout called main_layout:
            self.add_widget(button_layout)

            # self.qr_code_label.text = f'QR Code Message:\n{new_message}'
        else:
            self.qr_code_label.text = 'No QR Code detected'