import customtkinter as ctk
import subprocess
import sys
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Launcher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mask Detection Launcher")
        self.geometry("800x500")
        self.resizable(False, False)

        self.process = None

        # ===== MAIN FRAME =====
        self.main_frame = ctk.CTkFrame(self, corner_radius=20)
        self.main_frame.pack(expand=True, fill="both", padx=40, pady=40)

        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="MASK DETECTION SYSTEM",
            font=("Arial", 28, "bold")
        )
        self.title_label.pack(pady=40)

        self.start_btn = ctk.CTkButton(
            self.main_frame,
            text="▶ START SYSTEM",
            height=50,
            font=("Arial", 18),
            command=self.start_system
        )
        self.start_btn.pack(pady=20, padx=100, fill="x")

        self.stop_btn = ctk.CTkButton(
            self.main_frame,
            text="⏹ STOP SYSTEM",
            height=50,
            font=("Arial", 18),
            fg_color="#8B0000",
            hover_color="#5C0000",
            command=self.stop_system
        )
        self.stop_btn.pack(pady=20, padx=100, fill="x")

        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="STATUS: IDLE",
            font=("Arial", 20),
            text_color="gray"
        )
        self.status_label.pack(pady=30)

    # ================= START =================
    def start_system(self):
        if self.process is None:
            self.process = subprocess.Popen(
                [sys.executable, "app2.py"]
            )
            self.status_label.configure(
                text="STATUS: RUNNING",
                text_color="green"
            )

    # ================= STOP =================
    def stop_system(self):
        if self.process is not None:
            self.process.terminate()
            self.process = None
            self.status_label.configure(
                text="STATUS: STOPPED",
                text_color="red"
            )


if __name__ == "__main__":
    app = Launcher()
    app.mainloop()
