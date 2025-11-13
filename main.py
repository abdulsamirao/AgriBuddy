import customtkinter as ctk
from tkinter import filedialog, PhotoImage
from PIL import Image

from classifier_engine import BaseClassifier, \
                            TomatoLeafDiseaseClassifier, \
                            AgriculturePestClassifier, \
                            MangoDiseaseClassifier, \
                            CottonDiseaseClassifier

from tkinterdnd2 import DND_FILES, TkinterDnD
from database import init_database, create_user, authenticate_user


#  Color configuration
PRIMARY_GREEN = "#0A6847"
ACCENT_GREEN = "#128C7E"
LIGHT_BG = "#E8F5E9"         # Light green for panels
LIGHTER_BG = "#F6FFF8"       # Lighter green for main background
WHITE = "#FFFFFF"
TEXT_GRAY = "#5C5C5C"
DASHED_BORDER = "#128C7E"    # Accent color for drop zone border

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


# Main app window
# Inherits from both CTk and DnDWrapper
class AgriBuddyApp(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        
        # Initialize database
        init_database()
        
        self.title("AgriBuddy")
        self.wm_iconbitmap("icons/icon.ico")
        self.wm_iconphoto(True, PhotoImage(file="icons/icon.png"))
        self.geometry("900x600")
        self.minsize(800, 500)
        self.is_fullscreen = False
        self.frames = {}

        # Full screen toggle
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)

        # Main container
        container = ctk.CTkFrame(self, fg_color=LIGHTER_BG)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Add each page to dict for showing it
        for F in (LoginPage, SignUpPage, HomePage, TomatoPage, MangoPage, CottonPage, PestPage):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
        return "break"

    def end_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.attributes("-fullscreen", False)
        return "break"


# Login Page
class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=WHITE)
        self.controller = controller
        
        # Scroll frame
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)
        
        # Title frame
        title_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        title_frame.pack(pady=(60, 30))
        
        title = ctk.CTkLabel(title_frame, text="AgriBuddy🌾", 
                            font=("Segoe UI", 36, "bold"), text_color=PRIMARY_GREEN)
        title.pack()
        
        subtitle = ctk.CTkLabel(scroll_frame, text="Sign in to continue",
                               font=("Segoe UI", 16), text_color=TEXT_GRAY)
        subtitle.pack()
        
        # Login form frame
        form_frame = ctk.CTkFrame(scroll_frame, fg_color=LIGHT_BG, corner_radius=15)
        form_frame.pack(pady=(30, 20))
        
        # Email field
        email_label = ctk.CTkLabel(form_frame, text="Email", 
                                     font=("Segoe UI", 14, "bold"), text_color=PRIMARY_GREEN)
        email_label.pack(pady=(30, 5), padx=30)
        
        self.email_entry = ctk.CTkEntry(form_frame, width=300, height=40,
                                          font=("Segoe UI", 14), corner_radius=10)
        self.email_entry.pack(pady=(0, 15), padx=30)
        
        # Password field
        password_label = ctk.CTkLabel(form_frame, text="Password",
                                     font=("Segoe UI", 14, "bold"), text_color=PRIMARY_GREEN)
        password_label.pack(pady=(5, 5), padx=30)
        
        self.password_entry = ctk.CTkEntry(form_frame, width=300, height=40,
                                          font=("Segoe UI", 14), corner_radius=10,
                                          show="*")
        self.password_entry.pack(pady=(0, 20), padx=30)
        
        # Error message label
        self.error_label = ctk.CTkLabel(form_frame, text="", 
                                       font=("Segoe UI", 12), text_color="#FF0000")
        self.error_label.pack(pady=(0, 10))
        
        # Login button
        login_btn = ctk.CTkButton(form_frame, text="Login", width=300, height=45,
                                 fg_color=PRIMARY_GREEN, hover_color=ACCENT_GREEN,
                                 text_color=WHITE, font=("Segoe UI", 16, "bold"),
                                 corner_radius=10, command=self.handle_login)
        login_btn.pack(pady=(0, 20), padx=30)
        
        # Sign up link
        signup_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        signup_frame.pack(pady=(0, 30))
        
        signup_text = ctk.CTkLabel(signup_frame, text="Don't have an account? ",
                                  font=("Segoe UI", 12), text_color=TEXT_GRAY)
        signup_text.pack(side="left")
        
        signup_link = ctk.CTkButton(signup_frame, text="Sign Up", 
                                   fg_color="transparent", hover_color=LIGHT_BG,
                                   text_color=ACCENT_GREEN, font=("Segoe UI", 12, "bold"),
                                   command=lambda: controller.show_frame("SignUpPage"),
                                   width=80, height=20)
        signup_link.pack(side="left")
        
        # Bind Enter key to login
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
    
    def handle_login(self):
        """Handle login button click."""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if not email or not password:
            self.error_label.configure(text="Please enter both email and password")
            return
        
        # Disable UI during login
        self.error_label.configure(text="Logging in...", text_color=ACCENT_GREEN)
        
        # Perform (synchronous) authentication
        success, message = authenticate_user(email, password)
        self.login_callback(success, message)
        
        
    
    def login_callback(self, success: bool, message: str):
        """Callback after login attempt."""
        if success:
            self.error_label.configure(text="", text_color="#FF0000")
            self.controller.show_frame("HomePage")
        else:
            self.error_label.configure(text=message, text_color="#FF0000")


# Sign Up Page
class SignUpPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=WHITE)
        self.controller = controller
        
        # Scroll frame
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)
        
        # Title frame
        title_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        title_frame.pack(pady=40)
        
        title = ctk.CTkLabel(title_frame, text="Create Account",
                            font=("Segoe UI", 32, "bold"), text_color=PRIMARY_GREEN)
        title.pack()
        
        # Sign up form frame
        form_frame = ctk.CTkFrame(scroll_frame, fg_color=LIGHT_BG, corner_radius=15)
        form_frame.pack(pady=(0, 20))
        
        # Username field
        username_label = ctk.CTkLabel(form_frame, text="Username",
                                     font=("Segoe UI", 14, "bold"), text_color=PRIMARY_GREEN)
        username_label.pack(pady=(25, 5), padx=30)
        
        self.username_entry = ctk.CTkEntry(form_frame, width=300, height=40,
                                          font=("Segoe UI", 14), corner_radius=10)
        self.username_entry.pack(pady=(0, 10), padx=30)
        
        # Email field
        email_label = ctk.CTkLabel(form_frame, text="Email",
                                  font=("Segoe UI", 14, "bold"), text_color=PRIMARY_GREEN)
        email_label.pack(pady=(5, 5), padx=30)
        
        self.email_entry = ctk.CTkEntry(form_frame, width=300, height=40,
                                       font=("Segoe UI", 14), corner_radius=10)
        self.email_entry.pack(pady=(0, 10), padx=30)
        
        # Password field
        password_label = ctk.CTkLabel(form_frame, text="Password",
                                     font=("Segoe UI", 14, "bold"), text_color=PRIMARY_GREEN)
        password_label.pack(pady=(5, 5), padx=30)
        
        self.password_entry = ctk.CTkEntry(form_frame, width=300, height=40,
                                          font=("Segoe UI", 14), corner_radius=10,
                                          show="*")
        self.password_entry.pack(pady=(0, 10), padx=30)
        
        # Confirm password field
        confirm_password_label = ctk.CTkLabel(form_frame, text="Confirm Password",
                                             font=("Segoe UI", 14, "bold"), text_color=PRIMARY_GREEN)
        confirm_password_label.pack(pady=(5, 5), padx=30)
        
        self.confirm_password_entry = ctk.CTkEntry(form_frame, width=300, height=40,
                                                   font=("Segoe UI", 14), corner_radius=10,
                                                   show="*")
        self.confirm_password_entry.pack(pady=(0, 20), padx=30)
        
        # Error message label
        self.error_label = ctk.CTkLabel(form_frame, text="",
                                       font=("Segoe UI", 12), text_color="#FF0000")
        self.error_label.pack(pady=(0, 10))
        
        # Sign up button
        signup_btn = ctk.CTkButton(form_frame, text="Sign Up", width=300, height=45,
                                  fg_color=ACCENT_GREEN, hover_color=PRIMARY_GREEN,
                                  text_color=WHITE, font=("Segoe UI", 16, "bold"),
                                  corner_radius=10, command=self.handle_signup)
        signup_btn.pack(pady=(0, 20), padx=30)
        
        # Login link
        login_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        login_frame.pack(pady=(0, 25))
        
        login_text = ctk.CTkLabel(login_frame, text="Already have an account? ",
                                 font=("Segoe UI", 12), text_color=TEXT_GRAY)
        login_text.pack(side="left")
        
        login_link = ctk.CTkButton(login_frame, text="Login",
                                  fg_color="transparent", hover_color=LIGHT_BG,
                                  text_color=ACCENT_GREEN, font=("Segoe UI", 12, "bold"),
                                  command=lambda: controller.show_frame("LoginPage"),
                                  width=80, height=20)
        login_link.pack(side="left")
        
        # Bind Enter key to signup
        self.confirm_password_entry.bind("<Return>", lambda e: self.handle_signup())
    
    def handle_signup(self):
        """Handle sign up button click."""
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validation
        if not username or not email or not password or not confirm_password:
            self.error_label.configure(text="Please fill in all fields")
            return
        
        if password != confirm_password:
            self.error_label.configure(text="Passwords do not match")
            return
        
        if len(password) < 6:
            self.error_label.configure(text="Password must be at least 6 characters long")
            return
        
        # Basic email validation
        if "@" not in email or "." not in email.split("@")[-1]:
            self.error_label.configure(text="Please enter a valid email address")
            return
        
        # Disable UI during signup
        self.error_label.configure(text="Creating account...", text_color=ACCENT_GREEN)
        
        # Create user account
        success, message = create_user(username, email, password)
        self.signup_callback(success, message)
        
        
    
    def signup_callback(self, success: bool, message: str):
        """Callback after signup attempt."""
        if success:
            self.error_label.configure(text="", text_color="#FF0000")
            self.controller.show_frame("HomePage")
        else:
            self.error_label.configure(text=message, text_color="#FF0000")


# The page containing the options to select the model
class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=WHITE)
        self.controller = controller

        # Title frame (add gap between title and the top of window)
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(pady=(40, 20))
        
        title = ctk.CTkLabel(title_frame, text="AgriBuddy🌾", font=("Segoe UI", 32, "bold"), text_color=PRIMARY_GREEN)
        title.pack(side="left", padx=10)

        subtitle = ctk.CTkLabel(self, text="Your AI Assistant for Smart Farming",
                                font=("Segoe UI", 18), text_color=ACCENT_GREEN)
        subtitle.pack(pady=5)

        # Centered grid for model buttons
        grid_frame = ctk.CTkFrame(self, fg_color=WHITE)
        grid_frame.pack(expand=True, pady=0, padx=0, ipady=0, ipadx=0)

        models = [
            ("Tomato Leaf Disease", "TomatoPage"),
            ("Mango Leaf Disease", "MangoPage"),
            ("Cotton Leaf Disease", "CottonPage"),
            ("Agricultural Pest", "PestPage"),
        ]

        for i, (label, page) in enumerate[tuple[str, str]](models):
            # Shadow effect frame
            shadow = ctk.CTkFrame(grid_frame, fg_color="#D9F0E0", corner_radius=18)
            shadow.grid(row=i // 2, column=i % 2, padx=25, pady=25)

            button = ctk.CTkButton(
                shadow,
                text=label,
                width=200,
                height=130,
                corner_radius=15,
                font=("Segoe UI", 16, "bold"),
                fg_color=PRIMARY_GREEN,
                hover_color="#39A96B",
                text_color=WHITE,
                border_width=0,
                border_color=LIGHT_BG,
                command=lambda p=page: controller.show_frame(p)
            )
            
            button.pack(padx=5, pady=5)

        # Footer
        footer = ctk.CTkLabel(self, text="© 2025 AgriBuddy | All Rights Reserved", font=("Segoe UI", 11), text_color=TEXT_GRAY)
        footer.pack(side="bottom", pady=10)



#  Base class for model pages
class BaseModelPage(ctk.CTkFrame):
    def __init__(self, parent, controller, title_text, desc_text, model: BaseClassifier):
        super().__init__(parent, fg_color=WHITE)
        self.controller = controller
        self.selected_file_path = None # Store the path to the selected file
        self.model = model

        # Navigation bar
        nav_frame = ctk.CTkFrame(self, fg_color=PRIMARY_GREEN, height=60, corner_radius=0)
        nav_frame.pack(fill="x", side="top")

        home_btn = ctk.CTkButton(nav_frame, text="Home", width=90, fg_color=WHITE,
                                 text_color=PRIMARY_GREEN, hover_color=LIGHT_BG,
                                 font=("Segoe UI", 14, "bold"),
                                 command=lambda: controller.show_frame("HomePage"))
        home_btn.pack(side="left", padx=10, pady=10)

        title = ctk.CTkLabel(nav_frame, text=title_text,
                             font=("Segoe UI", 22, "bold"), text_color=WHITE)
        title.pack(side="left", expand=True, pady=10)


        # Main body
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        main_frame.grid_columnconfigure(1, weight=3)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Left panel (file upload)
        left_frame = ctk.CTkFrame(main_frame, fg_color=LIGHT_BG, corner_radius=15)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=10)

        # make it flexible vertically
        left_frame.grid_rowconfigure(3, weight=1)

        desc = ctk.CTkLabel(left_frame, text=desc_text, wraplength=230,
                            text_color=PRIMARY_GREEN, justify="left",
                            font=("Segoe UI", 14, "normal"))
        desc.grid(row=0, column=0, pady=(15, 10), padx=15, sticky="ew")

        # File drop frame
        self.drop_zone = ctk.CTkFrame(left_frame, fg_color=WHITE, border_width=2,
                                      border_color=DASHED_BORDER, corner_radius=10)
        self.drop_zone.grid(row=1, column=0, sticky="ew", padx=15, pady=10)

        drop_label = ctk.CTkLabel(self.drop_zone, text="Drag & Drop Image Here\n\n(or)",
                                  font=("Segoe UI", 13, "italic"), text_color=TEXT_GRAY)
        drop_label.pack(pady=(20, 10))

        upload_btn = ctk.CTkButton(self.drop_zone, text="Choose File",
                                   fg_color=PRIMARY_GREEN, hover_color=ACCENT_GREEN,
                                   text_color=WHITE, command=self.select_file)
        upload_btn.pack(pady=(0, 20), padx=20)

        # Image preview
        self.image_preview_label = ctk.CTkLabel(left_frame, text="No image selected",
                                                fg_color=LIGHTER_BG, corner_radius=8,
                                                height=160)
        self.image_preview_label.grid(row=2, column=0, sticky="ew", padx=15, pady=10)

        # Submit button
        submit_btn = ctk.CTkButton(
            left_frame,
            text="Submit",
            fg_color=ACCENT_GREEN,
            hover_color=PRIMARY_GREEN,
            text_color=WHITE,
            font=("Segoe UI", 16, "bold"),
            height=45,
            corner_radius=10,
            command=self.process_file
        )
        submit_btn.grid(row=4, column=0, sticky="ew", padx=20, pady=(10, 20))

        # Make sure grid expands properly
        for i in range(5):
            left_frame.grid_rowconfigure(i, weight=1 if i == 3 else 0) # allow middle section (row 3) to stretch (empty row)

        # DND Bindings
        self.drop_zone.drop_target_register(DND_FILES)
        self.drop_zone.dnd_bind('<<Drop>>', self.on_file_drop)
        self.drop_zone.dnd_bind('<<DragEnter>>', self.on_drag_enter)
        self.drop_zone.dnd_bind('<<DragLeave>>', self.on_drag_leave)

        # Right panel (output)
        right_frame = ctk.CTkFrame(main_frame, fg_color=LIGHTER_BG, corner_radius=15)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(15, 0), pady=10)

        output_title = ctk.CTkLabel(right_frame, text="Analysis Result",
                                     font=("Segoe UI", 18, "bold"), text_color=PRIMARY_GREEN)
        output_title.pack(pady=(15, 5), padx=20)

        self.output_box = ctk.CTkTextbox(right_frame, font=("Consolas", 13),
                                         text_color=PRIMARY_GREEN, wrap="word",
                                         fg_color=WHITE, border_width=1,
                                         border_color="#D0D0D0")
        self.output_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.output_box.insert("end", "Model output will appear here...\n")
        self.output_box.configure(state="disabled")

    
    

    def on_drag_enter(self, event):
        """Visual feedback when dragging over the drop zone."""
        self.drop_zone.configure(fg_color=LIGHT_BG)
        return event.action

    def on_drag_leave(self, event):
        """Reset visual when leaving the drop zone."""
        self.drop_zone.configure(fg_color=WHITE)
        return event.action
    
    def on_file_drop(self, event):
        """Handles the file drop event."""
        # event.data = "{FilePath1} {FilePath2}"
        
        file_paths: list[str] = event.data.strip("{}").split("} {")
        
        file_path = file_paths[0]

        self.selected_file_path = file_path
        self.load_and_display_image(file_path)
        self.on_drag_leave(event) # Reset bg color
        
        print(f"File dropped: {self.selected_file_path}")
        return event.action

    def select_file(self):
        """Opens a file dialog to select an image."""
        file_path = filedialog.askopenfilename(
            title="Select an image file",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif *.webp")]
        )
        if file_path:
            self.selected_file_path = file_path
            self.load_and_display_image(file_path)
            print(f"File selected: {self.selected_file_path}")

    def load_and_display_image(self, file_path):
        """Loads an image, creates a thumbnail, and displays it."""
        try:
            if not file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')):
                self.image_preview_label.configure(image=None, text="File is not a supported image.",
                                                   font=("Segoe UI", 12, "italic"))
                self.selected_file_path = None # Clear invalid file
                return

            image = Image.open(file_path)
            
            # Create a thumbnail
            image.thumbnail((200, 160))
            
            ctk_img = ctk.CTkImage(light_image=image, size=(image.width, image.height))
            
            # Display the image
            self.image_preview_label.configure(image=ctk_img, text="")
            self.image_preview_label.image = ctk_img # Prevent garbage collection

        except Exception as e:
            print(f"Error loading image: {e}")
            self.image_preview_label.configure(image=None, text=f"Error loading image:\n{e}",
                                               font=("Segoe UI", 12, "italic"))
            self.selected_file_path = None

    def process_file(self):
        """Handles the 'Submit' button click."""
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")

        if not self.selected_file_path:
            self.output_box.insert("end", "Error: Please select an image file first.")
            self.output_box.configure(state="disabled")
            return

        self.output_box.insert("end", f"Processing file: {self.selected_file_path.split('/')[-1]}\n\n")
        
        predicted_class, confidence = self.model.predict(self.selected_file_path)
        
        self.display_result(predicted_class, confidence)
        
        self.output_box.configure(state="disabled")

    def display_result(self, predicted_class, confidence):
        disease_name = predicted_class
        confidence = confidence * 100

        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", "✅ Processing Complete!\n\n")
        self.output_box.insert("end", f"File: {self.selected_file_path.split('/')[-1]}\n\n")
        self.output_box.insert("end", f"Detected Disease: {disease_name}\n")
        self.output_box.insert("end", f"Confidence: {confidence:.2f}%\n\n")


# Individual ML Model Pages
class TomatoPage(BaseModelPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,
                         "🍅 Tomato Leaf Disease Classifier",
                         "Upload an image of a tomato leaf. The model will analyze it and identify the disease.",
                         TomatoLeafDiseaseClassifier())


class MangoPage(BaseModelPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,
                         "🥭 Mango Leaf Disease Classifier",
                         "Upload an image of a mango leaf. The model will analyze it and identify the disease.",
                         MangoDiseaseClassifier())


class CottonPage(BaseModelPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,
                         "🌿 Cotton Leaf Disease Classifier",
                         "Upload an image of a cotton leaf. The model will analyze it and identify the disease.",
                         CottonDiseaseClassifier())


class PestPage(BaseModelPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,
                         "🐞 Agricultural Pest Classifier",
                         "Upload an image of an agricultural pest. The model will analyze it and find out what species it is.",
                         AgriculturePestClassifier())
    
    def display_result(self, predicted_class, confidence):
        disease_name = predicted_class
        confidence = confidence * 100

        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", "✅ Processing Complete!\n\n")
        self.output_box.insert("end", f"File: {self.selected_file_path.split('/')[-1]}\n\n")
        self.output_box.insert("end", f"Detected Pest: {disease_name}\n")
        self.output_box.insert("end", f"Confidence: {confidence:.2f}%\n\n")


# ---------------------------
#  Run the App
# ---------------------------
if __name__ == "__main__":
    app = AgriBuddyApp()
    app.mainloop()
