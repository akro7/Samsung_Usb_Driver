import os
import sys
import subprocess
import ctypes
import threading
import platform
import time
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def is_admin():
    try: 
        return ctypes.windll.shell32.IsUserAnAdmin()
    except: 
        return False

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class InstallerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("EKO FLASH PRO - Samsung Driver Installer")
        self.geometry("550x400")
        self.resizable(False, False)
        self.configure(fg_color="#0a0a0f")

        self.label = ctk.CTkLabel(self, text="SAMSUNG USB DRIVERS", font=("Segoe UI", 26, "bold"), text_color="#00E5FF")
        self.label.pack(pady=(30, 5))

        self.sub_label = ctk.CTkLabel(self, text="Lead Developer: Ahmed Younis", font=("Segoe UI", 12, "bold"), text_color="#FFD700")
        self.sub_label.pack(pady=5)

        self.status_frame = ctk.CTkFrame(self, width=450, height=80, fg_color="#12121c", corner_radius=10, border_width=1, border_color="#00E5FF")
        self.status_frame.pack(pady=(20, 10))
        self.status_frame.pack_propagate(False)

        self.status_label = ctk.CTkLabel(self.status_frame, text="Ready To Install", font=("Consolas", 12, "bold"), text_color="#A0A0B0")
        self.status_label.pack(expand=True)

        self.progress = ctk.CTkProgressBar(self, width=450, height=8, progress_color="#00E5FF", fg_color="#1a1a24")
        self.progress.set(0)
        self.progress.pack(pady=15)

        self.install_btn = ctk.CTkButton(self, text="Install Drivers", command=self.start_thread,
                                        fg_color="transparent", hover_color="#003344", border_width=2,
                                        border_color="#00E5FF", text_color="#00E5FF", font=("Segoe UI", 14, "bold"),
                                        corner_radius=8, width=250, height=40)
        self.install_btn.pack(pady=10)

        self.footer = ctk.CTkLabel(self, text="EKO FLASH PRO SYSTEM \u00A9 2026", font=("Segoe UI", 10), text_color="#444455")
        self.footer.pack(side="bottom", pady=10)

        self.animation_running = False

    def animate_status(self, dots=0):
        if not self.animation_running:
            return
        dots = (dots + 1) % 4
        text = f"Installing{'.' * dots}"
        self.status_label.configure(text=text, text_color="#FFD700")
        self.after(400, self.animate_status, dots)

    def start_thread(self):
        self.install_btn.configure(state="disabled", text="Please Wait...")
        self.progress.start()
        self.animation_running = True
        self.animate_status()
        threading.Thread(target=self.run_installation, daemon=True).start()

    def run_installation(self):
        time.sleep(1.5)

        is_64bit = platform.machine().endswith('64')
        installer_file = "installer_x64.exe" if is_64bit else "installer_x86.exe"
        
        setup_path = get_resource_path(installer_file)

        if not is_admin():
            self.finalize_ui("Error: Admin Rights Required", "#FF3333", 0)
            return

        if os.path.exists(setup_path):
            try:
                subprocess.run([setup_path, "/S", "/v/qn"])
                self.finalize_ui("Success: Drivers Installed", "#00FF7F", 1)
            except Exception:
                self.finalize_ui("Error: Installation Failed", "#FF3333", 0)
        else:
            self.finalize_ui(f"Error: Missing Component ({installer_file})", "#FF3333", 0)

    def finalize_ui(self, message, color, progress_val):
        self.animation_running = False
        self.progress.stop()
        self.progress.set(progress_val)
        self.status_label.configure(text=message, text_color=color)
        
        btn_hover = "#330000" if color == "#FF3333" else "#003311"
        self.install_btn.configure(state="normal", text="Exit", command=self.quit,
                                   border_color=color, text_color=color, hover_color=btn_hover)

if __name__ == "__main__":
    app = InstallerApp()
    app.mainloop()
