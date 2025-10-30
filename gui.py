import customtkinter as ctk
from tkinter import filedialog

# ---------------------------
#  App Configuration
# ---------------------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class AgriBuddyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AgriBuddy")
        self.geometry("900x600")
        self.resizable(False, False)
        self.frames = {}

        container = ctk.CTkFrame(self, fg_color="white")
        container.pack(fill="both", expand=True)

        for F in (HomePage, ML1Page, ML2Page, ML3Page, ML4Page):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


# ---------------------------
#  Home Page
# ---------------------------
class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="white")
        self.controller = controller

        title = ctk.CTkLabel(self, text="🌱 AgriBuddy", font=("Helvetica", 28, "bold"), text_color="#0A6847")
        title.pack(pady=40)

        subtitle = ctk.CTkLabel(
            self,
            text="Select a Machine Learning Model to Begin",
            font=("Helvetica", 16),
            text_color="#2E8B57"
        )
        subtitle.pack(pady=10)

        grid_frame = ctk.CTkFrame(self, fg_color="white")
        grid_frame.pack(pady=40)

        models = [
            ("ML Model 1", "ML1Page"),
            ("ML Model 2", "ML2Page"),
            ("ML Model 3", "ML3Page"),
            ("ML Model 4", "ML4Page")
        ]

        for i, (label, page) in enumerate(models):
            button = ctk.CTkButton(
                grid_frame,
                text=label,
                width=180,
                height=120,
                corner_radius=15,
                font=("Helvetica", 15, "bold"),
                fg_color="#0A6847",
                hover_color="#128C7E",
                text_color="white",
                command=lambda p=page: controller.show_frame(p)
            )
            button.grid(row=i // 2, column=i % 2, padx=30, pady=30)


# ---------------------------
#  Base Class for ML Pages
# ---------------------------
class BaseModelPage(ctk.CTkFrame):
    def __init__(self, parent, controller, title_text, desc_text):
        super().__init__(parent, fg_color="white")
        self.controller = controller

        # Top Navigation
        nav_frame = ctk.CTkFrame(self, fg_color="#0A6847", height=60)
        nav_frame.pack(fill="x", side="top")
        home_btn = ctk.CTkButton(nav_frame, text="🏠 Home", width=80, fg_color="white",
                                 text_color="#0A6847", hover_color="#DFF6E5",
                                 command=lambda: controller.show_frame("HomePage"))
        home_btn.pack(side="left", padx=20, pady=10)

        title = ctk.CTkLabel(nav_frame, text=title_text, font=("Helvetica", 22, "bold"), text_color="white")
        title.pack(pady=10)

        # Main Layout
        main_frame = ctk.CTkFrame(self, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Left: File Upload Section
        left_frame = ctk.CTkFrame(main_frame, fg_color="#E8F5E9", corner_radius=15)
        left_frame.pack(side="left", fill="y", padx=20, pady=10, ipadx=10)

        desc = ctk.CTkLabel(left_frame, text=desc_text, wraplength=220,
                            text_color="#0A6847", justify="left")
        desc.pack(pady=15, padx=10)

        self.file_label = ctk.CTkLabel(left_frame, text="No file selected", text_color="gray")
        self.file_label.pack(pady=5)

        upload_btn = ctk.CTkButton(left_frame, text="📁 Choose File", fg_color="#0A6847",
                                   hover_color="#128C7E", text_color="white", command=self.select_file)
        upload_btn.pack(pady=10)

        submit_btn = ctk.CTkButton(left_frame, text="Submit", fg_color="#128C7E",
                                   hover_color="#0A6847", text_color="white", command=self.show_output)
        submit_btn.pack(pady=10)

        # Right: Output Section
        right_frame = ctk.CTkFrame(main_frame, fg_color="#F6FFF8", corner_radius=15)
        right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=10)

        self.output_box = ctk.CTkTextbox(right_frame, width=400, height=400,
                                         font=("Consolas", 13), text_color="#0A6847")
        self.output_box.pack(padx=20, pady=20)
        self.output_box.insert("end", "Model output will appear here...\n")
        self.output_box.configure(state="disabled")

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_label.configure(text=file_path.split("/")[-1])

    def show_output(self):
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", "✅ Placeholder output:\nModel prediction or analysis result would appear here.")
        self.output_box.configure(state="disabled")


# ---------------------------
#  ML Model Pages
# ---------------------------
class ML1Page(BaseModelPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Model 1 - Crop Health Detection",
                         "Uploads an image or dataset to predict crop health status.")


class ML2Page(BaseModelPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Model 2 - Soil Quality Analysis",
                         "Analyzes soil composition data to suggest crop compatibility.")


class ML3Page(BaseModelPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Model 3 - Weather Pattern Predictor",
                         "Predicts weather impact on agricultural productivity.")


class ML4Page(BaseModelPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Model 4 - Yield Estimation",
                         "Estimates crop yield based on growth stage and environmental inputs.")


# ---------------------------
#  Run the App
# ---------------------------
if __name__ == "__main__":
    app = AgriBuddyApp()
    app.mainloop()

