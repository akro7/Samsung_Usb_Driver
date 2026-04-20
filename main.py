import os
import sys
import subprocess
import ctypes
import threading
import platform
import customtkinter as ctk

# إعدادات المظهر
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

        self.title("EKO FLASH - Samsung Driver Installer")
        self.geometry("500x350")
        self.resizable(False, False)

        # العناوين والجماليات
        self.label = ctk.CTkLabel(self, text="SAMSUNG USB DRIVERS", font=("Orbitron", 22, "bold"), text_color="#3B8ED0")
        self.label.pack(pady=(20, 10))

        self.sub_label = ctk.CTkLabel(self, text="Lead Developer: Ahmed Younis\nCo-Developer: Omar Hesham", font=("Segoe UI", 12))
        self.sub_label.pack(pady=5)

        # حالة التثبيت
        self.status_label = ctk.CTkLabel(self, text="Ready to Install", text_color="gray")
        self.status_label.pack(pady=(20, 5))

        # شريط التقدم
        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.set(0)
        self.progress.pack(pady=10)

        # أزرار التحكم
        self.install_btn = ctk.CTkButton(self, text="START INSTALLATION", command=self.start_thread, 
                                        fg_color="#1f538d", hover_color="#14375e", font=("Segoe UI", 14, "bold"))
        self.install_btn.pack(pady=20)

        self.footer = ctk.CTkLabel(self, text="Status: Waiting for user...", font=("Segoe UI", 10), text_color="#555")
        self.footer.pack(side="bottom", pady=10)

    def start_thread(self):
        # تشغيل التثبيت في خلفية منفصلة لضمان استجابة الواجهة
        self.install_btn.configure(state="disabled")
        self.status_label.configure(text="Installing... Please wait", text_color="#FFCC00")
        self.progress.start()
        threading.Thread(target=self.run_installation, daemon=True).start()

    def run_installation(self):
        # تحديد ملف التثبيت بناءً على معمارية الجهاز (64 أو 86) من واقع ملفاتك
        is_64bit = platform.machine().endswith('64')
        installer_file = "installer_x64.exe" if is_64bit else "installer_x86.exe"
        
        # المسار الصحيح للملف داخل مجلد DriverUsb
        setup_path = get_resource_path(os.path.join("DriverUsb", installer_file))

        if not is_admin():
            self.update_ui("Error: Admin Rights Required!", "#FF3333")
            return

        if os.path.exists(setup_path):
            try:
                # تشغيل التثبيت الصامت باستخدام الوسائط القياسية لتعريفات سامسونج
                subprocess.run([setup_path, "/S"], check=True)
                self.update_ui("SUCCESS: Drivers Installed!", "#00FF7F")
            except Exception:
                self.update_ui("Installation Failed!", "#FF3333")
        else:
            self.update_ui(f"File Not Found: {installer_file}", "#FF3333")

    def update_ui(self, message, color):
        self.progress.stop()
        self.progress.set(1)
        self.status_label.configure(text=message, text_color=color)
        self.footer.configure(text="Operation Finished.")
        self.install_btn.configure(state="normal", text="EXIT", command=self.quit)

if __name__ == "__main__":
    app = InstallerApp()
    app.mainloop()
