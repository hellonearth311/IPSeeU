import threading
import sys
import os

from customtkinter import *
from scan import _scan_devices, _lookup_vendor

def add_to_text_window(text):
    scanInfoTextWindow.configure(state="normal")
    scanInfoTextWindow.insert("end", text + "\n")
    scanInfoTextWindow.configure(state="disabled")

def print_devices(devices):
    if not devices:
        add_to_text_window("No devices found.")
        return
    add_to_text_window("\n{:<18} {:<20} {:<30}".format("IP Address", "MAC Address", "Vendor"))
    add_to_text_window("-"*70)
    for device in devices:
        add_to_text_window("{:<18} {:<20} {:<30}".format(device.get("ip","-"), device.get("mac","-"), device.get("vendor","Unknown")))
    add_to_text_window("\n")

def scan_with_ui(callback=None):
    def worker():
        add_to_text_window("Scanning devices...")
        scanStatusLabel.configure(text="Scanning...")

        devices = _scan_devices()
        add_to_text_window(f"{len(devices)} devices found! Looking up MAC vendors...")

        for i in range(len(devices)):
            devices[i]["vendor"] = _lookup_vendor(devices[i]["mac"])
        add_to_text_window("MAC Vendors found successfully!")

        print(devices)
        add_to_text_window(f"Scan successful!")

        scanStatusLabel.configure(text="Scan successful!", text_color="#90EE90")

        print_devices(devices)
        if callback:
            callback(devices)
    threading.Thread(target=worker, daemon=True).start()


root = CTk()
root.title("IPSeeU")
root.geometry("900x700")

def set_app_icon(window):
    if sys.platform.startswith("win"):
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
        if os.path.exists(icon_path):
            window.iconbitmap(icon_path)
    elif sys.platform == "darwin" or sys.platform.startswith("linux"):
        try:
            from tkinter import PhotoImage
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.png")
            if os.path.exists(icon_path):
                img = PhotoImage(file=icon_path)
                window.wm_iconphoto(True, img)
        except Exception:
            pass

set_app_icon(root)

set_default_color_theme("green")
set_appearance_mode("dark")

titleText = CTkLabel(root, text="IPSeeU", font=("poppins", 40))
titleText.place(relx=0.42, rely=0.05, anchor="nw")

scanStatusLabel = CTkLabel(root, text="Ready to scan", font=("poppins", 15), text_color='cyan')
scanStatusLabel.place(relx=0.4885, rely=0.13, anchor="center")

scanInfoTextWindow = CTkTextbox(
    root,
    state="disabled",
    width=700,
    height=400,
    fg_color="#181a1b",
    text_color="#25e022",
    font=("poppins", 13)
)
scanInfoTextWindow.place(relx=0.11, rely=0.22)

add_to_text_window("IPSeeU is ready to scan. Please press the scan button to begin.")

scanButton = CTkButton(root, text="Scan", font=("poppins", 15), command=scan_with_ui)
scanButton.place(relx=0.41, rely=0.9, anchor="nw")


root.mainloop()