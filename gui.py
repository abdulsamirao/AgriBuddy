import customtkinter as ctk
from tkinter import filedialog
from PIL import Image  # Used for image previews

from classifier_engine import TomatoLeafDiseaseClassifier, AgriculturePestClassifier, MangoDiseaseClassifier, CottonDiseaseClassifier

from tkinterdnd2 import DND_FILES, TkinterDnD


# ---------------------------
#  Theme Configuration
# ---------------------------
PRIMARY_GREEN = "#0A6847"
ACCENT_GREEN = "#128C7E"
LIGHT_BG = "#E8F5E9"         # Light green for panels
LIGHTER_BG = "#F6FFF8"       # Lighter green for main background
WHITE = "#FFFFFF"
TEXT_GRAY = "#5C5C5C"
DASHED_BORDER = "#128C7E"    # Accent color for drop zone border

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


# ---------------------------
#  Main App Class
# ---------------------------
class AgriBuddyApp(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        
        self.title("AgriBuddy 🌱")
        self.geometry("900x600")
        self.minsize(800, 500)
        self.is_fullscreen = False
        self.frames = {}

        # Key bindings
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)

        # Main container
        container = ctk.CTkFrame(self, fg_color=LIGHTER_BG)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (HomePage, ML1Page, ML2Page, ML3Page, ML4Page):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

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


# ---------------------------
#  Home Page
# ---------------------------
class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=LIGHTER_BG) # Use lighter bg for main
        self.controller = controller

        # Title
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(pady=(40, 20))
        
        title = ctk.CTkLabel(title_frame, text="🌾 AgriBuddy", font=("Segoe UI", 32, "bold"), text_color=PRIMARY_GREEN)
        title.pack(side="left", padx=10)

        subtitle = ctk.CTkLabel(self, text="Your AI Assistant for Smart Farming",
                                font=("Segoe UI", 18), text_color=ACCENT_GREEN)
        subtitle.pack(pady=5)

        # Centered grid for model buttons
        # This frame acts as a "card"
        grid_frame = ctk.CTkFrame(self, fg_color=WHITE, corner_radius=15)
        grid_frame.pack(expand=True, pady=30, padx=50, ipady=20, ipadx=20)

        models = [
            ("Leaf Disease Detection", "ML1Page"),
            ("Soil Quality Analysis", "ML2Page"),
            ("Crop Yield Prediction", "ML3Page"),
            ("Weather Impact Model", "ML4Page")
        ]

        for i, (label, page) in enumerate[tuple[str, str]](models):
            # Shadow effect frame
            shadow = ctk.CTkFrame(grid_frame, fg_color="#D9F0E0", corner_radius=18)
            shadow.grid(row=i // 2, column=i % 2, padx=35, pady=30)

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
                border_width=1,
                border_color=LIGHT_BG,
                command=lambda p=page: controller.show_frame(p)
            )
            button.pack(padx=3, pady=3)

        # Footer
        footer = ctk.CTkLabel(self, text="© 2025 AgriBuddy | All Rights Reserved",
                              font=("Segoe UI", 11), text_color=TEXT_GRAY)
        footer.pack(side="bottom", pady=10)


# ---------------------------
#  Base Class for ML Pages
# ---------------------------
class BaseModelPage(ctk.CTkFrame):
    def __init__(self, parent, controller, title_text, desc_text):
        super().__init__(parent, fg_color=WHITE)
        self.controller = controller
        self.selected_file_path = None # Store the path to the selected file

        # ---------------------------
        # Navigation Bar
        # ---------------------------
        nav_frame = ctk.CTkFrame(self, fg_color=PRIMARY_GREEN, height=60, corner_radius=0)
        nav_frame.pack(fill="x", side="top")

        home_btn = ctk.CTkButton(nav_frame, text="🏠 Home", width=90, fg_color=WHITE,
                                 text_color=PRIMARY_GREEN, hover_color=LIGHT_BG,
                                 font=("Segoe UI", 14, "bold"),
                                 command=lambda: controller.show_frame("HomePage"))
        home_btn.pack(side="left", padx=20, pady=10)

        title = ctk.CTkLabel(nav_frame, text=title_text,
                             font=("Segoe UI", 22, "bold"), text_color=WHITE)
        title.pack(side="left", expand=True, pady=10)

        version_label = ctk.CTkLabel(nav_frame, text="v1.1", font=("Segoe UI", 12),
                                     text_color=WHITE)
        #version_label.pack(side="right", padx=10)

        # Theme toggle button
        self.theme_button = ctk.CTkButton(nav_frame, text=self.get_theme_icon(), width=35, height=30,
                                   fg_color=ACCENT_GREEN, hover_color="#39A96B",
                                   font=("Segoe UI", 16),
                                   command=self.toggle_theme)
        #self.theme_button.pack(side="right", padx=15, pady=10)

                # ---------------------------
        # Main Layout
        # ---------------------------
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

        # --- Drop Zone ---
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

        # --- Image Preview ---
        self.image_preview_label = ctk.CTkLabel(left_frame, text="No image selected",
                                                fg_color=LIGHTER_BG, corner_radius=8,
                                                height=160)
        self.image_preview_label.grid(row=2, column=0, sticky="ew", padx=15, pady=10)

        # --- Submit Button ---
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

        # --- Make sure grid expands properly ---
        for i in range(5):
            left_frame.grid_rowconfigure(i, weight=0)
        left_frame.grid_rowconfigure(3, weight=1)  # allow middle section to stretch

        # --- DND Bindings ---
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

    # ---------------------------
    # Helper Methods
    # ---------------------------

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
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            self.selected_file_path = file_path
            self.load_and_display_image(file_path)
            print(f"File selected: {self.selected_file_path}")

    def load_and_display_image(self, file_path):
        """Loads an image, creates a thumbnail, and displays it."""
        try:
            if not file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                self.image_preview_label.configure(image=None, text="File is not a supported image.",
                                                   font=("Segoe UI", 12, "italic"))
                self.selected_file_path = None # Clear invalid file
                return

            image = Image.open(file_path)
            
            # Create a thumbnail
            preview_width = self.image_preview_label.winfo_width() - 20
            preview_height = self.image_preview_label.winfo_height() - 20
            if preview_width < 50 or preview_height < 50:
                 preview_width, preview_height = 200, 160 # default fallback
                 
            image.thumbnail((preview_width, preview_height))
            
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
            self.output_box.insert("end", "❌ Error: Please select an image file first.")
            self.output_box.configure(state="disabled")
            return

        self.output_box.insert("end", f"⏳ Processing file: {self.selected_file_path.split('/')[-1]}\n\n")
        
        # --- ML Model Integration Point ---
        # This is where you would call your model.
        # e.g., result = your_ml_model.predict(self.selected_file_path)
        # For now, we use a placeholder.
        # self.after(1200, lambda: self.display_placeholder_result(result))
        
        self.after(1200, self.display_placeholder_result) # Simulate processing time

    def display_placeholder_result(self):
        """Shows a placeholder result in the output box."""
        # Placeholder data - replace with actual model output
        disease_name = "Apple Scab (Venturia inaequalis)"
        confidence = "95.2%"
        recommendation = "Apply recommended fungicides. Prune infected branches."

        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", "✅ Processing Complete!\n\n")
        self.output_box.insert("end", f"File:\t\t{self.selected_file_path.split('/')[-1]}\n\n")
        self.output_box.insert("end", f"Detected Disease:\t{disease_name}\n")
        self.output_box.insert("end", f"Confidence Score:\t{confidence}\n\n")
        self.output_box.insert("end", f"Recommendation:\t{recommendation}\n\n")
        self.output_box.insert("end", "--- (This is a placeholder result) ---")
        self.output_box.configure(state="disabled")
        
        # Clear selection after processing
        self.selected_file_path = None
        self.image_preview_label.configure(image=None)

    def get_theme_icon(self):
        """Returns the correct icon based on the current theme."""
        return "Light Theme" if ctk.get_appearance_mode() == "Dark" else "Dark Theme"

    def toggle_theme(self):
        """Toggles the app's appearance mode between light and dark."""
        new_mode = "dark" if ctk.get_appearance_mode() == "Light" else "light"
        ctk.set_appearance_mode(new_mode)
        self.theme_button.configure(text=self.get_theme_icon())


# ---------------------------
#  ML Model Pages
# ---------------------------
class ML1Page(BaseModelPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,
                         "Model 1 - Leaf Disease Detection",
                         "Upload an image of a plant leaf. The model will analyze it and identify potential diseases.")


class ML2Page(BaseModelPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,
                         "Model 2 - Soil Quality Analysis",
                         "Upload soil data (e.g., CSV, JSON). This model will analyze composition and suggest crop compatibility.")


class ML3Page(BaseModelPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,
                         "Model 3 - Crop Yield Prediction",
                         "Input environmental data, crop type, and acreage to receive an estimated yield prediction.")


class ML4Page(BaseModelPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,
                         "Model 4 - Weather Impact Model",
                         "Analyze historical and forecasted weather data to predict its impact on your crops.")


# ---------------------------
#  Run the App
# ---------------------------
if __name__ == "__main__":
    app = AgriBuddyApp()
    app.mainloop()
