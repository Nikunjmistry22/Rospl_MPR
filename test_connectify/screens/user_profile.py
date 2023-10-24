from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import qrcode,sqlite3

class UserProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logo_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=50)
        profile_layout = BoxLayout(orientation='vertical', spacing=10)

        # Create a DropDown for selecting a social media platform
        self.social_media_dropdown = DropDown()

        # Define social media platforms
        social_media_labels = ['Instagram', 'Facebook', 'Twitter', 'Snapchat']

        self.username_entries = {}  # Dictionary to store username entries

        for label_text in social_media_labels:
            btn = Button(text=label_text, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn, label_text=label_text: self.show_input_popup(label_text))
            self.social_media_dropdown.add_widget(btn)

            # Initialize the username entry for this platform
            self.username_entries[label_text] = ""

        # Create a Button to open the dropdown
        social_media_button = Button(text='Select Social Media',size_hint_y=None, height=30)
        social_media_button.bind(on_release=self.social_media_dropdown.open)

        # Create a Button to show the message
        show_message_button = Button(text='Show Message', on_release=self.show_message,size_hint_y=None, height=30)

        # Create a button for generating the QR code (initially empty)
        generate_qr_button = Button(text='Generate QR Code', on_release=self.show_confirmation_dialog,size_hint_y=None, height=30)

        show_qr_details_button = Button(text='Show Current QR Details',on_release=self.show_current_qr_details,size_hint_y=None,height=30,)

        # Add all the widgets to the profile layout
        profile_layout.add_widget(show_qr_details_button)
        profile_layout.add_widget(social_media_button)
        profile_layout.add_widget(show_message_button)
        profile_layout.add_widget(generate_qr_button)

        # Initialize the message
        self.message = ""

        # Add the profile layout to the UserProfileScreen
        self.add_widget(profile_layout)

    def show_input_popup(self, platform):
        # Check if a username entry already exists for this platform
        if self.username_entries[platform]:
            popup = Popup(
                title='Warning',
                content=Label(text=f'Username for {platform} already exists'),
                size_hint=(None, None),
                size=(300, 150),
            )
            popup.open()
            return

        # Create a popup for user input
        content = BoxLayout(orientation='vertical', spacing=10)
        input_field = TextInput(hint_text=f'Enter {platform} Username', multiline=False)
        confirm_button = Button(text='Confirm')
        cancel_button = Button(text='Cancel')

        content.add_widget(input_field)
        content_buttons = BoxLayout(spacing=10)
        content_buttons.add_widget(confirm_button)
        content_buttons.add_widget(cancel_button)
        content.add_widget(content_buttons)

        popup = Popup(
            title=f'Enter {platform} Username',
            content=content,
            size_hint=(None, None),
            size=(300, 150),
            auto_dismiss=False
        )

        def on_confirm_button(instance):
            input_text = input_field.text.strip()
            if input_text:
                # Set the username entry for this platform
                self.username_entries[platform] = input_text
                # Append the new information to the existing message
                self.message += f'\n{platform}: {input_text}'
                # Update the selected_input field
                popup.dismiss()
            else:
                Popup(
                    title='Warning',
                    content=Label(text='No username written on input box'),
                    size_hint=(None, None),
                    size=(350, 150),
                ).open()

        def on_cancel_button(instance):
            popup.dismiss()

        confirm_button.bind(on_release=on_confirm_button)
        cancel_button.bind(on_release=on_cancel_button)

        popup.open()

    def show_message(self, instance):
        if not self.message:
            popup = Popup(
                title='Message',
                content=Label(text='No username mentioned for any platform'),
                size_hint=(None, None),
                size=(350, 150),
            )
        else:
            popup = Popup(
                title='Message',
                content=Label(text=self.message),
                size_hint=(None, None),
                size=(350, 150),
            )
        popup.open()

    def show_confirmation_dialog(self, instance):
        if not self.message:
            popup = Popup(
                title='Warning',
                content=Label(text='No username mentioned for any platform'),
                size_hint=(None, None),
                size=(350, 150),
            )
            popup.open()
            return

        # Create a confirmation dialog
        confirm_dialog = Popup(
            title='Generate QR Code',
            content=BoxLayout(orientation='vertical', spacing=10),
            size_hint=(None, None),
            size=(350, 150),
        )

        confirm_label = Label(text='Are you sure you want to generate the QR code?')

        confirm_button = Button(text='Yes', size_hint=(None, None), size=(100, 44))
        cancel_button = Button(text='No', size_hint=(None, None), size=(100, 44))

        # Center the "Yes" and "No" buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(None, None), size=(200, 44))
        button_layout.add_widget(confirm_button)
        button_layout.add_widget(cancel_button)

        def generate_qr_and_close(instance):
            self.generate_qr_code(instance)
            confirm_dialog.dismiss()

        def close_dialog(instance):
            confirm_dialog.dismiss()

        confirm_button.bind(on_release=generate_qr_and_close)
        cancel_button.bind(on_release=close_dialog)

        confirm_dialog.content.add_widget(confirm_label)
        confirm_dialog.content.add_widget(button_layout)
        confirm_dialog.open()

    def generate_qr_code(self, instance):
        # Generate the QR code and save it as qrcode.png
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.message)
        qr.make(fit=True)

        # Create a QR code image
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Save the image as qrcode.png in the assets/images directory
        qr_img.save("assets/images/qrcode.png")
        self.save_message_to_database()
        # Show a success popup
        success = Popup(
            title='Success',
            content=Label(text='Successfully generated QR Code'),
            size_hint=(None, None),
            size=(350, 150),
        )
        success.open()

    def save_message_to_database(self):
        # Define the path to the database file in your app's root directory
        db_path = 'connectify_db.db'

        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            # Check if there is existing data in the qr_details table
            cursor.execute("SELECT COUNT(*) FROM qr_details")
            result = cursor.fetchone()

            if result and result[0] > 0:
                # Update the existing message
                cursor.execute("UPDATE qr_details SET message = ?", (self.message,))
            else:
                # Insert the message into the database
                cursor.execute("INSERT INTO qr_details (message) VALUES (?)", (self.message,))

            conn.commit()
        except sqlite3.Error as e:
            # Handle any errors that may occur during database insertion or update
            print(f"Error inserting/updating message in the database: {e}")
        finally:
            conn.close()

    def show_current_qr_details(self, instance):
        # Define the path to the database file in your app's root directory
        db_path = 'connectify_db.db'  # Update this with your database file path

        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            # Fetch the most recent message from the database (you might need to adjust the query)
            cursor.execute("SELECT message FROM qr_details")
            result = cursor.fetchone()

            if result:
                message = result[0]
                popup = Popup(
                    title='Current QR Details',
                    content=Label(text=message),
                    size_hint=(None, None),
                    size=(350, 200),
                )
                popup.open()
            else:
                popup = Popup(
                    title='Message',
                    content=Label(text='No QR code details found in the database'),
                    size_hint=(None, None),
                    size=(400, 150),
                )
                popup.open()

        except sqlite3.Error as e:
            print(f"SQLite Error: {e}")
        finally:
            conn.close()