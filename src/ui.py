from customtkinter import *
import threading
from datetime import datetime
from tkinter import messagebox
import platform

from scan import scan_network_no_root, get_local_subnet, get_mac_vendor

def import_custom_font(font_path, size):
    """Import a custom font for the UI"""
    try:
        custom_font = CTkFont(family=font_path, size=size)
        return custom_font
    except Exception as e:
        print(f"Error loading custom font: {e}")
        return None

def build_main_ui():
    """Build the main UI for the network scanner"""
    root = CTk()
    root.title("IPSeeU")
    root.geometry("700x700")

    try:
        if platform.system() == "Windows":
            root.iconbitmap("assets/img/icon.ico")
        else:
            from tkinter import PhotoImage
            icon_image = PhotoImage(file="assets/img/icon.png")
            root.iconphoto(False, icon_image)
    except Exception as e:
        print(f"Could not load application icon: {e}")

    poppins_font_title = import_custom_font("assets/fonts/Poppins.ttf", 30)
    poppins_font_body = import_custom_font("assets/fonts/Poppins.ttf", 18)

    frame = CTkFrame(root)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    label = CTkLabel(frame, text="IPSeeU", font=poppins_font_title)
    label.place(relx=0.5, rely=0.1, anchor="center")

    status_label = CTkLabel(frame, text="Ready to scan", font=poppins_font_body, text_color="#407DF0")
    status_label.place(relx=0.5, rely=0.2, anchor="center")

    results_text = CTkTextbox(frame, width=600, height=400, font=poppins_font_body)
    results_text.place(relx=0.5, rely=0.55, anchor="center")

    def scan_network_threaded():
        """Run network scan in a separate thread"""
        def scan_worker():
            try:
                # Update UI to show scanning status
                root.after(0, lambda: status_label.configure(text="Scanning network...", text_color="#407DF0"))
                root.after(0, lambda: scanButton.configure(state="disabled", text="Scanning..."))
                root.after(0, lambda: results_text.delete("1.0", "end"))
                
                # Get subnet and scan
                ip_range = get_local_subnet()
                # root.after(0, lambda: results_text.insert("end", f"Scanning subnet: {ip_range}\n\n"))
                root.after(0, lambda: results_text.insert("end", f"Scanning subnet: [REDACTED FOR DEVLOG]\n\n"))
                
                devices = scan_network_no_root(ip_range)
                
                # Update results in the main thread
                def update_results():
                    results_text.insert("end", f"Found {len(devices)} devices:\n")
                    results_text.insert("end", "-" * 50 + "\n")
                    
                    for device in devices:
                        vendor = get_mac_vendor(device['mac']) if device['mac'] != "Unknown" else "Unknown"
                        # results_text.insert("end", f"IP: {device['ip']:<15}\n")
                        results_text.insert("end", f"IP: [REDACTED FOR DEVLOG]\n")
                        results_text.insert("end", f"MAC: {device['mac']}\n")
                        results_text.insert("end", f"Vendor: {vendor}\n")
                        results_text.insert("end", "-" * 30 + "\n")
                    
                    status_label.configure(text=f"Scan complete - Found {len(devices)} devices", text_color="#90EE90")
                    scanButton.configure(state="normal", text="Scan Network")
                    exportButton.configure(state="normal")
                
                root.after(0, update_results)
                
            except Exception as e:
                # Handle errors in the main thread
                def show_error():
                    status_label.configure(text="Scan failed", text_color="#FF6B6B")
                    results_text.insert("end", f"Error during scan: {str(e)}\n")
                    scanButton.configure(state="normal", text="Scan Network")
                
                root.after(0, show_error)

        # Start the worker threads
        thread = threading.Thread(target=scan_worker, daemon=True)
        thread.start()
        
    def show_custom_message(title, message, is_success=True):
        """Create a custom CTk dialog"""
        dialog = CTkToplevel(root)
        dialog.title(title)
        dialog.geometry("350x150")
        dialog.resizable(False, False)
        
        # Center the dialog on parent window
        dialog.transient(root)
        dialog.grab_set()
        
        # Message label
        color = "#90EE90" if is_success else "#FF6B6B"
        msg_label = CTkLabel(dialog, text=message, wraplength=300, text_color=color)
        msg_label.pack(pady=30)
        
        # OK button
        ok_button = CTkButton(dialog, text="OK", command=dialog.destroy, width=100)
        ok_button.pack(pady=10)
        
    def export_results():
        try:
            today = datetime.now()
            date_str = today.strftime("%Y-%m-%d")
            time_str = today.strftime("%H-%M-%S")

            filename = f"ipseeu_export_{date_str}_{time_str}.txt"
            
            with open(filename, "x") as f:
                f.write(results_text.get(1.0, END))
            
            show_custom_message("Export Successful", f"Exported output to {filename}")
        except Exception as e:
            show_custom_message("Error Exporting", f"Error exporting data: {e}", False)


    scanButton = CTkButton(frame, text="Scan Network", command=scan_network_threaded)
    scanButton.place(relx=0.15, rely=0.95, anchor="center")

    exportButton = CTkButton(frame, text="Export Results", command=export_results, state="disabled")
    exportButton.place(relx=0.85, rely=0.95, anchor="center")

    settingsButton = CTkButton(frame, text="⛭", width=37, height=35, font=poppins_font_title)
    settingsButton.place(relx=0.95, rely=0.1, anchor="center")

    root.mainloop()