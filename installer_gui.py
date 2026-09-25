import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import shutil
import winreg

class AayuInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("AAYU Setup")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Style
        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
        
        # UI Elements
        ttk.Label(root, text="AAYU Compiler Setup", style="Header.TLabel").pack(pady=20)
        ttk.Label(root, text="This will install the AAYU compiler on your system.").pack(pady=10)
        
        self.add_to_path_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(root, text="Add AAYU to system PATH (Recommended)", variable=self.add_to_path_var).pack(pady=10)
        
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=20)
        
        self.install_btn = ttk.Button(root, text="Install Now", command=self.install)
        self.install_btn.pack(pady=10)
        
    def install(self):
        self.install_btn.config(state="disabled")
        self.progress["value"] = 20
        self.root.update_idletasks()
        
        try:
            # Source executable (bundled)
            if hasattr(sys, '_MEIPASS'):
                src_exe = os.path.join(sys._MEIPASS, "aayu.exe")
            else:
                # Fallback for testing uncompiled
                src_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist", "aayu.exe")
                
            if not os.path.exists(src_exe):
                messagebox.showerror("Error", f"Could not find compiler binary at {src_exe}")
                self.install_btn.config(state="normal")
                return
                
            # Dest
            user_profile = os.environ.get("USERPROFILE")
            aayu_dir = os.path.join(user_profile, ".aayu", "bin")
            os.makedirs(aayu_dir, exist_ok=True)
            dest_exe = os.path.join(aayu_dir, "aayu.exe")
            
            self.progress["value"] = 50
            self.root.update_idletasks()
            
            # Copy file
            shutil.copy2(src_exe, dest_exe)
            
            self.progress["value"] = 80
            self.root.update_idletasks()
            
            # Add to PATH
            if self.add_to_path_var.get():
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)
                    try:
                        path_val, _ = winreg.QueryValueEx(key, "Path")
                    except FileNotFoundError:
                        path_val = ""
                        
                    if aayu_dir not in path_val:
                        new_path = path_val + ";" + aayu_dir if path_val else aayu_dir
                        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                    winreg.CloseKey(key)
                    
                    # Broadcast WM_SETTINGCHANGE so some apps pick it up
                    import ctypes
                    HWND_BROADCAST = 0xFFFF
                    WM_SETTINGCHANGE = 0x001A
                    SMTO_ABORTIFHUNG = 0x0002
                    ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", SMTO_ABORTIFHUNG, 5000, None)
                except Exception as e:
                    print("Could not set path:", e)
            
            self.progress["value"] = 100
            self.root.update_idletasks()
            
            messagebox.showinfo("Success", "AAYU installed successfully!\n\nPlease restart your terminal or VS Code to use 'aayu'.")
            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror("Installation Failed", str(e))
            self.install_btn.config(state="normal")
            self.progress["value"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = AayuInstaller(root)
    root.mainloop()
