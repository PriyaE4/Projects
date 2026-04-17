"""
CyberShield - Malicious Website Blocker
Enhanced GUI with Cybersecurity Theme
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os, threading, random, string, json, webbrowser, time, platform, re, subprocess, sys
import math
import ipaddress
import ssl
import socket
import argparse
from collections import Counter, defaultdict
from datetime import datetime, date

from urllib.parse import urlparse, parse_qsl
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

try:
    import whois as whois_lib
except Exception:
    whois_lib = None

# ---------------- CONFIG ----------------
DATA_FILE = "blocked_sites.json"
try:
    _APP_DIR = os.path.dirname(os.path.abspath(__file__))
except Exception:
    _APP_DIR = os.getcwd()

EXTENSION_STATUS_FILE = os.path.join(_APP_DIR, "cybershield_extension_status.json")
EXTENSION_ACTIVE_WINDOW_SECONDS = 25
CYBERSHIELD_SERVICE_HOST = "127.0.0.1"
CYBERSHIELD_SERVICE_PORT = 8765

VT_API_KEY = os.environ.get("VT_API_KEY", "YOUR_VT_API_KEY")
MALWAREBAZAAR_KEY = os.environ.get("MBZ_AUTH_KEY", "YOUR_MALWAREBAZAAR_API_KEY")
GMAIL_ADDRESS = os.environ.get("BLOCKER_EMAIL", "YOUR_GMAIL")
APP_PASSWORD = os.environ.get("BLOCKER_PASS", "YOUR_GMAIL_APP_PASSWORD")

OPENPHISH_FEED_URL = "[openphish.com](https://openphish.com/feed.txt)"
_OPENPHISH_CACHE = {"fetched_at": 0, "entries": set()}
OPENPHISH_TTL_SECONDS = 60 * 60 * 6

# ================= CYBER THEME COLORS =================
COLORS = {
    'bg_dark': '#0a0a0f',
    'bg_medium': '#12121a',
    'bg_light': '#1a1a2e',
    'bg_card': '#16213e',
    'accent_cyan': '#00f5ff',
    'accent_green': '#00ff88',
    'accent_red': '#ff0055',
    'accent_orange': '#ff8c00',
    'accent_purple': '#bf00ff',
    'text_primary': '#ffffff',
    'text_secondary': '#8892b0',
    'text_muted': '#495670',
    'glow_cyan': '#00f5ff',
    'glow_green': '#00ff88',
    'border': '#233554',
    'success': '#00ff88',
    'warning': '#ffaa00',
    'danger': '#ff0055',
    'matrix_green': '#00ff41',
}

# ================= SPLASH SCREEN =================
class SplashScreen(tk.Toplevel):
    """Animated cybersecurity-themed splash screen"""
    
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.parent = parent
        
        # Window setup
        self.overrideredirect(True)
        self.configure(bg=COLORS['bg_dark'])
        
        # Center on screen
        width, height = 800, 500
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Make window appear on top
        self.attributes('-topmost', True)
        self.lift()
        
        # Animation variables
        self.matrix_chars = []
        self.glow_phase = 0
        self.title_alpha = 0
        self.tagline_index = 0
        self.shield_pulse = 0
        self.particles = []
        
        # Create canvas for animations
        self.canvas = tk.Canvas(
            self, 
            width=width, 
            height=height, 
            bg=COLORS['bg_dark'],
            highlightthickness=0
        )
        self.canvas.pack(fill='both', expand=True)
        
        # Initialize matrix rain
        self._init_matrix_rain()
        
        # Initialize particles
        self._init_particles()
        
        # Start animations
        self._animate_matrix()
        self._animate_main()
        
        # Schedule transition
        self.after(4500, self._fade_out)


# ================= UI HELPERS =================
class ScrollableFrame(tk.Frame):
    def __init__(self, parent, bg, *args, **kwargs):
        super().__init__(parent, bg=bg, *args, **kwargs)
        self._bg = bg

        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.v_scroll = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set)

        self.v_scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner = tk.Frame(self.canvas, bg=bg)
        self._window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>", self._on_inner_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self._bind_mousewheel(self.canvas)
        self._bind_mousewheel(self.inner)

    def _on_inner_configure(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfigure(self._window, width=event.width)

    def _bind_mousewheel(self, widget):
        widget.bind("<Enter>", lambda _e: self._set_mousewheel(True))
        widget.bind("<Leave>", lambda _e: self._set_mousewheel(False))

    def _set_mousewheel(self, enabled):
        if enabled:
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
        else:
            try:
                self.canvas.unbind_all("<MouseWheel>")
            except Exception:
                pass

    def _on_mousewheel(self, event):
        try:
            delta = int(-1 * (event.delta / 120))
        except Exception:
            delta = 0
        if delta:
            try:
                target = self.winfo_containing(event.x_root, event.y_root)
            except Exception:
                target = None

            try:
                if target is not None:
                    cls = target.winfo_class()
                    if cls in {"Treeview", "Text", "Listbox"}:
                        target.yview_scroll(delta, "units")
                        return "break"
            except Exception:
                pass

            self.canvas.yview_scroll(delta, "units")
    
    def _init_matrix_rain(self):
        """Initialize matrix-style falling characters"""
        chars = "01アイウエオカキクケコサシスセソタチツテト"
        for i in range(40):
            x = random.randint(0, 800)
            y = random.randint(-500, 0)
            speed = random.uniform(3, 8)
            char = random.choice(chars)
            opacity = random.randint(30, 100)
            self.matrix_chars.append({
                'x': x, 'y': y, 'speed': speed, 
                'char': char, 'opacity': opacity
            })
    
    def _init_particles(self):
        """Initialize floating particles"""
        for _ in range(30):
            self.particles.append({
                'x': random.randint(0, 800),
                'y': random.randint(0, 500),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'size': random.randint(1, 3),
                'alpha': random.randint(50, 150)
            })
    
    def _animate_matrix(self):
        """Animate matrix rain effect"""
        if not self.winfo_exists():
            return
            
        # Update and draw matrix characters
        for char_data in self.matrix_chars:
            char_data['y'] += char_data['speed']
            if char_data['y'] > 500:
                char_data['y'] = random.randint(-100, -10)
                char_data['x'] = random.randint(0, 800)
        
        self.after(50, self._animate_matrix)
    
    def _animate_main(self):
        """Main animation loop"""
        if not self.winfo_exists():
            return
            
        self.canvas.delete('all')
        
        # Draw matrix rain
        for char_data in self.matrix_chars:
            green_val = int(char_data['opacity'] * 2.55)
            color = f'#{0:02x}{green_val:02x}{int(green_val*0.3):02x}'
            self.canvas.create_text(
                char_data['x'], char_data['y'],
                text=char_data['char'],
                fill=color,
                font=('Consolas', 10)
            )
        
        # Draw particles
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            if p['x'] < 0 or p['x'] > 800:
                p['vx'] *= -1
            if p['y'] < 0 or p['y'] > 500:
                p['vy'] *= -1
            
            alpha = p['alpha']
            color = f'#{alpha:02x}{alpha:02x}{min(255, alpha + 50):02x}'
            self.canvas.create_oval(
                p['x'] - p['size'], p['y'] - p['size'],
                p['x'] + p['size'], p['y'] + p['size'],
                fill=color, outline=''
            )
        
        # Draw central dark overlay for text visibility
        self.canvas.create_rectangle(
            150, 100, 650, 400,
            fill=COLORS['bg_dark'],
            stipple='gray50',
            outline=''
        )
        
        # Animate glow effect
        self.glow_phase += 0.1
        glow_intensity = int((math.sin(self.glow_phase) + 1) * 40 + 175)
        
        # Draw shield icon with pulse
        self.shield_pulse += 0.15
        pulse_size = int(math.sin(self.shield_pulse) * 5 + 50)
        
        # Shield glow
        for i in range(3, 0, -1):
            glow_alpha = int(glow_intensity / (i + 1))
            glow_color = f'#00{glow_alpha:02x}{glow_alpha:02x}'
            self._draw_shield(400, 180, pulse_size + i * 8, glow_color)
        
        # Main shield
        self._draw_shield(400, 180, pulse_size, COLORS['accent_cyan'])
        
        # Draw "CYBERSHIELD" title with glow
        title_y = 280
        
        # Glow layers
        for i in range(4, 0, -1):
            glow_alpha = int(glow_intensity / (i + 1))
            self.canvas.create_text(
                400, title_y,
                text="CYBERSHIELD",
                font=('Orbitron', 48, 'bold') if self._font_exists('Orbitron') else ('Impact', 48, 'bold'),
                fill=f'#00{glow_alpha:02x}{glow_alpha:02x}'
            )
        
        # Main title
        self.canvas.create_text(
            400, title_y,
            text="CYBERSHIELD",
            font=('Orbitron', 48, 'bold') if self._font_exists('Orbitron') else ('Impact', 48, 'bold'),
            fill=COLORS['accent_cyan']
        )
        
        # Animated tagline (typewriter effect)
        tagline = "━━ Malicious Website Blocker ━━"
        self.tagline_index = min(self.tagline_index + 0.3, len(tagline))
        visible_tagline = tagline[:int(self.tagline_index)]
        
        self.canvas.create_text(
            400, 340,
            text=visible_tagline,
            font=('Consolas', 16),
            fill=COLORS['accent_green']
        )
        
        # Draw scanning line effect
        scan_y = (time.time() * 100) % 500
        self.canvas.create_line(
            0, scan_y, 800, scan_y,
            fill=COLORS['accent_cyan'],
            width=1,
            stipple='gray50'
        )
        
        # Loading indicator
        self._draw_loading_bar(400, 420, 200, 4)
        
        # Status text
        statuses = ["Initializing security protocols...", "Loading threat database...", 
                   "Configuring firewall...", "System ready..."]
        status_idx = min(int((time.time() * 0.5) % len(statuses)), len(statuses) - 1)
        self.canvas.create_text(
            400, 450,
            text=statuses[status_idx],
            font=('Consolas', 10),
            fill=COLORS['text_secondary']
        )
        
        self.after(30, self._animate_main)
    
    def _draw_shield(self, x, y, size, color):
        """Draw a shield icon"""
        points = [
            x, y - size,
            x + size * 0.8, y - size * 0.5,
            x + size * 0.8, y + size * 0.3,
            x, y + size,
            x - size * 0.8, y + size * 0.3,
            x - size * 0.8, y - size * 0.5,
        ]
        self.canvas.create_polygon(points, fill='', outline=color, width=3)
        
        # Inner check mark
        check_points = [
            x - size * 0.3, y,
            x - size * 0.1, y + size * 0.3,
            x + size * 0.4, y - size * 0.3
        ]
        self.canvas.create_line(check_points, fill=color, width=3)
    
    def _draw_loading_bar(self, x, y, width, height):
        """Draw animated loading bar"""
        progress = (time.time() % 4) / 4
        
        # Background
        self.canvas.create_rectangle(
            x - width/2, y - height/2,
            x + width/2, y + height/2,
            fill=COLORS['bg_light'],
            outline=COLORS['border']
        )
        
        # Progress
        progress_width = width * progress
        self.canvas.create_rectangle(
            x - width/2, y - height/2,
            x - width/2 + progress_width, y + height/2,
            fill=COLORS['accent_cyan'],
            outline=''
        )
    
    def _font_exists(self, font_name):
        """Check if a font exists"""
        try:
            import tkinter.font as tkfont
            return font_name in tkfont.families()
        except:
            return False
    
    def _fade_out(self):
        """Fade out and show login"""
        if not self.winfo_exists():
            return
        self.destroy()
        self.callback()


# Fix: Splash screen animation methods were accidentally placed under `ScrollableFrame`.
# Alias them back onto `SplashScreen` so the splash screen can run normally.
SplashScreen._init_matrix_rain = ScrollableFrame._init_matrix_rain
SplashScreen._init_particles = ScrollableFrame._init_particles
SplashScreen._animate_matrix = ScrollableFrame._animate_matrix
SplashScreen._animate_main = ScrollableFrame._animate_main
SplashScreen._draw_shield = ScrollableFrame._draw_shield
SplashScreen._draw_loading_bar = ScrollableFrame._draw_loading_bar
SplashScreen._font_exists = ScrollableFrame._font_exists
SplashScreen._fade_out = ScrollableFrame._fade_out


# ================= MODERN DIALOGS (CYBER THEMED) =================
class CyberDialog(tk.Toplevel):
    """Base class for cyber-themed dialogs"""
    
    def __init__(self, parent, title="Dialog", width=500, height=300):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.configure(bg=COLORS['bg_dark'])
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Center on parent
        self.update_idletasks()
        try:
            x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
            y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
            self.geometry(f"+{x}+{y}")
        except:
            pass
        
        self.result = None
        
        # Add border effect
        self.configure(highlightbackground=COLORS['accent_cyan'], highlightthickness=2)
    
    def create_header(self, icon, title):
        """Create styled header"""
        header = tk.Frame(self, bg=COLORS['bg_card'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Accent line
        accent = tk.Frame(header, bg=COLORS['accent_cyan'], height=3)
        accent.pack(fill='x', side='top')
        
        content = tk.Frame(header, bg=COLORS['bg_card'])
        content.pack(fill='both', expand=True)
        
        tk.Label(
            content, text=icon, 
            bg=COLORS['bg_card'], 
            fg=COLORS['accent_cyan'],
            font=('Segoe UI', 28)
        ).pack(side='left', padx=20, pady=10)
        
        tk.Label(
            content, text=title,
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            font=('Segoe UI', 16, 'bold')
        ).pack(side='left', pady=10)
    
    def create_cyber_button(self, parent, text, command, style='primary', width=12):
        """Create cyber-themed button"""
        colors = {
            'primary': {'bg': COLORS['accent_cyan'], 'hover': '#00c4cc', 'fg': COLORS['bg_dark']},
            'success': {'bg': COLORS['accent_green'], 'hover': '#00cc66', 'fg': COLORS['bg_dark']},
            'danger': {'bg': COLORS['accent_red'], 'hover': '#cc0044', 'fg': COLORS['text_primary']},
            'secondary': {'bg': COLORS['bg_light'], 'hover': COLORS['bg_card'], 'fg': COLORS['text_primary']},
        }
        c = colors.get(style, colors['primary'])
        
        btn_frame = tk.Frame(parent, bg=c['bg'], padx=2, pady=2)
        
        btn = tk.Button(
            btn_frame, text=text, command=command,
            bg=c['bg'], fg=c['fg'],
            font=('Segoe UI', 11, 'bold'),
            borderwidth=0, padx=20, pady=10,
            cursor='hand2', relief='flat',
            width=width,
            activebackground=c['hover'],
            activeforeground=c['fg']
        )
        btn.pack()
        
        def on_enter(e):
            btn.config(bg=c['hover'])
            btn_frame.config(bg=c['hover'])
        
        def on_leave(e):
            btn.config(bg=c['bg'])
            btn_frame.config(bg=c['bg'])
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn_frame


class CyberMessageBox(CyberDialog):
    """Cyber-themed message box"""
    
    def __init__(self, parent, title, message, icon='info', buttons=None):
        super().__init__(parent, title, 550, 320)
        
        if buttons is None:
            buttons = [('OK', 'primary')]
        
        icon_map = {
            'info': '🛡️',
            'warning': '⚠️',
            'error': '🚫',
            'success': '✅',
            'question': '❓',
            'security': '🔒'
        }
        display_icon = icon_map.get(icon.lower(), icon)
        
        self.create_header(display_icon, title)
        
        content = tk.Frame(self, bg=COLORS['bg_dark'])
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Message with cyber styling
        msg_frame = tk.Frame(content, bg=COLORS['bg_light'], padx=20, pady=15)
        msg_frame.pack(fill='x', pady=10)
        
        tk.Label(
            msg_frame, text=message,
            bg=COLORS['bg_light'],
            fg=COLORS['text_secondary'],
            font=('Consolas', 11),
            wraplength=450, justify='left'
        ).pack()
        
        btn_frame = tk.Frame(self, bg=COLORS['bg_dark'])
        btn_frame.pack(pady=20)
        
        for text, style in buttons:
            cmd = lambda t=text: self._on_click(t)
            btn = self.create_cyber_button(btn_frame, text, cmd, style)
            btn.pack(side='left', padx=8)
    
    def _on_click(self, text):
        self.result = text
        self.destroy()
    
    @staticmethod
    def show(parent, title, message, icon='info', buttons=None):
        dialog = CyberMessageBox(parent, title, message, icon, buttons)
        dialog.wait_window()
        return dialog.result


class CyberInputDialog(CyberDialog):
    """Cyber-themed input dialog"""
    
    def __init__(self, parent, title, message, icon='📝', show_char=None, default=''):
        super().__init__(parent, title, 550, 350)
        self.create_header(icon, title)
        
        content = tk.Frame(self, bg=COLORS['bg_dark'])
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        tk.Label(
            content, text=message,
            bg=COLORS['bg_dark'],
            fg=COLORS['text_secondary'],
            font=('Segoe UI', 11),
            wraplength=450, justify='left'
        ).pack(pady=(10, 20))
        
        # Cyber-styled input
        input_frame = tk.Frame(content, bg=COLORS['accent_cyan'], padx=2, pady=2)
        input_frame.pack(fill='x', pady=10)
        
        inner_frame = tk.Frame(input_frame, bg=COLORS['bg_light'])
        inner_frame.pack(fill='both', expand=True)
        
        self.entry = tk.Entry(
            inner_frame,
            bg=COLORS['bg_light'],
            fg=COLORS['text_primary'],
            font=('Consolas', 12),
            relief='flat',
            insertbackground=COLORS['accent_cyan'],
            show=show_char or ''
        )
        self.entry.pack(fill='x', padx=10, pady=12)
        self.entry.insert(0, default)
        self.entry.focus_set()
        self.entry.bind('<Return>', lambda e: self._on_ok())
        self.entry.bind('<Escape>', lambda e: self._on_cancel())
        
        btn_frame = tk.Frame(self, bg=COLORS['bg_dark'])
        btn_frame.pack(pady=20)
        
        self.create_cyber_button(btn_frame, 'Confirm', self._on_ok, 'success').pack(side='left', padx=8)
        self.create_cyber_button(btn_frame, 'Cancel', self._on_cancel, 'secondary').pack(side='left', padx=8)
    
    def _on_ok(self):
        self.result = self.entry.get()
        self.destroy()
    
    def _on_cancel(self):
        self.result = None
        self.destroy()
    
    @staticmethod
    def show(parent, title, message, icon='📝', show_char=None, default=''):
        dialog = CyberInputDialog(parent, title, message, icon, show_char, default)
        dialog.wait_window()
        return dialog.result


class CyberListDialog(CyberDialog):
    """Cyber-themed list dialog"""
    
    def __init__(self, parent, title, message, items, icon='📋'):
        height = min(550, 280 + len(items) * 25)
        super().__init__(parent, title, 600, height)
        self.create_header(icon, title)
        
        if message:
            msg_frame = tk.Frame(self, bg=COLORS['bg_dark'])
            msg_frame.pack(fill='x', padx=30, pady=(15, 5))
            tk.Label(
                msg_frame, text=message,
                bg=COLORS['bg_dark'],
                fg=COLORS['text_secondary'],
                font=('Segoe UI', 11),
                wraplength=520
            ).pack()
        
        # List with cyber styling
        list_frame = tk.Frame(self, bg=COLORS['accent_cyan'], padx=2, pady=2)
        list_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        inner = tk.Frame(list_frame, bg=COLORS['bg_light'])
        inner.pack(fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(inner, bg=COLORS['bg_card'])
        scrollbar.pack(side='right', fill='y')
        
        self.listbox = tk.Listbox(
            inner,
            bg=COLORS['bg_light'],
            fg=COLORS['text_primary'],
            font=('Consolas', 10),
            relief='flat',
            selectbackground=COLORS['accent_cyan'],
            selectforeground=COLORS['bg_dark'],
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.listbox.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.config(command=self.listbox.yview)
        
        for item in items:
            self.listbox.insert(tk.END, item)
        
        btn_frame = tk.Frame(self, bg=COLORS['bg_dark'])
        btn_frame.pack(pady=15)
        self.create_cyber_button(btn_frame, 'Close', self.destroy, 'primary').pack()
    
    @staticmethod
    def show(parent, title, message, items, icon='📋'):
        dialog = CyberListDialog(parent, title, message, items, icon)
        dialog.wait_window()


# Use the new cyber dialogs
ModernMessageBox = CyberMessageBox
ModernInputDialog = CyberInputDialog
ModernListDialog = CyberListDialog


# ================= UTILITIES =================
LOG_FILE = "security_log.txt"
USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_user_role(email):
    users = load_users()
    user = users.get(email.lower())
    if not user:
        return "viewer"
    return user.get("role", "viewer")

def authenticate_admin(email, password):
    users = load_users()
    user = users.get(email.lower())
    if not user:
        return False
    if user.get("role") != "admin":
        return False
    return user.get("password") == password

def export_pdf_report(path, blocked_sites):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(path)
    content = []
    content.append(Paragraph("<b>CyberShield - Blocked Websites Report</b>", styles["Title"]))
    for dom, info in blocked_sites.items():
        text = f"""
        <b>Domain:</b> {dom}<br/>
        <b>Date Blocked:</b> {info.get('date')}<br/>
        <b>Threat Score:</b> {info.get('score')}<br/>
        <b>Risk Level:</b> {info.get('risk')}<br/>
        <b>Blocked By:</b> {info.get('email')}<br/>
        <b>Reason:</b> {info.get('reason')}<br/><br/>
        """
        content.append(Paragraph(text, styles["Normal"]))
    doc.build(content)

def export_txt_report(path, blocked_sites):
    with open(path, "w", encoding="utf-8") as f:
        f.write("CyberShield - Blocked Websites Report\n")
        f.write("=" * 50 + "\n\n")
        for dom, info in blocked_sites.items():
            f.write(f"Domain      : {dom}\n")
            f.write(f"Date Blocked: {info.get('date')}\n")
            f.write(f"Threat Score: {info.get('score')}\n")
            f.write(f"Risk Level  : {info.get('risk')}\n")
            f.write(f"Blocked By  : {info.get('email')}\n")
            f.write(f"Reason      : {info.get('reason')}\n")
            f.write("-" * 50 + "\n")

def export_csv_report(path, blocked_sites):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Domain", "Date Blocked", "Threat Score", "Risk Level", "Blocked By", "Reason"])
        for dom, info in blocked_sites.items():
            writer.writerow([dom, info.get("date"), info.get("score"), info.get("risk"), info.get("email"), info.get("reason")])

def write_security_log(action, domain_or_url, email=None, score=None, risk=None, sources=None):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "time": timestamp,
        "action": action,
        "target": domain_or_url,
        "email": email if email else "N/A",
        "score": score if score is not None else "N/A",
        "risk": risk if risk else "N/A",
        "sources": ",".join(sources) if sources else "None"
    }
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(
                f"[{timestamp}] ACTION={action} TARGET={domain_or_url} "
                f"EMAIL={log_entry['email']} SCORE={log_entry['score']} "
                f"RISK={log_entry['risk']} SOURCES={log_entry['sources']}\n"
            )
    except Exception:
        pass
    return log_entry

def load_blocked_sites():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
                else:
                    return {site: {"status": "blocked", "password": None, "email": None} for site in data}
        except Exception:
            return {}
    return {}

def save_blocked_sites(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def random_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def random_code(length=6):
    return ''.join(random.choice(string.digits) for _ in range(length))

def normalize_raw_url(raw):
    raw = (raw or "").strip()
    if not raw:
        return None, None
    if not raw.startswith(("http://", "https://")):
        raw = "http://" + raw
    p = urlparse(raw)
    if not p.netloc:
        return None, None
    domain = p.netloc.lower().split(":")[0]
    if domain.startswith("www."):
        domain = domain[4:]
    return raw, domain

def get_hosts_path():
    system = platform.system()
    if system == "Windows":
        return r"C:\Windows\System32\drivers\etc\hosts"
    elif system in ("Linux", "Darwin"):
        return "/etc/hosts"
    else:
        raise RuntimeError("Unsupported OS")

def add_host_entry(domain):
    hosts = get_hosts_path()
    with open(hosts, "r", encoding="utf-8") as fh:
        content = fh.read()
    if domain.lower() in content.lower():
        return False
    with open(hosts, "a", encoding="utf-8") as fh:
        if not content.endswith("\n"):
            fh.write("\n")
        fh.write(f"127.0.0.1 {domain}\n127.0.0.1 www.{domain}\n")
    return True

def remove_host_entry(domain):
    hosts = get_hosts_path()
    with open(hosts, "r", encoding="utf-8") as fh:
        lines = fh.readlines()
    kept = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 2 and not parts[0].startswith("#"):
            tokens = [p.lower() for p in parts[1:]]
            if domain.lower() in tokens or ("www." + domain.lower()) in tokens:
                continue
        kept.append(line)
    with open(hosts, "w", encoding="utf-8") as fh:
        fh.writelines(kept)


# ================= EMAIL FUNCTIONS =================
def is_email_configured():
    if not GMAIL_ADDRESS or "@gmail.com" not in GMAIL_ADDRESS.lower():
        return False
    if not APP_PASSWORD or len(APP_PASSWORD.replace(" ", "")) < 8:
        return False
    return True

def configure_email_interactive():
    root = tk.Tk()
    root.withdraw()
    msg = (
        "Email Configuration Required\n\n"
        "This application needs Gmail credentials to send verification codes.\n\n"
        "Steps to get Gmail App Password:\n"
        "1. Go to: [myaccount.google.com](https://myaccount.google.com/apppasswords\n)"
        "2. Enable 2-Factor Authentication (if not already)\n"
        "3. Create an app password for 'Mail'\n"
        "4. Copy the 16-character password\n\n"
        "Do you want to configure email now?"
    )
    if messagebox.askyesno("Email Configuration", msg):
        email = simpledialog.askstring("Enter Gmail Address", "Enter your Gmail address:", parent=root)
        if email and "@gmail.com" in email.lower():
            app_pwd = simpledialog.askstring("Enter App Password", "Enter your Gmail App Password\n(16 characters, no spaces):", show="*", parent=root)
            if app_pwd:
                app_pwd = app_pwd.replace(" ", "")
                success, msg = send_email_single(email, "CyberShield - Test Email", "This is a test email from CyberShield.\n\nYour email is configured correctly!", test_email=email, test_password=app_pwd)
                if success:
                    messagebox.showinfo("Success", f"Email configured successfully!\n\nTest email sent to: {email}\n\nTo make this permanent, set environment variables:\nBLOCKER_EMAIL={email}\nBLOCKER_PASS={app_pwd}")
                    root.destroy()
                    return email, app_pwd
                else:
                    messagebox.showerror("Configuration Failed", f"Failed to send test email:\n\n{msg}")
    root.destroy()
    return None, None

def send_email_single(recipient, subject, body, test_email=None, test_password=None):
    if not recipient or "@" not in recipient:
        return False, "Invalid recipient email"
    email_addr = test_email if test_email else GMAIL_ADDRESS
    email_pass = test_password if test_password else APP_PASSWORD
    if not email_addr or "@" not in email_addr:
        return False, "Email address not configured"
    if not email_pass or len(email_pass) < 8:
        return False, "App password not configured"
    try:
        msg = MIMEMultipart()
        msg["From"] = email_addr
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=20)
        server.starttls()
        server.login(email_addr, email_pass)
        server.send_message(msg)
        server.quit()
        return True, "Email sent successfully"
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed!"
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

def send_verification_code(email, purpose="unblock"):
    code = random_code(6)
    subject = f"CyberShield - Verification Code for {purpose.title()}"
    body = f"Your one-time verification code for {purpose} operation is:\n\n{code}\n\nThis code is valid for a short time."
    success, msg = send_email_single(email, subject, body)
    if success:
        return True, code
    return False, msg


# ================= THREAT CHECKS =================
PHISHING_KEYWORDS = ["login", "verify", "secure", "account", "update", "signin", "password", "bank", "wallet", "confirm"]
PHISHING_SUSPICIOUS_TLDS = {"zip", "mov", "xyz", "top", "icu", "click", "link", "rest", "country", "gq", "tk", "ml", "cf", "ga", "cam", "work", "support", "live", "quest", "party", "loan", "biz", "info"}
PHISHING_BRAND_KEYWORDS = {"google", "gmail", "microsoft", "office", "outlook", "live", "apple", "icloud", "amazon", "paypal", "chase", "wellsfargo", "boa", "bank", "secure", "login", "verify", "account", "facebook", "instagram", "meta", "whatsapp", "telegram", "twitter", "x", "netflix", "spotify", "adobe", "steam", "discord", "coinbase", "binance", "dropbox", "onedrive", "paypal", "paypa1", "crypto", "billing", "invoice"}
PHISHING_SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly", "rb.gy", "ow.ly", "buff.ly", "shorte.st", "tiny.cc"}
PHISHING_REDIRECT_PARAMS = {"url", "u", "redirect", "redirect_url", "redir", "next", "continue", "return", "returnurl", "dest", "destination", "target", "to"}
PHISHING_SENSITIVE_TOKENS = {"otp", "2fa", "mfa", "passcode", "token", "reset", "unlock", "recovery", "billing", "payment", "invoice", "kyc", "wallet", "crypto", "seed"}
PHISHING_EXECUTABLE_EXTENSIONS = {".exe", ".scr", ".zip", ".rar", ".msi", ".bat", ".cmd", ".js", ".vbs"}
PHISHING_CANONICAL_BRANDS = {"google", "microsoft", "apple", "amazon", "paypal", "facebook", "instagram", "netflix", "adobe", "dropbox", "coinbase", "binance", "bankofamerica", "wellsfargo", "chase", "icloud", "outlook", "gmail"}
PHISHING_LEGIT_BRAND_DOMAINS = {"google": {"google.com"}, "microsoft": {"microsoft.com"}, "apple": {"apple.com"}, "amazon": {"amazon.com"}, "paypal": {"paypal.com"}, "facebook": {"facebook.com"}, "instagram": {"instagram.com"}, "netflix": {"netflix.com"}, "adobe": {"adobe.com"}, "dropbox": {"dropbox.com"}, "coinbase": {"coinbase.com"}, "binance": {"binance.com"}, "bankofamerica": {"bankofamerica.com"}, "wellsfargo": {"wellsfargo.com"}, "chase": {"chase.com"}, "icloud": {"icloud.com"}, "outlook": {"outlook.com"}, "gmail": {"gmail.com"}}
WHOIS_CACHE_TTL_SECONDS = 60 * 60 * 24
_WHOIS_CACHE = {}
HIGH_TRUST_BASE_DOMAINS = {"youtube.com", "google.com", "accounts.google.com", "microsoft.com", "apple.com", "github.com"}

def phishing_heuristic_check(url, domain):
    text = f"{url} {domain}".lower()
    hits = [kw for kw in PHISHING_KEYWORDS if kw in text]
    if hits:
        return "SUSPECT", hits
    return "CLEAN", []

def _label_entropy(label):
    if not label:
        return 0.0
    total = len(label)
    counts = Counter(label)
    entropy = 0.0
    for c in counts.values():
        p = c / total
        entropy -= p * math.log2(p)
    return entropy

def _normalize_leetspeak(text):
    table = str.maketrans({"0": "o", "1": "l", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s"})
    return text.translate(table)

def _is_one_edit_apart(a, b):
    if a == b:
        return False
    la, lb = len(a), len(b)
    if abs(la - lb) > 1:
        return False
    if la == lb:
        return sum(1 for i in range(la) if a[i] != b[i]) == 1
    if la < lb:
        a, b = b, a
        la, lb = lb, la
    i = j = edits = 0
    while i < la and j < lb:
        if a[i] == b[j]:
            i += 1
            j += 1
        else:
            edits += 1
            i += 1
            if edits > 1:
                return False
    return True

def _is_legit_brand_base_domain(normalized_base_domain, brand):
    allowed = PHISHING_LEGIT_BRAND_DOMAINS.get(brand, {f"{brand}.com"})
    return normalized_base_domain in allowed

def _coerce_to_datetime(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d-%b-%Y", "%Y.%m.%d", "%d.%m.%Y"):
            try:
                return datetime.strptime(value.strip(), fmt)
            except:
                continue
    return None

def _extract_creation_datetime(whois_data):
    creation = whois_data.get("creation_date") if isinstance(whois_data, dict) else getattr(whois_data, "creation_date", None)
    if isinstance(creation, list):
        candidates = [_coerce_to_datetime(v) for v in creation]
        candidates = [c for c in candidates if c is not None]
        return min(candidates) if candidates else None
    return _coerce_to_datetime(creation)

def _get_domain_age_days(domain):
    if not domain or whois_lib is None:
        return None
    now = time.time()
    cached = _WHOIS_CACHE.get(domain)
    if cached and now - cached["ts"] < WHOIS_CACHE_TTL_SECONDS:
        return cached["age_days"]
    try:
        data = whois_lib.whois(domain)
        created_at = _extract_creation_datetime(data)
        age_days = max(0, (datetime.utcnow() - created_at).days) if created_at else None
    except:
        age_days = None
    _WHOIS_CACHE[domain] = {"ts": now, "age_days": age_days}
    return age_days

def phishing_algorithm_check(url, domain):
    score = 0
    reasons = []
    reason_seen = set()

    def add(points, reason):
        nonlocal score
        if reason not in reason_seen:
            reason_seen.add(reason)
            reasons.append(reason)
            score += points

    text = (url or "").lower()
    dom = (domain or "").lower()
    normalized_text = _normalize_leetspeak(text)
    parsed = urlparse(text)
    host = (parsed.netloc or dom).lower().split("@")[-1].split(":")[0]
    path = (parsed.path or "").lower()
    query = (parsed.query or "").lower()
    scheme = (parsed.scheme or "").lower()

    keyword_hits = [kw for kw in PHISHING_KEYWORDS if kw in text]
    if keyword_hits:
        add(min(30, 6 * len(keyword_hits)), "keywords")
        if len(keyword_hits) >= 3:
            add(8, "keyword-cluster")

    labels = [p for p in host.split(".") if p]
    base_domain = ".".join(labels[-2:]) if len(labels) >= 2 else host
    normalized_base_domain = _normalize_leetspeak(base_domain)

    # Reduce false positives on highly trusted platforms that legitimately use
    # login/secure/account keywords and redirects (e.g., Gmail/Google).
    if base_domain in HIGH_TRUST_BASE_DOMAINS:
        return "CLEAN", 0, [], {}
    
    for brand in PHISHING_CANONICAL_BRANDS:
        if (brand in text or brand in normalized_text) and not _is_legit_brand_base_domain(normalized_base_domain, brand):
            add(18, f"brand-mismatch:{brand}")
            break

    for label in labels:
        clean_label = re.sub(r"[^a-z0-9]", "", label)
        if not clean_label:
            continue
        normalized = _normalize_leetspeak(clean_label)
        for brand in PHISHING_CANONICAL_BRANDS:
            if clean_label == brand:
                continue
            if normalized == brand or _is_one_edit_apart(normalized, brand) or (brand in normalized and not _is_legit_brand_base_domain(normalized_base_domain, brand)):
                add(20, f"typosquat:{brand}")
                break

    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host or ""):
        try:
            ip_obj = ipaddress.ip_address(host)
            add(25, "ip-host")
            if ip_obj.is_private or ip_obj.is_loopback:
                add(8, "private-or-loopback-ip")
        except:
            pass

    if "xn--" in host:
        add(18, "punycode")
    if any(ord(c) > 127 for c in host):
        add(12, "non-ascii-host")

    subdomain_count = max(0, len(labels) - 2)
    if subdomain_count >= 3:
        add(14, "many-subdomains")
    if subdomain_count >= 5:
        add(8, "excessive-subdomains")

    if len(labels) >= 1 and any(lb.startswith("-") or lb.endswith("-") for lb in labels):
        add(8, "invalid-label-shape")
    if "--" in host:
        add(6, "double-hyphen-host")
    if host.count(".") >= 4:
        add(8, "many-dot-levels")
    if any(len(lb) >= 25 for lb in labels):
        add(8, "long-label")
    for lb in labels:
        if len(lb) >= 12 and _label_entropy(lb) >= 3.6:
            add(10, "high-entropy-label")
            break

    if len(text) > 80:
        add(10, "long-url")
    if len(text) > 140:
        add(14, "very-long-url")
    if len(path) > 60:
        add(8, "long-path")
    if len(query) > 50:
        add(8, "long-query")

    if "@" in text:
        add(18, "at-symbol")
    if "//" in path:
        add(10, "double-slash-path")
    if "\\" in text:
        add(10, "backslash-obfuscation")
    percent_count = text.count("%")
    if percent_count >= 1:
        add(7, "url-encoding")
    if percent_count >= 6:
        add(8, "heavy-encoding")
    if text.count("-") >= 3:
        add(9, "many-hyphens")
    if text.count("-") >= 6:
        add(6, "excessive-hyphens")

    digit_ratio = sum(c.isdigit() for c in text) / max(1, len(text))
    if digit_ratio >= 0.2:
        add(8, "many-digits")
    if digit_ratio >= 0.3:
        add(8, "digit-heavy-url")

    query_pairs = parse_qsl(query, keep_blank_values=True)
    if query:
        param_count = len([p for p in query.split("&") if p])
        if param_count >= 4:
            add(8, "many-params")
        if param_count >= 8:
            add(6, "excessive-params")
    for k, v in query_pairs:
        lk, lv = (k or "").lower(), (v or "").lower()
        if lk in PHISHING_REDIRECT_PARAMS and ("http://" in lv or "https://" in lv or "%2f%2f" in lv):
            add(18, "redirect-param-chain")
            break
    if any(t in (path + " " + query) for t in PHISHING_SENSITIVE_TOKENS):
        add(8, "sensitive-token-presence")

    if any(tok in path for tok in ("webscr", "security-check", "recover", "sso", "auth")):
        add(8, "credential-harvest-pattern")
    if any(path.endswith(ext) for ext in PHISHING_EXECUTABLE_EXTENSIONS):
        add(16, "executable-download-path")

    if host and "." in host:
        tld = host.split(".")[-1]
        if tld in PHISHING_SUSPICIOUS_TLDS:
            add(12, f"suspicious-tld:{tld}")

    if host in PHISHING_SHORTENERS:
        add(12, "shortener")

    if text and scheme != "https":
        add(8, "no-https")
    if "https" in host and scheme != "https":
        add(10, "https-token-mismatch")
    if parsed.port and parsed.port not in (80, 443):
        add(8, "non-standard-port")

    domain_age_days = _get_domain_age_days(base_domain)
    if domain_age_days is not None:
        if domain_age_days < 30:
            add(22, f"new-domain:{domain_age_days}d")
        elif domain_age_days < 90:
            add(14, f"young-domain:{domain_age_days}d")
        elif domain_age_days < 180:
            add(8, f"recent-domain:{domain_age_days}d")

    score = min(score, 100)
    status = "SUSPECT" if score >= 35 else "CLEAN"
    return status, score, reasons, keyword_hits

def calculate_threat_score(vt, mb, op, uh, phishing_status=None, phishing_score=0, redirect_status="UNKNOWN", ssl_status="UNKNOWN"):
    score = 0
    sources = []
    if vt == "UNSAFE":
        score += 40
        sources.append("VirusTotal")
    if op == "UNSAFE":
        score += 30
        sources.append("OpenPhish")
    if uh == "UNSAFE":
        score += 30
        sources.append("URLHaus")
    if mb == "UNSAFE":
        score += 20
        sources.append("MalwareBazaar")
    if redirect_status == "UNSAFE":
        score += 15
        sources.append("Redirect-Chain")
    if ssl_status == "UNSAFE":
        score += 20
        sources.append("SSL-Certificate")
    if phishing_status == "SUSPECT":
        score += max(15, min(30, int(phishing_score)))
        sources.append("Phishing-Algorithm")
    elif int(phishing_score) >= 10:
        score += 8
        sources.append("Phishing-Algorithm")
    score = min(score, 100)
    if score >= 70:
        risk = "HIGH"
    elif score >= 40:
        risk = "MEDIUM"
    else:
        risk = "LOW"
    return score, risk, sources

def _base_domain_simple(domain):
    dom = (domain or "").strip().lower()
    if dom.startswith("www."):
        dom = dom[4:]
    labels = [p for p in dom.split(".") if p]
    return ".".join(labels[-2:]) if len(labels) >= 2 else dom

def vt_check_url(url):
    try:
        parsed = urlparse(url or "")
        host = (parsed.netloc or "").split("@")[-1].split(":")[0]
        if _base_domain_simple(host) in HIGH_TRUST_BASE_DOMAINS:
            return "SAFE"
    except:
        pass
    if not VT_API_KEY:
        try:
            r = requests.head(url, timeout=8, allow_redirects=True)
            return "SAFE" if r.status_code < 400 else "UNKNOWN"
        except:
            return "UNKNOWN"
    try:
        params = {"apikey": VT_API_KEY, "resource": url}
        r = requests.get("[virustotal.com](https://www.virustotal.com/vtapi/v2/url/report)", params=params, timeout=12)
        j = r.json()
        if j.get("response_code") == 1:
            return "UNSAFE" if j.get("positives", 0) > 0 else "SAFE"
        return "UNKNOWN"
    except:
        return "UNKNOWN"

def malwarebazaar_check_url(domain):
    if _base_domain_simple(domain) in HIGH_TRUST_BASE_DOMAINS:
        return "SAFE"
    try:
        endpoint = "[bazaar.abuse.ch](https://bazaar.abuse.ch/api/)"
        headers = {"Auth-Key": MALWAREBAZAAR_KEY} if MALWAREBAZAAR_KEY else {}
        data = {"query": "search", "search_term": domain}
        r = requests.post(endpoint, data=data, headers=headers, timeout=12)
        j = r.json()
        return "UNSAFE" if j.get("data") else "SAFE"
    except:
        return "UNKNOWN"

def _fetch_openphish_feed():
    now = time.time()
    if now - _OPENPHISH_CACHE["fetched_at"] < OPENPHISH_TTL_SECONDS and _OPENPHISH_CACHE["entries"]:
        return _OPENPHISH_CACHE["entries"]
    try:
        r = requests.get(OPENPHISH_FEED_URL, timeout=12)
        if r.status_code == 200:
            lines = [ln.strip() for ln in r.text.splitlines() if ln.strip()]
            _OPENPHISH_CACHE["entries"] = set(lines)
            _OPENPHISH_CACHE["fetched_at"] = now
            return _OPENPHISH_CACHE["entries"]
    except:
        pass
    return _OPENPHISH_CACHE.get("entries", set())

def openphish_check(url, domain):
    feed = _fetch_openphish_feed()
    if not feed:
        return "UNKNOWN"
    for f in feed:
        try:
            parsed = urlparse(f)
            feed_domain = parsed.netloc.lower()
            if feed_domain.startswith("www."):
                feed_domain = feed_domain[4:]
            if domain == feed_domain:
                return "UNSAFE"
        except:
            continue
    return "SAFE"

def urlhaus_check_host(domain):
    if _base_domain_simple(domain) in HIGH_TRUST_BASE_DOMAINS:
        return "SAFE"
    try:
        endpoint = "[urlhaus-api.abuse.ch](https://urlhaus-api.abuse.ch/v1/host/)"
        r = requests.post(endpoint, data={"host": domain}, timeout=10)
        j = r.json()
        url_count = int(j.get("url_count", 0)) if j.get("url_count") is not None else 0
        if "ok" in j.get("query_status", "").lower() and url_count > 0:
            return "UNSAFE"
        return "SAFE"
    except:
        return "UNKNOWN"

def redirect_chain_check(url, original_domain, max_hops=10):
    try:
        r = requests.get(url, timeout=12, allow_redirects=True)
        hops = len(r.history)
        final_url = r.url or url
        _, final_domain = normalize_raw_url(final_url)
        if hops > max_hops:
            return "UNSAFE", {"hops": hops, "final_domain": final_domain}
        if final_domain and original_domain:
            # Treat redirects within the same base domain as normal (mail.google.com -> accounts.google.com).
            if _base_domain_simple(final_domain) != _base_domain_simple(original_domain):
                return "UNSAFE", {"hops": hops, "final_domain": final_domain}
        return "SAFE", {"hops": hops, "final_domain": final_domain}
    except:
        return "UNKNOWN", {"hops": 0, "final_domain": None}

def ssl_certificate_check(domain):
    if not domain:
        return "UNKNOWN", {"days_left": None}
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=8) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
        not_after = cert.get("notAfter")
        if not not_after:
            return "UNKNOWN", {"days_left": None}
        expiry = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
        days_left = (expiry - datetime.utcnow()).days
        if days_left < 0:
            return "UNSAFE", {"days_left": days_left}
        if days_left < 15:
            return "UNSAFE", {"days_left": days_left}
        return "SAFE", {"days_left": days_left}
    except:
        return "UNKNOWN", {"days_left": None}


# ================= PROJECT INFO =================
def on_project_info():
    return
    html = """
    <html>
    <head>
        <style>
            body { font-family: 'Segoe UI', Arial, sans-serif; padding: 30px; background: linear-gradient(135deg, #0a0a0f 0%, #12121a 100%); color: white; }
            .container { max-width: 1000px; margin: 0 auto; background: rgba(22, 33, 62, 0.9); padding: 30px; border-radius: 15px; box-shadow: 0 0 40px rgba(0, 245, 255, 0.3); border: 1px solid #00f5ff; }
            h1 { font-size: 32px; margin-bottom: 10px; color: #00f5ff; text-align: center; text-shadow: 0 0 20px #00f5ff; }
            .subtitle { text-align: center; font-size: 16px; color: #00ff88; margin-bottom: 30px; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 20px; background: rgba(26, 26, 46, 0.8); border-radius: 8px; overflow: hidden; }
            th, td { border: 1px solid #233554; padding: 12px 15px; text-align: left; }
            th { background-color: #16213e; font-weight: bold; color: #00f5ff; }
            tr:hover { background-color: rgba(0, 245, 255, 0.1); }
            .section-title { font-size: 20px; font-weight: bold; margin-top: 30px; margin-bottom: 15px; color: #00f5ff; border-left: 4px solid #00f5ff; padding-left: 15px; }
            a { color: #00f5ff; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ CyberShield Project</h1>
            <p class="subtitle">━━ Malicious Website Blocker ━━</p>
            <p>Advanced security system designed to protect organizations from cyber threats by blocking malicious websites and preventing unauthorized access.</p>
            <div class="section-title">📋 Project Details</div>
            <table>
                <tr><th>Project Name</th><td>Blocking Malicious Websites</td></tr>
                <tr><th>Description</th><td>Advanced website blocker with password protection, email verification, and threat intelligence integration</td></tr>
            </table>
            <div class="section-title">👥 Development Team</div>
            <table>
                <tr><th>Name</th><th>Employee ID</th><th>Email</th></tr>
                <tr><td>Priyamvada Atmakuri</td><td>23wh1a05e4</td><td>23wh1a05e4@bvrithyderabad.edu.in</td></tr>
                <tr><td>J. Naga Ananya</td><td>23wh1a05e0</td><td>23wh1a05e0@bvrithyderabad.edu.in</td></tr>
                <tr><td>Akshaya Reddy Patlolla</td><td>23wh1a05e9</td><td>23wh1a05e9@bvrithyderabad.edu.in</td></tr>
            </table>
            <div class="section-title">🔧 Features</div>
            <table>
                <tr><th>Feature</th><th>Description</th></tr>
                <tr><td>Multi-Source Threat Checking</td><td>VirusTotal, MalwareBazaar, OpenPhish, URLhaus</td></tr>
                <tr><td>Password Protection</td><td>Secure blocking/unblocking with user-defined or auto-generated passwords</td></tr>
                <tr><td>Email Verification</td><td>Send verification codes and passwords via email</td></tr>
                <tr><td>Bulk Operations</td><td>Upload .txt files with multiple URLs</td></tr>
                <tr><td>Cyber-Themed UI</td><td>Dark theme with neon accents and interactive elements</td></tr>
            </table>
        </div>
    </body>
    </html>
    """
    path = "project_info.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    webbrowser.open("file://" + os.path.abspath(path))


# ================= MAIN APPLICATION CLASS =================
class WebsiteBlockerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CyberShield - Malicious Website Blocker")
        self.root.geometry("1000x700")
        self.root.configure(bg=COLORS['bg_dark'])
        
        # Hide main window initially
        self.root.withdraw()
        
        self.blocked_sites = load_blocked_sites()
        self.frames = {}
        self._last_uploaded_urls = []
        self.auto_block_enabled = tk.BooleanVar(value=False)
        self.threat_cache = {}
        self.current_user_email = None
        self.current_user_role = None
        self._current_frame_name = None
        self._service_proc = None
        self._ext_after_id = None
        self._ext_indicator_loop_running = False

        self._help_default = "Hover a button to see help. Click User Guide for full instructions."
        self._help_var = tk.StringVar(value=self._help_default)
        
        # Dashboard state
        self._dashboard_last_state = None
        self._dashboard_refresh_token = 0
        self._dashboard_data = None
        self._dashboard_data_loading = False
        self._dashboard_notebook = None
        self._dashboard_tabs = {}
        self._dashboard_tab_loading_labels = {}
        self._dashboard_rendered_tabs = set()
        self._dashboard_figures = []
        self._dashboard_canvases = []
        
        # Email config
        global GMAIL_ADDRESS, APP_PASSWORD
        self.email_configured = is_email_configured()
        
        if not self.email_configured:
            env_email = os.environ.get("BLOCKER_EMAIL")
            env_pass = os.environ.get("BLOCKER_PASS")
            if env_email and env_pass:
                GMAIL_ADDRESS = env_email
                APP_PASSWORD = env_pass
                self.email_configured = is_email_configured()
        
        # Show splash screen
        self.splash = SplashScreen(self.root, self._after_splash)

        try:
            self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        except Exception:
            pass
    
    def _after_splash(self):
        """Called after splash screen completes"""
        self.root.deiconify()
        self._configure_styles()
        self._build_login_frame()
        self._build_admin_auth_frame()
        self.show_frame("login")

    def _bind_help(self, widget, text):
        def on_enter(_e=None):
            try:
                self._help_var.set(text)
            except Exception:
                pass

        def on_leave(_e=None):
            try:
                self._help_var.set(self._help_default)
            except Exception:
                pass

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def _build_help_bar(self, parent):
        bar = tk.Frame(parent, bg=COLORS['bg_card'])
        tk.Label(
            bar,
            textvariable=self._help_var,
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary'],
            font=("Consolas", 10),
            anchor="w",
            padx=12,
            pady=6,
        ).pack(fill="x")
        return bar

    def _build_login_frame(self):
        if "login" in self.frames:
            return

        login = tk.Frame(self.root, bg=COLORS['bg_dark'])

        scroll = ScrollableFrame(login, bg=COLORS['bg_dark'])
        scroll.pack(side="top", fill="both", expand=True)
        content = scroll.inner

        self._build_help_bar(login).pack(side="bottom", fill="x")

        header = tk.Frame(content, bg=COLORS['bg_card'], height=110)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Frame(header, bg=COLORS['accent_cyan'], height=4).pack(fill="x")
        tk.Label(
            header,
            text="🔐 SECURE LOGIN",
            bg=COLORS['bg_card'],
            fg=COLORS['accent_cyan'],
            font=("Segoe UI", 20, "bold"),
        ).pack(pady=(20, 5))
        tk.Label(
            header,
            text="Enter your email to start a session (logged for security).",
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary'],
            font=("Consolas", 11),
        ).pack()

        spacer_top = tk.Frame(content, bg=COLORS['bg_dark'])
        spacer_top.pack(fill="both", expand=True)

        card = tk.Frame(content, bg=COLORS['bg_light'], padx=40, pady=35, width=640, height=260)
        card.pack_propagate(False)
        card.pack(padx=60, pady=25, anchor="center")

        spacer_bottom = tk.Frame(content, bg=COLORS['bg_dark'])
        spacer_bottom.pack(fill="both", expand=True)

        self._login_error = tk.StringVar(value="")
        tk.Label(
            card,
            textvariable=self._login_error,
            bg=COLORS['bg_light'],
            fg=COLORS['accent_red'],
            font=("Consolas", 10),
            justify="left",
        ).pack(fill="x", pady=(0, 10))

        tk.Label(
            card,
            text="Email",
            bg=COLORS['bg_light'],
            fg=COLORS['text_secondary'],
            font=("Consolas", 11, "bold"),
        ).pack(anchor="w")

        entry_border = tk.Frame(card, bg=COLORS['accent_cyan'], padx=2, pady=2)
        entry_border.pack(fill="x", pady=(6, 14))
        self._login_email_var = tk.StringVar(value="")
        email_entry = tk.Entry(
            entry_border,
            textvariable=self._login_email_var,
            bg=COLORS['bg_medium'],
            fg=COLORS['text_primary'],
            font=("Consolas", 12),
            borderwidth=0,
            insertbackground=COLORS['accent_cyan'],
        )
        email_entry.pack(fill="x", padx=1, pady=1, ipady=10)

        btn_row = tk.Frame(card, bg=COLORS['bg_light'])
        btn_row.pack(anchor="center", pady=(8, 0))

        login_btn = tk.Button(
            btn_row,
            text="LOGIN",
            bg=COLORS['accent_cyan'],
            fg=COLORS['bg_dark'],
            font=("Segoe UI", 11, "bold"),
            borderwidth=0,
            padx=30,
            pady=12,
            cursor="hand2",
            command=lambda: self._do_login(email_entry),
        )
        login_btn.pack(side="left", padx=6)
        self._bind_help(login_btn, "Start a session after entering your email.")

        exit_btn = tk.Button(
            btn_row,
            text="EXIT",
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary'],
            font=("Segoe UI", 11, "bold"),
            borderwidth=0,
            padx=25,
            pady=12,
            cursor="hand2",
            command=self.root.destroy,
        )
        exit_btn.pack(side="left", padx=6)
        self._bind_help(exit_btn, "Close CyberShield.")

        email_entry.focus_set()
        email_entry.bind("<Return>", lambda _e: self._do_login(email_entry))

        self.frames["login"] = login

    def _do_login(self, email_entry):
        email = (self._login_email_var.get() or "").strip().lower()
        self._login_error.set("")

        if not email or "@" not in email or "." not in email.split("@")[-1]:
            self._login_error.set("Enter a valid email address to continue.")
            try:
                email_entry.focus_set()
            except Exception:
                pass
            return

        if not self.email_configured:
            res = CyberMessageBox.show(
                self.root,
                "Security Configuration",
                "⚠️ Email is not configured.\n\n"
                "Email is required for verification codes.\n\n"
                "Configure it now?",
                "warning",
                [("Configure", "success"), ("Skip", "secondary")],
            )
            if res == "Configure":
                cfg_email, cfg_pwd = configure_email_interactive()
                if cfg_email and cfg_pwd:
                    global GMAIL_ADDRESS, APP_PASSWORD
                    GMAIL_ADDRESS = cfg_email
                    APP_PASSWORD = cfg_pwd
                    self.email_configured = True

        self.current_user_email = email
        self.current_user_role = get_user_role(self.current_user_email)

        if "main" not in self.frames:
            self._build_frames()

        self._apply_role_permissions()
        self._help_var.set(self._help_default)
        self.show_frame("main")

    def logout(self):
        self.current_user_email = None
        self.current_user_role = None
        try:
            self._login_email_var.set("")
            self._login_error.set("")
        except Exception:
            pass
        self._apply_role_permissions()
        self.show_frame("login")

    def _apply_role_permissions(self):
        role = (self.current_user_role or "user").lower()
        role_text = role.upper()
        try:
            if hasattr(self, "role_label"):
                self.role_label.config(
                    text=role_text,
                    fg=COLORS['accent_purple'] if role_text == "ADMIN" else COLORS['text_secondary'],
                )
        except Exception:
            pass

        # Enable/disable admin-only buttons when role changes.
        try:
            if hasattr(self, "block_btn"):
                self.block_btn.config(state='normal' if role == "admin" else 'disabled')
        except Exception:
            pass
        try:
            if hasattr(self, "unblock_btn"):
                self.unblock_btn.config(state='normal' if role == "admin" else 'disabled')
        except Exception:
            pass

    def _extension_is_active(self):
        try:
            if not os.path.exists(EXTENSION_STATUS_FILE):
                return False, None
            with open(EXTENSION_STATUS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f) or {}
            last_seen = float(data.get("last_seen") or 0)
            if last_seen <= 0:
                return False, None
            return (time.time() - last_seen) <= EXTENSION_ACTIVE_WINDOW_SECONDS, last_seen
        except Exception:
            return False, None

    def _service_script_path(self):
        return os.path.join(_APP_DIR, "cybershield_service.py")

    def _is_service_running(self):
        try:
            import requests
            url = f"http://{CYBERSHIELD_SERVICE_HOST}:{CYBERSHIELD_SERVICE_PORT}/heartbeat"
            r = requests.get(url, timeout=0.6)
            return r.status_code == 200
        except Exception:
            return False

    def start_browser_service(self):
        if self._is_service_running():
            CyberMessageBox.show(self.root, "Service Running", "CyberShield service is already running.", "info")
            return

        script = self._service_script_path()
        if not os.path.exists(script):
            CyberMessageBox.show(self.root, "Missing File", f"Could not find:\n{script}", "error")
            return

        try:
            creationflags = 0
            if os.name == "nt":
                creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)

            self._service_proc = subprocess.Popen(
                [sys.executable, script],
                cwd=_APP_DIR,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=creationflags,
            )

            # Give it a moment to bind the port.
            t0 = time.time()
            while time.time() - t0 < 2.0:
                if self._is_service_running():
                    CyberMessageBox.show(self.root, "Service Started", "CyberShield browser service is running.", "success")
                    return
                time.sleep(0.15)

            CyberMessageBox.show(
                self.root,
                "Service Starting",
                "Service started, but it may still be initializing.\n\n"
                "If the extension still shows NOT ACTIVE, wait a few seconds and try again.",
                "info",
            )
        except Exception as e:
            CyberMessageBox.show(self.root, "Start Failed", str(e), "error")

    def stop_browser_service(self):
        try:
            if self._service_proc is None or self._service_proc.poll() is not None:
                CyberMessageBox.show(self.root, "Not Running", "CyberShield service was not started from this app.", "info")
                return
            self._service_proc.terminate()
            try:
                self._service_proc.wait(timeout=2.0)
            except Exception:
                pass
            CyberMessageBox.show(self.root, "Service Stopped", "CyberShield browser service stopped.", "success")
        except Exception as e:
            CyberMessageBox.show(self.root, "Stop Failed", str(e), "error")

    def _ensure_extension_indicator_loop(self):
        if getattr(self, "_ext_indicator_loop_running", False):
            return
        self._ext_indicator_loop_running = True
        self._ext_blink_on = True
        try:
            self._ext_after_id = self.root.after(250, self._tick_extension_indicator)
        except Exception:
            self._ext_after_id = None
            self._ext_indicator_loop_running = False

    def _tick_extension_indicator(self):
        # If the app is closing, don't reschedule periodic callbacks.
        try:
            if not self.root.winfo_exists():
                self._ext_indicator_loop_running = False
                self._ext_after_id = None
                return
        except Exception:
            self._ext_indicator_loop_running = False
            self._ext_after_id = None
            return

        try:
            active, _last_seen = self._extension_is_active()
            self._ext_blink_on = not getattr(self, "_ext_blink_on", True)
            service_running = self._is_service_running()

            if hasattr(self, "_ext_status_label") and hasattr(self, "_ext_dot_canvas") and hasattr(self, "_ext_dot_id"):
                if active:
                    dot_color = COLORS['accent_green'] if self._ext_blink_on else "#0a4a2a"
                    self._ext_dot_canvas.itemconfig(self._ext_dot_id, fill=dot_color, outline=dot_color)
                    self._ext_status_label.config(text="ACTIVE", fg=COLORS['accent_green'])
                    if hasattr(self, "_ext_indicator_frame"):
                        border = COLORS['accent_green'] if self._ext_blink_on else "#0a4a2a"
                        self._ext_indicator_frame.config(highlightbackground=border)
                    if hasattr(self, "_ext_indicator_title"):
                        self._ext_indicator_title.config(fg=COLORS['text_secondary'])
                else:
                    dot_color = COLORS['accent_red'] if self._ext_blink_on else "#4a0a1f"
                    self._ext_dot_canvas.itemconfig(self._ext_dot_id, fill=dot_color, outline=dot_color)
                    self._ext_status_label.config(text="NOT ACTIVE", fg=COLORS['accent_red'])
                    if hasattr(self, "_ext_indicator_frame"):
                        border = COLORS['accent_red'] if self._ext_blink_on else "#4a0a1f"
                        self._ext_indicator_frame.config(highlightbackground=border)
                    if hasattr(self, "_ext_indicator_title"):
                        self._ext_indicator_title.config(fg=COLORS['text_secondary'])

            if hasattr(self, "_ext_start_service_btn"):
                self._ext_start_service_btn.config(state="disabled" if service_running else "normal")
            if hasattr(self, "_ext_stop_service_btn"):
                can_stop = self._service_proc is not None and self._service_proc.poll() is None
                self._ext_stop_service_btn.config(state="normal" if can_stop else "disabled")
            if hasattr(self, "_ext_hint_label"):
                self._ext_hint_label.config(text="(Guard • Service ON)" if service_running else "(Guard • Service OFF)")
        except Exception:
            pass

        try:
            if self.root.winfo_exists():
                self._ext_after_id = self.root.after(250, self._tick_extension_indicator)
            else:
                self._ext_after_id = None
                self._ext_indicator_loop_running = False
        except Exception:
            self._ext_after_id = None
            self._ext_indicator_loop_running = False

    def _on_close(self):
        try:
            if self._ext_after_id is not None:
                try:
                    self.root.after_cancel(self._ext_after_id)
                except Exception:
                    pass
                self._ext_after_id = None
            self._ext_indicator_loop_running = False
        except Exception:
            pass

        # Best-effort stop the service we started.
        try:
            if self._service_proc is not None and self._service_proc.poll() is None:
                try:
                    self._service_proc.terminate()
                except Exception:
                    pass
        except Exception:
            pass

        try:
            self.root.destroy()
        except Exception:
            pass

    def _build_admin_auth_frame(self):
        if "admin_auth" in self.frames:
            return

        admin_auth = tk.Frame(self.root, bg=COLORS['bg_dark'])

        scroll = ScrollableFrame(admin_auth, bg=COLORS['bg_dark'])
        scroll.pack(side="top", fill="both", expand=True)
        content = scroll.inner

        self._build_help_bar(admin_auth).pack(side="bottom", fill="x")

        header = tk.Frame(content, bg=COLORS['bg_card'], height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Frame(header, bg=COLORS['accent_purple'], height=4).pack(fill="x")
        tk.Label(
            header,
            text="🔐 ADMIN AUTHENTICATION",
            bg=COLORS['bg_card'],
            fg=COLORS['accent_purple'],
            font=("Segoe UI", 18, "bold"),
        ).pack(pady=25)

        card = tk.Frame(content, bg=COLORS['bg_light'], padx=25, pady=25)
        card.pack(fill="x", padx=60, pady=25)

        self._admin_auth_error = tk.StringVar(value="")
        tk.Label(
            card,
            textvariable=self._admin_auth_error,
            bg=COLORS['bg_light'],
            fg=COLORS['accent_red'],
            font=("Consolas", 10),
            justify="left",
        ).pack(fill="x", pady=(0, 10))

        tk.Label(
            card,
            text="Admin Password",
            bg=COLORS['bg_light'],
            fg=COLORS['text_secondary'],
            font=("Consolas", 11, "bold"),
        ).pack(anchor="w")

        entry_border = tk.Frame(card, bg=COLORS['accent_purple'], padx=2, pady=2)
        entry_border.pack(fill="x", pady=(6, 14))
        self._admin_auth_pwd_var = tk.StringVar(value="")
        self._admin_auth_entry = tk.Entry(
            entry_border,
            textvariable=self._admin_auth_pwd_var,
            show="*",
            bg=COLORS['bg_medium'],
            fg=COLORS['text_primary'],
            font=("Consolas", 12),
            borderwidth=0,
            insertbackground=COLORS['accent_purple'],
        )
        self._admin_auth_entry.pack(fill="x", padx=1, pady=1, ipady=10)

        btn_row = tk.Frame(card, bg=COLORS['bg_light'])
        btn_row.pack(fill="x")

        self._admin_auth_result = tk.StringVar(value="")
        submit_btn = tk.Button(
            btn_row,
            text="CONTINUE",
            bg=COLORS['accent_purple'],
            fg=COLORS['text_primary'],
            font=("Segoe UI", 11, "bold"),
            borderwidth=0,
            padx=25,
            pady=12,
            cursor="hand2",
            command=self._admin_auth_submit,
        )
        submit_btn.pack(side="left")
        self._bind_help(submit_btn, "Verify admin password and continue.")

        cancel_btn = tk.Button(
            btn_row,
            text="CANCEL",
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary'],
            font=("Segoe UI", 11, "bold"),
            borderwidth=0,
            padx=25,
            pady=12,
            cursor="hand2",
            command=self._admin_auth_cancel,
        )
        cancel_btn.pack(side="left", padx=10)
        self._bind_help(cancel_btn, "Cancel and return.")

        self._admin_auth_entry.bind("<Return>", lambda _e: self._admin_auth_submit())
        self._admin_auth_entry.bind("<Escape>", lambda _e: self._admin_auth_cancel())

        self.frames["admin_auth"] = admin_auth

    def _admin_auth_submit(self):
        pwd = (self._admin_auth_pwd_var.get() or "").strip()
        if not pwd:
            self._admin_auth_error.set("Enter the admin password.")
            try:
                self._admin_auth_entry.focus_set()
            except Exception:
                pass
            return

        if not authenticate_admin(self.current_user_email, pwd):
            self._admin_auth_error.set("Invalid admin password. Try again.")
            try:
                self._admin_auth_entry.focus_set()
            except Exception:
                pass
            return

        self._admin_auth_error.set("")
        self._admin_auth_result.set("ok")

    def _admin_auth_cancel(self):
        self._admin_auth_error.set("")
        self._admin_auth_result.set("cancel")
    
    def _show_login(self):
        """Show login dialog"""
        if not self.email_configured:
            res = CyberMessageBox.show(
                self.root,
                "Security Configuration",
                "⚠️ Email is not configured!\n\n"
                "Email is required for verification codes.\n\n"
                "Would you like to configure it now?",
                "warning",
                [("Configure", "success"), ("Skip", "secondary"), ("Exit", "danger")]
            )
            if res == "Exit":
                self.root.destroy()
                return
            elif res == "Configure":
                email, pwd = configure_email_interactive()
                if email and pwd:
                    global GMAIL_ADDRESS, APP_PASSWORD
                    GMAIL_ADDRESS = email
                    APP_PASSWORD = pwd
                    self.email_configured = True
                else:
                    CyberMessageBox.show(self.root, "Limited Mode", "Continuing with limited functionality.", "info")
        
        # Show email login
        self.current_user_email = CyberInputDialog.show(
            self.root,
            "🔐 Secure Login",
            "Enter your email to access CyberShield:\n\nYour session will be logged for security.",
            "👤"
        )
        
        if not self.current_user_email:
            self.root.destroy()
            return
        
        self.current_user_email = self.current_user_email.strip().lower()
        self.current_user_role = get_user_role(self.current_user_email)
        
        self._configure_styles()
        self._build_frames()
        self.show_frame("main")
    
    def _configure_styles(self):
        """Configure ttk styles with cyber theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Button styles
        style.configure('Cyber.TButton',
                       background=COLORS['accent_cyan'],
                       foreground=COLORS['bg_dark'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 12),
                       font=('Segoe UI', 11, 'bold'))
        style.map('Cyber.TButton', 
                 background=[('active', '#00c4cc'), ('pressed', '#00a0a8')])
        
        style.configure('CyberDanger.TButton',
                       background=COLORS['accent_red'],
                       foreground=COLORS['text_primary'],
                       borderwidth=0,
                       padding=(20, 12),
                       font=('Segoe UI', 11, 'bold'))
        style.map('CyberDanger.TButton',
                 background=[('active', '#cc0044')])
        
        style.configure('CyberSuccess.TButton',
                       background=COLORS['accent_green'],
                       foreground=COLORS['bg_dark'],
                       borderwidth=0,
                       padding=(20, 12),
                       font=('Segoe UI', 11, 'bold'))
        style.map('CyberSuccess.TButton',
                 background=[('active', '#00cc66')])
        
        # Frame styles
        style.configure('Cyber.TFrame', background=COLORS['bg_dark'])
        style.configure('CyberCard.TFrame', background=COLORS['bg_card'])
        
        # Label styles
        style.configure('CyberTitle.TLabel',
                       background=COLORS['bg_dark'],
                       foreground=COLORS['accent_cyan'],
                       font=('Segoe UI', 24, 'bold'))
        style.configure('CyberHeader.TLabel',
                       background=COLORS['bg_dark'],
                       foreground=COLORS['text_primary'],
                       font=('Segoe UI', 18, 'bold'))
        style.configure('CyberInfo.TLabel',
                       background=COLORS['bg_dark'],
                       foreground=COLORS['text_secondary'],
                       font=('Segoe UI', 11))
        style.configure('CyberAccent.TLabel',
                       background=COLORS['bg_dark'],
                       foreground=COLORS['accent_green'],
                       font=('Consolas', 12))
        
        # Treeview styles
        style.configure('Cyber.Treeview',
                       background=COLORS['bg_light'],
                       foreground=COLORS['text_primary'],
                       fieldbackground=COLORS['bg_light'],
                       borderwidth=0,
                       font=('Consolas', 10))
        style.configure('Cyber.Treeview.Heading',
                       background=COLORS['bg_card'],
                       foreground=COLORS['accent_cyan'],
                       borderwidth=0,
                       font=('Segoe UI', 11, 'bold'))
        style.map('Cyber.Treeview',
                 background=[('selected', COLORS['accent_cyan'])],
                 foreground=[('selected', COLORS['bg_dark'])])
        
        # Entry styles
        style.configure('Cyber.TEntry',
                       fieldbackground=COLORS['bg_light'],
                       foreground=COLORS['text_primary'],
                       borderwidth=2)
        
        # Notebook styles
        style.configure('Cyber.TNotebook',
                       background=COLORS['bg_dark'],
                       borderwidth=0)
        style.configure('Cyber.TNotebook.Tab',
                       background=COLORS['bg_light'],
                       foreground=COLORS['text_secondary'],
                       padding=(16, 10),
                       font=('Segoe UI', 10, 'bold'))
        style.map('Cyber.TNotebook.Tab',
                 background=[('selected', COLORS['accent_cyan']), ('active', COLORS['bg_card'])],
                 foreground=[('selected', COLORS['bg_dark']), ('active', COLORS['text_primary'])])
    
    def _build_frames(self):
        """Build all application frames"""
        self._build_main_frame()
        self._build_guide_frame()
        self._build_blocking_frame()
        self._build_unblocking_frame()
        self._build_logs_frame()
        self._build_dashboard_frame()
    
    def _build_main_frame(self):
        """Build the main menu frame with cyber theme"""
        main = tk.Frame(self.root, bg=COLORS['bg_dark'])
        scroll = ScrollableFrame(main, bg=COLORS['bg_dark'])
        scroll.pack(side="top", fill="both", expand=True)
        content = scroll.inner
        self._build_help_bar(main).pack(side="bottom", fill="x")

        # Browser extension status indicator (top-right)
        self._ext_indicator_frame = tk.Frame(
            main,
            bg=COLORS['bg_card'],
            padx=10,
            pady=6,
            highlightthickness=1,
            highlightbackground=COLORS['border'],
        )
        self._ext_indicator_frame.place(relx=1.0, x=-18, y=14, anchor="ne")

        self._ext_indicator_title = tk.Label(
            self._ext_indicator_frame,
            text="BROWSER EXTENSION",
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary'],
            font=("Consolas", 9, "bold"),
        )
        self._ext_indicator_title.pack(anchor="w")

        row = tk.Frame(self._ext_indicator_frame, bg=COLORS['bg_card'])
        row.pack(anchor="w", pady=(4, 0))

        self._ext_dot_canvas = tk.Canvas(row, width=14, height=14, bg=COLORS['bg_card'], highlightthickness=0)
        self._ext_dot_id = self._ext_dot_canvas.create_oval(2, 2, 12, 12, fill=COLORS['accent_red'], outline=COLORS['accent_red'])
        self._ext_dot_canvas.pack(side="left")

        self._ext_status_label = tk.Label(
            row,
            text="NOT ACTIVE",
            bg=COLORS['bg_card'],
            fg=COLORS['accent_red'],
            font=("Segoe UI", 10, "bold"),
        )
        self._ext_status_label.pack(side="left", padx=(6, 0))

        self._ext_hint_label = tk.Label(
            row,
            text="(Guard)",
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted'],
            font=("Consolas", 9),
        )
        self._ext_hint_label.pack(side="left", padx=(6, 0))

        btn_row = tk.Frame(self._ext_indicator_frame, bg=COLORS['bg_card'])
        btn_row.pack(anchor="w", pady=(6, 0))

        self._ext_start_service_btn = tk.Button(
            btn_row,
            text="▶ Start Service",
            command=self.start_browser_service,
            bg=COLORS['bg_light'],
            fg=COLORS['accent_cyan'],
            font=("Segoe UI", 9, "bold"),
            borderwidth=0,
            padx=10,
            pady=6,
            cursor="hand2",
            activebackground=COLORS['bg_medium'],
            activeforeground=COLORS['accent_cyan'],
        )
        self._ext_start_service_btn.pack(side="left")

        self._ext_stop_service_btn = tk.Button(
            btn_row,
            text="■ Stop",
            command=self.stop_browser_service,
            bg=COLORS['bg_light'],
            fg=COLORS['accent_red'],
            font=("Segoe UI", 9, "bold"),
            borderwidth=0,
            padx=10,
            pady=6,
            cursor="hand2",
            activebackground=COLORS['bg_medium'],
            activeforeground=COLORS['accent_red'],
        )
        self._ext_stop_service_btn.pack(side="left", padx=(8, 0))

        help_text = "Browser extension status. Green blinking = extension is connected. Red blinking = not connected."
        self._bind_help(self._ext_indicator_frame, help_text)
        self._bind_help(self._ext_dot_canvas, help_text)
        self._bind_help(self._ext_indicator_title, help_text)
        self._bind_help(self._ext_status_label, help_text)
        self._bind_help(self._ext_hint_label, help_text)
        self._bind_help(self._ext_start_service_btn, "Start the local browser service (same as running: python cybershield_service.py).")
        self._bind_help(self._ext_stop_service_btn, "Stop the service (only if started from this app).")

        self._ensure_extension_indicator_loop()
        
        # Animated header section
        header_frame = tk.Frame(content, bg=COLORS['bg_dark'])
        header_frame.pack(pady=30)
        
        # Shield logo with glow effect
        logo_canvas = tk.Canvas(
            header_frame, 
            width=120, height=120, 
            bg=COLORS['bg_dark'], 
            highlightthickness=0
        )
        logo_canvas.pack()
        
        # Outer glow
        for i in range(3):
            size = 55 - i * 5
            alpha = 80 + i * 30
            color = f'#00{alpha:02x}{alpha:02x}'
            logo_canvas.create_oval(
                60-size, 60-size, 60+size, 60+size,
                fill='', outline=color, width=2
            )
        
        # Shield shape
        shield_points = [60, 20, 100, 40, 100, 70, 60, 105, 20, 70, 20, 40]
        logo_canvas.create_polygon(shield_points, fill=COLORS['bg_card'], outline=COLORS['accent_cyan'], width=3)
        
        # Check mark
        logo_canvas.create_line(40, 60, 55, 80, 85, 45, fill=COLORS['accent_green'], width=4)
        
        # Title with glow
        title_frame = tk.Frame(header_frame, bg=COLORS['bg_dark'])
        title_frame.pack(pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="CYBERSHIELD",
            bg=COLORS['bg_dark'],
            fg=COLORS['accent_cyan'],
            font=('Impact', 36, 'bold')
        )
        title_label.pack()
        
        # Tagline
        tk.Label(
            header_frame,
            text="━━ Malicious Website Blocker ━━",
            bg=COLORS['bg_dark'],
            fg=COLORS['accent_green'],
            font=('Consolas', 14)
        ).pack(pady=5)
        
        # Status card
        status_frame = tk.Frame(content, bg=COLORS['bg_card'], padx=30, pady=15)
        status_frame.pack(fill='x', padx=60, pady=20)
        
        # Add subtle border
        status_inner = tk.Frame(status_frame, bg=COLORS['bg_card'])
        status_inner.pack(fill='x')
        
        # Stats row
        stats_row = tk.Frame(status_inner, bg=COLORS['bg_card'])
        stats_row.pack(fill='x')
        
        # Blocked count
        blocked_card = tk.Frame(stats_row, bg=COLORS['bg_light'], padx=20, pady=15)
        blocked_card.pack(side='left', expand=True, fill='x', padx=5)
        
        tk.Label(blocked_card, text="🚫", bg=COLORS['bg_light'], fg=COLORS['accent_red'], font=('Segoe UI', 24)).pack()
        self.blocked_count_label = tk.Label(
            blocked_card,
            text=f"{len(self.blocked_sites)} BLOCKED",
            bg=COLORS['bg_light'],
            fg=COLORS['accent_cyan'],
            font=('Segoe UI', 14, 'bold')
        )
        self.blocked_count_label.pack()
        
        # Protection status
        protect_card = tk.Frame(stats_row, bg=COLORS['bg_light'], padx=20, pady=15)
        # protect_card.pack(side='left', expand=True, fill='x', padx=5)  # replaced by top-right extension indicator
        
        tk.Label(protect_card, text="🛡️", bg=COLORS['bg_light'], fg=COLORS['accent_green'], font=('Segoe UI', 24)).pack()
        tk.Label(
            protect_card,
            text="ACTIVE",
            bg=COLORS['bg_light'],
            fg=COLORS['accent_green'],
            font=('Segoe UI', 14, 'bold')
        ).pack()
        
        # User info
        user_card = tk.Frame(stats_row, bg=COLORS['bg_light'], padx=20, pady=15)
        user_card.pack(side='left', expand=True, fill='x', padx=5)
        
        tk.Label(user_card, text="👤", bg=COLORS['bg_light'], fg=COLORS['accent_cyan'], font=('Segoe UI', 24)).pack()
        role_text = self.current_user_role.upper() if hasattr(self, 'current_user_role') else "USER"
        self.role_label = tk.Label(
            user_card,
            text=role_text,
            bg=COLORS['bg_light'],
            fg=COLORS['accent_purple'] if role_text == "ADMIN" else COLORS['text_secondary'],
            font=('Segoe UI', 14, 'bold')
        )
        self.role_label.pack()
        
        # Menu buttons
        btn_frame = tk.Frame(content, bg=COLORS['bg_dark'])
        btn_frame.pack(pady=20, fill='x', padx=60)
        
        buttons = [
            ("📖 User Guide", lambda: self.show_frame("guide"), COLORS['accent_cyan'],
             "Open the User Guide. Hover buttons anywhere to see quick help."),
            ("🚫 Block Websites", lambda: self.show_frame("blocking"), COLORS['accent_red'],
             "Scan URLs and block HIGH risk domains (Admin only)."),
            ("✅ Unblock Websites", lambda: self.show_frame("unblocking"), COLORS['accent_green'],
             "View blocked domains and unblock them (Admin only)."),
            ("📜 Security Logs", lambda: self.show_frame("logs"), COLORS['accent_orange'],
             "View logged actions: scans, blocks, unblocks, and scores."),
            ("📈 Admin Dashboard", lambda: self.show_frame("dashboard"), COLORS['accent_purple'],
             "Charts and stats from your security logs (Admin only)."),
            ("📤 Export Report", self.export_report, COLORS['text_secondary'],
             "Export blocked websites to TXT/CSV/PDF."),
            ("🚪 Logout", self.logout, COLORS['text_secondary'],
             "End your session and return to the login screen."),
        ]
        
        for text, cmd, color, help_text in buttons:
            btn = self._create_menu_button(btn_frame, text, cmd, color, help_text=help_text)
            btn.pack(fill='x', pady=5)
        
        self.frames["main"] = main

    def _build_guide_frame(self):
        """Build the user guide frame (scrollable)"""
        guide = tk.Frame(self.root, bg=COLORS['bg_dark'])

        scroll = ScrollableFrame(guide, bg=COLORS['bg_dark'])
        scroll.pack(side="top", fill="both", expand=True)
        content = scroll.inner

        self._build_help_bar(guide).pack(side="bottom", fill="x")

        header = tk.Frame(content, bg=COLORS['bg_card'], height=90)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Frame(header, bg=COLORS['accent_cyan'], height=4).pack(fill="x")
        tk.Label(
            header,
            text="📖 USER GUIDE",
            bg=COLORS['bg_card'],
            fg=COLORS['accent_cyan'],
            font=("Segoe UI", 20, "bold"),
        ).pack(pady=20)

        card = tk.Frame(content, bg=COLORS['bg_light'], padx=25, pady=25)
        card.pack(fill="both", expand=True, padx=35, pady=20)

        guide_text = (
            "Welcome to CyberShield.\n\n"
            "Quick tips:\n"
            "• Hover any button to see help in the bottom bar.\n"
            "• If you can't see buttons at the bottom, scroll down.\n\n"
            "Browser Extension Status (top-right indicator)\n"
            "• Green blinking dot + ACTIVE = browser extension is running and connected to the local CyberShield service.\n"
            "• Red dot + NOT ACTIVE = extension is not connected (extension not running, browser closed, or the local service is not running).\n"
            "• To use the extension: load the extension folder and start the local service.\n"
            "  - You can click ▶ Start Service in the top-right badge (recommended for demos).\n"
            "  - Or run: python cybershield_service.py\n\n"
            "1) Block Websites (Admin)\n"
            "• Enter a URL or upload a .txt list.\n"
            "• Click 'SCAN THREATS' to analyze.\n"
            "• To select more than one Websites/URLs to block, use 'ctrl + left click' on the rows.\n"
            "• Select one or more rows and click 'BLOCK SELECTED' to block.\n"
            "• Optional: enable Auto‑Block to block HIGH risk domains automatically.\n\n"
            "2) Unblock Websites (Admin)\n"
            "• Open the Unblock screen, select domains, then click 'UNBLOCK SELECTED'.\n\n"
            "3) Security Logs\n"
            "• View all actions and threat scores recorded by the app.\n\n"
            "4) Admin Dashboard (Admin)\n"
            "• Shows charts built from your logs (opens fast; charts render per tab).\n\n"
            "5) Export Report\n"
            "• Export blocked websites to TXT / CSV / PDF.\n\n"
            "Notes:\n"
            "• Admin-only actions will ask for admin authentication.\n"
            "• Use clean URLs (with https:// when possible) for best results.\n"
        )

        tk.Label(
            card,
            text=guide_text,
            bg=COLORS['bg_light'],
            fg=COLORS['text_primary'],
            font=("Consolas", 11),
            justify="left",
            wraplength=900,
        ).pack(anchor="w", fill="x")

        btn_row = tk.Frame(content, bg=COLORS['bg_dark'])
        btn_row.pack(pady=15)

        back_btn = tk.Button(
            btn_row,
            text="← BACK",
            command=lambda: self.show_frame("main"),
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary'],
            font=("Segoe UI", 11, "bold"),
            borderwidth=0,
            padx=25,
            pady=12,
            cursor="hand2",
        )
        back_btn.pack()
        self._bind_help(back_btn, "Return to the main menu.")

        self.frames["guide"] = guide
    
    def _create_menu_button(self, parent, text, command, color, help_text=None):
        """Create a cyber-styled menu button"""
        btn_frame = tk.Frame(parent, bg=COLORS['bg_dark'])
        
        btn = tk.Button(
            btn_frame,
            text=text,
            command=command,
            bg=COLORS['bg_light'],
            fg=color,
            font=('Segoe UI', 12, 'bold'),
            borderwidth=0,
            padx=30, pady=15,
            cursor='hand2',
            relief='flat',
            activebackground=COLORS['bg_card'],
            activeforeground=color,
            anchor='w'
        )
        btn.pack(fill='x', ipady=2)
        
        # Add left accent bar
        accent = tk.Frame(btn_frame, bg=color, width=4)
        accent.place(x=0, y=0, relheight=1)
        
        def on_enter(e):
            btn.config(bg=COLORS['bg_card'])
            accent.config(width=8)
            if help_text:
                try:
                    self._help_var.set(help_text)
                except Exception:
                    pass
        
        def on_leave(e):
            btn.config(bg=COLORS['bg_light'])
            accent.config(width=4)
            if help_text:
                try:
                    self._help_var.set(self._help_default)
                except Exception:
                    pass
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn_frame
    
    def _build_blocking_frame(self):
        """Build the blocking frame with cyber theme"""
        blocking = tk.Frame(self.root, bg=COLORS['bg_dark'])
        scroll = ScrollableFrame(blocking, bg=COLORS['bg_dark'])
        scroll.pack(side="top", fill="both", expand=True)
        content = scroll.inner
        self._build_help_bar(blocking).pack(side="bottom", fill="x")
        
        # Header
        header = tk.Frame(content, bg=COLORS['bg_card'], height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Frame(header, bg=COLORS['accent_red'], height=4).pack(fill='x')
        
        tk.Label(
            header,
            text="🚫 THREAT BLOCKING CENTER",
            bg=COLORS['bg_card'],
            fg=COLORS['accent_red'],
            font=('Segoe UI', 20, 'bold')
        ).pack(pady=20)
        
        # URL input section
        input_frame = tk.Frame(content, bg=COLORS['bg_light'], padx=20, pady=20)
        input_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Label(
            input_frame,
            text="TARGET URL",
            bg=COLORS['bg_light'],
            fg=COLORS['accent_cyan'],
            font=('Consolas', 10, 'bold')
        ).pack(anchor='w')
        
        entry_row = tk.Frame(input_frame, bg=COLORS['bg_light'])
        entry_row.pack(fill='x', pady=10)
        
        # Styled entry
        entry_frame = tk.Frame(entry_row, bg=COLORS['accent_cyan'], padx=2, pady=2)
        entry_frame.pack(side='left', fill='x', expand=True)
        
        self.url_entry = tk.Entry(
            entry_frame,
            bg=COLORS['bg_dark'],
            fg=COLORS['text_primary'],
            font=('Consolas', 12),
            relief='flat',
            insertbackground=COLORS['accent_cyan']
        )
        self.url_entry.pack(fill='x', padx=1, pady=1, ipady=10)
        
        # Upload button
        upload_btn = tk.Button(
            entry_row,
            text="📁 UPLOAD",
            command=self.upload_file,
            bg=COLORS['accent_cyan'],
            fg=COLORS['bg_dark'],
            font=('Segoe UI', 10, 'bold'),
            borderwidth=0,
            padx=20, pady=12,
            cursor='hand2'
        )
        upload_btn.pack(side='left', padx=(10, 0))
        self._bind_help(upload_btn, "Upload a .txt file with one URL per line.")
        
        self.upload_status = tk.Label(
            entry_row,
            text="",
            bg=COLORS['bg_light'],
            font=('Segoe UI', 16)
        )
        self.upload_status.pack(side='left', padx=10)
        
        # Action buttons
        action_frame = tk.Frame(content, bg=COLORS['bg_dark'])
        action_frame.pack(pady=10)
        
        scan_btn = tk.Button(
            action_frame,
            text="🔍 SCAN THREATS",
            command=self.check_urls,
            bg=COLORS['accent_cyan'],
            fg=COLORS['bg_dark'],
            font=('Segoe UI', 12, 'bold'),
            borderwidth=0,
            padx=30, pady=12,
            cursor='hand2'
        )
        scan_btn.pack(side='left', padx=5)
        self._bind_help(scan_btn, "Scan the entered/uploaded URLs using threat intelligence sources.")
        
        # Auto-block checkbox
        auto_frame = tk.Frame(content, bg=COLORS['bg_dark'])
        auto_frame.pack(pady=5)
        
        auto_cb = tk.Checkbutton(
            auto_frame,
            text="⚡ AUTO-BLOCK HIGH RISK (Score > 60)",
            variable=self.auto_block_enabled,
            bg=COLORS['bg_dark'],
            fg=COLORS['accent_orange'],
            selectcolor=COLORS['bg_light'],
            activebackground=COLORS['bg_dark'],
            activeforeground=COLORS['accent_orange'],
            font=('Consolas', 10)
        )
        auto_cb.pack()
        self._bind_help(auto_cb, "When enabled: automatically block HIGH risk domains (score > 60).")
        
        # Results tree
        tree_frame = tk.Frame(content, bg=COLORS['accent_cyan'], padx=2, pady=2)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("url", "status"),
            show="headings",
            selectmode="extended",
            style='Cyber.Treeview'
        )
        self.tree.heading("url", text="TARGET URL")
        self.tree.heading("status", text="THREAT ANALYSIS")
        self.tree.column("url", width=350)
        self.tree.column("status", width=500)
        self.tree.pack(fill='both', expand=True)
        
        # Bottom buttons
        btn_frame = tk.Frame(content, bg=COLORS['bg_dark'])
        btn_frame.pack(pady=15)
        
        self.block_btn = tk.Button(
            btn_frame,
            text="🚫 BLOCK SELECTED",
            command=self.block_selected,
            bg=COLORS['accent_red'],
            fg=COLORS['text_primary'],
            font=('Segoe UI', 11, 'bold'),
            borderwidth=0,
            padx=25, pady=12,
            cursor='hand2'
        )
        self.block_btn.pack(side='left', padx=5)
        self._bind_help(self.block_btn, "Block the selected domains (Admin only; requires authentication).")
        
        if hasattr(self, 'current_user_role') and self.current_user_role != "admin":
            self.block_btn.config(state='disabled')
        
        back_btn = tk.Button(
            btn_frame,
            text="← BACK",
            command=lambda: self.show_frame("main"),
            bg=COLORS['bg_light'],
            fg=COLORS['text_secondary'],
            font=('Segoe UI', 11, 'bold'),
            borderwidth=0,
            padx=25, pady=12,
            cursor='hand2'
        )
        back_btn.pack(side='left', padx=5)
        self._bind_help(back_btn, "Return to the main menu.")
        
        self.frames["blocking"] = blocking
    
    def _build_unblocking_frame(self):
        """Build the unblocking frame"""
        unblocking = tk.Frame(self.root, bg=COLORS['bg_dark'])
        scroll = ScrollableFrame(unblocking, bg=COLORS['bg_dark'])
        scroll.pack(side="top", fill="both", expand=True)
        content = scroll.inner
        self._build_help_bar(unblocking).pack(side="bottom", fill="x")
        
        # Header
        header = tk.Frame(content, bg=COLORS['bg_card'], height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Frame(header, bg=COLORS['accent_green'], height=4).pack(fill='x')
        
        tk.Label(
            header,
            text="✅ THREAT REMOVAL CENTER",
            bg=COLORS['bg_card'],
            fg=COLORS['accent_green'],
            font=('Segoe UI', 20, 'bold')
        ).pack(pady=20)
        
        # Tree
        tree_frame = tk.Frame(content, bg=COLORS['accent_green'], padx=2, pady=2)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.tree_unblock = ttk.Treeview(
            tree_frame,
            columns=("url", "status"),
            show="headings",
            selectmode="extended",
            style='Cyber.Treeview'
        )
        self.tree_unblock.heading("url", text="BLOCKED DOMAIN")
        self.tree_unblock.heading("status", text="STATUS")
        self.tree_unblock.pack(fill='both', expand=True)
        
        # Buttons
        btn_frame = tk.Frame(content, bg=COLORS['bg_dark'])
        btn_frame.pack(pady=15)
        
        self.unblock_btn = tk.Button(
            btn_frame,
            text="✅ UNBLOCK SELECTED",
            command=self.unblock_selected,
            bg=COLORS['accent_green'],
            fg=COLORS['bg_dark'],
            font=('Segoe UI', 11, 'bold'),
            borderwidth=0,
            padx=25, pady=12,
            cursor='hand2'
        )
        self.unblock_btn.pack(side='left', padx=5)
        self._bind_help(self.unblock_btn, "Unblock the selected domains (Admin only; requires authentication).")
        
        if hasattr(self, 'current_user_role') and self.current_user_role != "admin":
            self.unblock_btn.config(state='disabled')
        
        back_btn = tk.Button(
            btn_frame,
            text="← BACK",
            command=lambda: self.show_frame("main"),
            bg=COLORS['bg_light'],
            fg=COLORS['text_secondary'],
            font=('Segoe UI', 11, 'bold'),
            borderwidth=0,
            padx=25, pady=12,
            cursor='hand2'
        )
        back_btn.pack(side='left', padx=5)
        
        self.frames["unblocking"] = unblocking
    
    def _build_logs_frame(self):
        """Build the security logs frame"""
        logs = tk.Frame(self.root, bg=COLORS['bg_dark'])
        scroll = ScrollableFrame(logs, bg=COLORS['bg_dark'])
        scroll.pack(side="top", fill="both", expand=True)
        content = scroll.inner
        self._build_help_bar(logs).pack(side="bottom", fill="x")
        
        # Header
        header = tk.Frame(content, bg=COLORS['bg_card'], height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Frame(header, bg=COLORS['accent_orange'], height=4).pack(fill='x')
        
        tk.Label(
            header,
            text="📜 SECURITY AUDIT LOG",
            bg=COLORS['bg_card'],
            fg=COLORS['accent_orange'],
            font=('Segoe UI', 20, 'bold')
        ).pack(pady=20)
        
        # Tree
        tree_frame = tk.Frame(content, bg=COLORS['accent_orange'], padx=2, pady=2)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        self.log_tree = ttk.Treeview(
            tree_frame,
            columns=("time", "action", "target", "email", "score", "risk", "sources"),
            show="headings",
            style='Cyber.Treeview'
        )
        
        cols = [
            ("time", "TIMESTAMP", 140),
            ("action", "ACTION", 90),
            ("target", "TARGET", 200),
            ("email", "USER", 160),
            ("score", "SCORE", 70),
            ("risk", "RISK", 80),
            ("sources", "SOURCES", 180),
        ]
        
        for col_id, col_text, width in cols:
            self.log_tree.heading(col_id, text=col_text)
            self.log_tree.column(col_id, width=width, anchor="center")
        
        self.log_tree.pack(fill='both', expand=True)
        
        # Back button
        btn_frame = tk.Frame(content, bg=COLORS['bg_dark'])
        btn_frame.pack(pady=15)
        
        back_btn = tk.Button(
            btn_frame,
            text="← BACK",
            command=lambda: self.show_frame("main"),
            bg=COLORS['bg_light'],
            fg=COLORS['text_secondary'],
            font=('Segoe UI', 11, 'bold'),
            borderwidth=0,
            padx=25, pady=12,
            cursor='hand2'
        )
        back_btn.pack()
        
        self.frames["logs"] = logs
    
    def _build_dashboard_frame(self):
        """Build the admin dashboard frame"""
        dashboard = tk.Frame(self.root, bg=COLORS['bg_dark'])
        scroll = ScrollableFrame(dashboard, bg=COLORS['bg_dark'])
        scroll.pack(side="top", fill="both", expand=True)
        content = scroll.inner
        self._build_help_bar(dashboard).pack(side="bottom", fill="x")
        
        # Header
        header = tk.Frame(content, bg=COLORS['bg_card'], height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Frame(header, bg=COLORS['accent_purple'], height=4).pack(fill='x')
        
        tk.Label(
            header,
            text="📈 ADMIN COMMAND CENTER",
            bg=COLORS['bg_card'],
            fg=COLORS['accent_purple'],
            font=('Segoe UI', 20, 'bold')
        ).pack(pady=20)
        
        # Dashboard container
        self.dashboard_container = tk.Frame(content, bg=COLORS['bg_dark'])
        self.dashboard_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Back button
        btn_frame = tk.Frame(content, bg=COLORS['bg_dark'])
        btn_frame.pack(pady=15)
        
        back_btn = tk.Button(
            btn_frame,
            text="← BACK",
            command=lambda: self.show_frame("main"),
            bg=COLORS['bg_light'],
            fg=COLORS['text_secondary'],
            font=('Segoe UI', 11, 'bold'),
            borderwidth=0,
            padx=25, pady=12,
            cursor='hand2'
        )
        back_btn.pack()
        
        self.frames["dashboard"] = dashboard
    
    def admin_password_check(self):
        if getattr(self, "current_user_role", None) != "admin":
            CyberMessageBox.show(self.root, "Access Denied", "Admin privileges required.", "error")
            return False

        self._build_admin_auth_frame()
        return_to = self._current_frame_name or "main"

        try:
            self._admin_auth_pwd_var.set("")
            self._admin_auth_error.set("")
            self._admin_auth_result.set("")
        except Exception:
            pass

        self.show_frame("admin_auth")
        try:
            self.root.after(50, lambda: self._admin_auth_entry.focus_set())
        except Exception:
            pass

        try:
            self.root.wait_variable(self._admin_auth_result)
        except Exception:
            return False

        ok = (self._admin_auth_result.get() == "ok")
        self.show_frame(return_to)
        return ok
    
    def export_report(self):
        if not self.blocked_sites:
            CyberMessageBox.show(self.root, "No Data", "No blocked websites to export.", "info")
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt"), ("CSV File", "*.csv"), ("PDF File", "*.pdf")]
        )
        if not path:
            return
        
        try:
            if path.endswith(".txt"):
                export_txt_report(path, self.blocked_sites)
            elif path.endswith(".csv"):
                export_csv_report(path, self.blocked_sites)
            elif path.endswith(".pdf"):
                export_pdf_report(path, self.blocked_sites)
            
            CyberMessageBox.show(self.root, "Export Complete", f"Report saved to:\n{path}", "success")
        except Exception as e:
            CyberMessageBox.show(self.root, "Export Failed", str(e), "error")
    
    def load_logs_into_gui(self):
        if not os.path.exists(LOG_FILE):
            return
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    parts = dict(p.split("=", 1) for p in line.strip().split() if "=" in p)
                    time_part = line.split("]")[0][1:]
                    self.log_tree.insert("", "end", values=(
                        time_part,
                        parts.get("ACTION", ""),
                        parts.get("TARGET", ""),
                        parts.get("EMAIL", ""),
                        parts.get("SCORE", ""),
                        parts.get("RISK", ""),
                        parts.get("SOURCES", "")
                    ))
                except:
                    continue
    
    def update_blocked_count(self):
        count = len(self.blocked_sites)
        if hasattr(self, 'blocked_count_label'):
            self.blocked_count_label.config(text=f"{count} BLOCKED")
    
    def show_frame(self, name):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[name].pack(fill="both", expand=True)
        self._current_frame_name = name
        try:
            self._help_var.set(self._help_default)
        except Exception:
            pass
        
        if name == "dashboard":
            if self.current_user_role != "admin":
                CyberMessageBox.show(self.root, "Access Denied", "Admin privileges required.", "error")
                self.show_frame("main")
                return
            self._refresh_dashboard()
        
        if name == "main":
            self.update_blocked_count()
        elif name == "unblocking":
            for i in self.tree_unblock.get_children():
                self.tree_unblock.delete(i)
            for url in self.blocked_sites:
                self.tree_unblock.insert("", "end", values=(url, "🔒 BLOCKED"))
        elif name == "logs":
            self.log_tree.delete(*self.log_tree.get_children())
            self.load_logs_into_gui()
    
    def upload_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            with open(path, "r", encoding="utf-8") as f:
                raw_lines = [line.strip() for line in f if line.strip()]
            seen = set()
            unique_lines = []
            for ln in raw_lines:
                if ln not in seen:
                    seen.add(ln)
                    unique_lines.append(ln)
            self._last_uploaded_urls = unique_lines
            if self._last_uploaded_urls:
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, self._last_uploaded_urls[0])
                self.upload_status.config(text="✅", fg=COLORS['accent_green'])
            else:
                self.upload_status.config(text="❌", fg=COLORS['accent_red'])
    
    def check_urls(self):
        self.tree.delete(*self.tree.get_children())
        urls = []
        input_val = self.url_entry.get().strip()
        if input_val:
            urls.append(input_val)
        if self._last_uploaded_urls:
            for u in self._last_uploaded_urls:
                if u not in urls:
                    urls.append(u)
        
        if not urls:
            CyberMessageBox.show(self.root, "Input Required", "Please enter a URL or upload a file.", "warning")
            return
        
        def worker():
            _fetch_openphish_feed()
            for u in urls:
                raw, dom = normalize_raw_url(u)
                
                if not raw:
                    overall_status = "❌ INVALID URL"
                else:
                    vt = vt_check_url(raw)
                    mb = malwarebazaar_check_url(dom)
                    op = openphish_check(raw, dom)
                    uh = urlhaus_check_host(dom)
                    redirect_status, redirect_info = redirect_chain_check(raw, dom)
                    ssl_status, ssl_info = ssl_certificate_check(dom)
                    phish_status, phish_score, phish_reasons, phish_hits = phishing_algorithm_check(raw, dom)
                    
                    score, risk, sources = calculate_threat_score(
                        vt, mb, op, uh,
                        phishing_status=phish_status,
                        phishing_score=phish_score,
                        redirect_status=redirect_status,
                        ssl_status=ssl_status
                    )
                    
                    self.threat_cache[dom] = {
                        "score": score,
                        "risk": risk,
                        "sources": sources + (["Phishing-Algorithm"] if phish_status == "SUSPECT" else [])
                    }
                    
                    if self.auto_block_enabled.get() and risk == "HIGH" and dom and dom not in self.blocked_sites:
                        try:
                            add_host_entry(dom)
                            self.blocked_sites[dom] = {"status": "blocked", "email": "AUTO-BLOCK"}
                            save_blocked_sites(self.blocked_sites)
                            write_security_log("AUTO-BLOCK", raw, score=score, risk=risk, sources=sources)
                        except:
                            pass
                    
                    write_security_log("SCAN", raw, score=score, risk=risk, sources=sources)
                    
                    if risk == "HIGH":
                        icon = "🚨"
                        risk_color = "HIGH RISK"
                        if self.auto_block_enabled.get():
                            risk_color += " [AUTO-BLOCKED]"
                    elif risk == "MEDIUM":
                        icon = "⚠️"
                        risk_color = "MEDIUM RISK"
                    else:
                        icon = "✅"
                        risk_color = "LOW RISK"
                    
                    overall_status = f"{icon} {risk_color} | Score: {score}/100 | Sources: {', '.join(sources) if sources else 'None'}"
                
                self.root.after(0, lambda u=u, s=overall_status: self.tree.insert("", "end", values=(u, s)))
        
        threading.Thread(target=worker, daemon=True).start()
    
    def verify_email_code(self, preset_email=None):
        while True:
            if preset_email:
                email = preset_email
            else:
                email = CyberInputDialog.show(self.root, "📧 Email Verification", "Enter your email for verification:", "📧")
            
            if not email:
                return None
            
            email = email.strip()
            if "@" not in email:
                CyberMessageBox.show(self.root, "Invalid Email", "Please enter a valid email.", "error")
                if preset_email:
                    return None
                continue
            
            ok, code_or_msg = send_verification_code(email, purpose="verification")
            if not ok:
                CyberMessageBox.show(self.root, "Failed", f"Could not send code:\n{code_or_msg}", "error")
                if preset_email:
                    return None
                continue
            
            code = code_or_msg
            CyberMessageBox.show(self.root, "Code Sent", f"Verification code sent to:\n{email}", "success")
            
            while True:
                entry = CyberInputDialog.show(
                    self.root,
                    "🔐 Enter Code",
                    f"Code sent to {email}\n\nType 'resend' or 'change' if needed.",
                    "🔐"
                )
                if entry is None:
                    return None
                entry = entry.strip()
                if entry.lower() == "resend":
                    send_email_single(email, "CyberShield - Code (Resent)", f"Your code: {code}")
                    CyberMessageBox.show(self.root, "Resent", "Code resent.", "success")
                    continue
                if entry.lower() == "change":
                    new_email = CyberInputDialog.show(self.root, "Change Email", "Enter new email:", "📧")
                    if new_email:
                        preset_email = new_email
                    break
                if entry == code:
                    CyberMessageBox.show(self.root, "Verified", "Email verified!", "success")
                    return email
                CyberMessageBox.show(self.root, "Invalid", "Incorrect code.", "error")
    
    def block_selected(self):
        if self.current_user_role != "admin":
            CyberMessageBox.show(self.root, "Access Denied", "Admin privileges required.", "error")
            return
        
        if not self.admin_password_check():
            return
        
        sel = self.tree.selection()
        if not sel:
            CyberMessageBox.show(self.root, "No Selection", "Select URLs to block.", "warning")
            return
        
        email = self.verify_email_code()
        if not email:
            return
        
        success, failed = [], []
        for iid in sel:
            url = self.tree.item(iid, "values")[0]
            raw, dom = normalize_raw_url(url)
            if not raw or not dom:
                failed.append(url + " (invalid)")
                continue
            
            try:
                if add_host_entry(dom):
                    threat = self.threat_cache.get(dom, {})
                    self.blocked_sites[dom] = {
                        "status": "blocked",
                        "email": email,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "score": threat.get("score", "N/A"),
                        "risk": threat.get("risk", "N/A"),
                        "reason": ", ".join(threat.get("sources", [])) or "Manual"
                    }
                    success.append(dom)
                    write_security_log("BLOCK", dom, email=email)
                else:
                    failed.append(dom + " (already blocked)")
            except PermissionError:
                failed.append(dom + " (admin required)")
            except Exception as e:
                failed.append(dom + f" ({e})")
        
        save_blocked_sites(self.blocked_sites)
        self.update_blocked_count()
        
        items = []
        if success:
            items.append("✅ Blocked:")
            items.extend([f"  • {s}" for s in success])
        if failed:
            if items:
                items.append("")
            items.append("❌ Failed:")
            items.extend([f"  • {f}" for f in failed])
        
        if items:
            CyberListDialog.show(self.root, "Block Result", f"Processed {len(success)+len(failed)} sites", items, "🚫")
    
    def unblock_selected(self):
        if self.current_user_role != "admin":
            CyberMessageBox.show(self.root, "Access Denied", "Admin privileges required.", "error")
            return
        
        if not self.admin_password_check():
            return
        
        sel = self.tree_unblock.selection()
        if not sel:
            CyberMessageBox.show(self.root, "No Selection", "Select domains to unblock.", "warning")
            return
        
        domains_to_unblock = []
        for iid in sel:
            dom = self.tree_unblock.item(iid, "values")[0]
            site_info = self.blocked_sites.get(dom, {})
            stored_email = site_info.get("email") if isinstance(site_info, dict) else None
            if not stored_email:
                CyberListDialog.show(
                    self.root, "Cannot Unblock",
                    "Domain blocked without email:",
                    [f"• {dom}", "", "Edit hosts file manually."],
                    "❌"
                )
                return
            domains_to_unblock.append({"domain": dom, "email": stored_email})
        
        unique_emails = list(set(d["email"] for d in domains_to_unblock))
        if len(unique_emails) > 1:
            CyberMessageBox.show(self.root, "Multiple Emails", "Domains have different emails. Unblock separately.", "error")
            return
        
        expected_email = unique_emails[0]
        
        if expected_email == "AUTO-BLOCK":
            CyberMessageBox.show(self.root, "Auto-Blocked", "This domain was auto-blocked.\nManual verification required.", "warning")
            verified_email = self.verify_email_code()
        else:
            CyberMessageBox.show(self.root, "Verify Email", f"Verify email used for blocking:\n{expected_email}", "info")
            verified_email = self.verify_email_code(preset_email=expected_email)
        
        if not verified_email:
            return
        
        success, failed = [], []
        for item in domains_to_unblock:
            dom = item["domain"]
            try:
                remove_host_entry(dom)
                self.blocked_sites.pop(dom, None)
                success.append(dom)
                write_security_log("UNBLOCK", dom, email=verified_email)
            except PermissionError:
                failed.append(dom + " (admin required)")
            except Exception as e:
                failed.append(dom + f" ({e})")
        
        save_blocked_sites(self.blocked_sites)
        self.update_blocked_count()
        
        items = []
        if success:
            items.append("✅ Unblocked:")
            items.extend([f"  • {s}" for s in success])
        if failed:
            if items:
                items.append("")
            items.append("❌ Failed:")
            items.extend([f"  • {f}" for f in failed])
        
        if items:
            CyberListDialog.show(self.root, "Unblock Result", f"Processed {len(success)+len(failed)} sites", items, "✅")
        
        self.show_frame("unblocking")
    
    # Dashboard methods
    def _parse_security_logs_for_dashboard(self):
        entries = []
        if not os.path.exists(LOG_FILE):
            return entries
        log_re = re.compile(
            r"^\[(?P<time>[^\]]+)\]\s+ACTION=(?P<action>\w+)\s+TARGET=(?P<target>.+?)\s+"
            r"EMAIL=(?P<email>.+?)\s+SCORE=(?P<score>.+?)\s+RISK=(?P<risk>.+?)\s+"
            r"SOURCES=(?P<sources>.+)$"
        )
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                m = log_re.match(line.strip())
                if not m:
                    continue
                d = m.groupdict()
                try:
                    d["score"] = int(d.get("score", 0))
                except:
                    d["score"] = 0
                d["sources"] = [s.strip() for s in d.get("sources", "").split(",") if s.strip() and s.strip().lower() != "none"]
                try:
                    d["time_dt"] = datetime.strptime(d.get("time"), "%Y-%m-%d %H:%M:%S")
                except:
                    d["time_dt"] = None
                entries.append(d)
        return entries
    
    def _dashboard_safe_mtime(self, path):
        try:
            return os.path.getmtime(path)
        except OSError:
            return None
    
    def _dashboard_state(self):
        return (self._dashboard_safe_mtime(DATA_FILE), self._dashboard_safe_mtime(LOG_FILE))
    
    def _dashboard_cleanup_figures(self):
        for fig in getattr(self, "_dashboard_figures", []):
            try:
                plt.close(fig)
            except:
                pass
        self._dashboard_figures = []
        self._dashboard_canvases = []
    
    def _dashboard_init_layout(self):
        self._dashboard_notebook = ttk.Notebook(self.dashboard_container, style="Cyber.TNotebook")
        self._dashboard_notebook.pack(fill="both", expand=True)
        
        self._dashboard_tabs = {}
        self._dashboard_tab_loading_labels = {}
        for tab_name in ["Overview", "Blocking", "Sources", "Activity"]:
            tab = tk.Frame(self._dashboard_notebook, bg=COLORS['bg_dark'])
            self._dashboard_notebook.add(tab, text=tab_name)
            self._dashboard_tabs[tab_name] = tab
            self._dashboard_tab_loading_labels[tab_name] = tk.Label(
                tab, text="Loading...", bg=COLORS['bg_dark'], fg=COLORS['text_secondary'], font=('Consolas', 12)
            )
            self._dashboard_tab_loading_labels[tab_name].pack(fill="both", expand=True, pady=30)
        
        self._dashboard_notebook.bind("<<NotebookTabChanged>>", self._on_dashboard_tab_changed)
        
        plt.rcParams.update({
            "figure.facecolor": COLORS['bg_dark'],
            "axes.facecolor": COLORS['bg_light'],
            "axes.edgecolor": COLORS['border'],
            "axes.labelcolor": COLORS['text_primary'],
            "xtick.color": COLORS['text_secondary'],
            "ytick.color": COLORS['text_secondary'],
            "text.color": COLORS['text_primary'],
        })
    
    def _dashboard_load_data_worker(self, token, desired_state):
        try:
            blocked = load_blocked_sites()
            logs = self._parse_security_logs_for_dashboard()
            
            risk_counts = Counter([e.get("risk", "").upper() for e in logs if e.get("risk")])
            action_counts = Counter([e.get("action") for e in logs if e.get("action")])
            source_counts = Counter()
            for e in logs:
                for s in e.get("sources", []):
                    source_counts[s] += 1
            
            auto_block = sum(1 for v in blocked.values() if isinstance(v, dict) and v.get("email") == "AUTO-BLOCK")
            manual_block = max(0, len(blocked) - auto_block)
            top_domains = Counter(blocked.keys()).most_common(10)
            scores = [e["score"] for e in logs if isinstance(e.get("score"), int)]
            
            date_counts = defaultdict(int)
            for e in logs:
                if e.get("time_dt"):
                    date_counts[e["time_dt"].date()] += 1
            
            data = {
                "state": desired_state, "risk_counts": risk_counts, "action_counts": action_counts,
                "source_counts": source_counts, "auto_block": auto_block, "manual_block": manual_block,
                "top_domains": top_domains, "scores": scores, "date_counts": date_counts,
            }
        except Exception as e:
            data = {"state": desired_state, "error": str(e)}
        
        try:
            self.root.after(0, lambda: self._dashboard_on_data_ready(token, data))
        except:
            pass
    
    def _dashboard_on_data_ready(self, token, data):
        if token != self._dashboard_refresh_token:
            return
        self._dashboard_data_loading = False
        self._dashboard_data = data
        self._dashboard_last_state = data.get("state")
        
        if data.get("error"):
            for tab in self._dashboard_tabs.values():
                for child in tab.winfo_children():
                    child.destroy()
                tk.Label(tab, text=f"Error: {data['error']}", bg=COLORS['bg_dark'], fg=COLORS['accent_red']).pack()
            return
        
        try:
            tab_text = self._dashboard_notebook.tab(self._dashboard_notebook.select(), "text")
        except:
            tab_text = "Overview"
        self._dashboard_render_tab(tab_text)
    
    def _on_dashboard_tab_changed(self, _event=None):
        try:
            tab_text = self._dashboard_notebook.tab(self._dashboard_notebook.select(), "text")
        except:
            tab_text = "Overview"
        self._dashboard_render_tab(tab_text)
    
    def _dashboard_render_tab(self, tab_text):
        if not self._dashboard_data or self._dashboard_data.get("error"):
            return
        if tab_text in self._dashboard_rendered_tabs:
            return
        tab = self._dashboard_tabs.get(tab_text)
        if not tab:
            return
        
        for child in tab.winfo_children():
            child.destroy()
        
        data = self._dashboard_data
        
        def empty_chart(ax, title):
            ax.set_title(title, color=COLORS['accent_cyan'])
            ax.text(0.5, 0.5, "No data", ha="center", va="center", color=COLORS['text_secondary'])
            ax.set_xticks([])
            ax.set_yticks([])
        
        if tab_text == "Overview":
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
            fig.tight_layout(pad=3)
            risk_counts = data["risk_counts"]
            action_counts = data["action_counts"]
            if risk_counts:
                labels = list(risk_counts.keys())
                values = [risk_counts[k] for k in labels]
                colors = [COLORS['accent_red'] if 'HIGH' in l else COLORS['accent_orange'] if 'MEDIUM' in l else COLORS['accent_green'] for l in labels]
                ax1.pie(values, labels=labels, autopct="%1.0f%%", colors=colors)
                ax1.set_title("Risk Distribution", color=COLORS['accent_cyan'])
            else:
                empty_chart(ax1, "Risk Distribution")
            if action_counts:
                labels = list(action_counts.keys())
                values = [action_counts[k] for k in labels]
                ax2.bar(labels, values, color=COLORS['accent_cyan'])
                ax2.set_title("Actions", color=COLORS['accent_cyan'])
            else:
                empty_chart(ax2, "Actions")
        elif tab_text == "Blocking":
            fig, (ax3, ax4) = plt.subplots(1, 2, figsize=(10, 4))
            fig.tight_layout(pad=3)
            if data["top_domains"]:
                labels = [d for d, _ in data["top_domains"]]
                values = [c for _, c in data["top_domains"]]
                ax3.barh(labels, values, color=COLORS['accent_red'])
                ax3.set_title("Top Blocked", color=COLORS['accent_cyan'])
            else:
                empty_chart(ax3, "Top Blocked")
            if data["auto_block"] + data["manual_block"] > 0:
                ax4.pie([data["manual_block"], data["auto_block"]], labels=["Manual", "Auto"], autopct="%1.0f%%", colors=[COLORS['accent_cyan'], COLORS['accent_orange']])
                ax4.set_title("Block Type", color=COLORS['accent_cyan'])
            else:
                empty_chart(ax4, "Block Type")
        elif tab_text == "Sources":
            fig, ax5 = plt.subplots(1, 1, figsize=(10, 4))
            fig.tight_layout(pad=3)
            if data["source_counts"]:
                labels = list(data["source_counts"].keys())
                values = [data["source_counts"][k] for k in labels]
                ax5.bar(labels, values, color=COLORS['accent_purple'])
                ax5.set_title("Source Frequency", color=COLORS['accent_cyan'])
                ax5.tick_params(axis="x", rotation=20)
            else:
                empty_chart(ax5, "Source Frequency")
        elif tab_text == "Activity":
            fig, (ax6, ax7) = plt.subplots(1, 2, figsize=(10, 4))
            fig.tight_layout(pad=3)
            if data["date_counts"]:
                dates = sorted(data["date_counts"].keys())
                values = [data["date_counts"][d] for d in dates]
                ax6.plot(dates, values, marker="o", color=COLORS['accent_cyan'])
                ax6.set_title("Activity Over Time", color=COLORS['accent_cyan'])
                ax6.tick_params(axis="x", rotation=20)
            else:
                empty_chart(ax6, "Activity Over Time")
            if data["scores"]:
                ax7.hist(data["scores"], bins=10, color=COLORS['accent_green'])
                ax7.set_title("Score Distribution", color=COLORS['accent_cyan'])
            else:
                empty_chart(ax7, "Score Distribution")
        else:
            return
        
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self._dashboard_figures.append(fig)
        self._dashboard_canvases.append(canvas)
        self._dashboard_rendered_tabs.add(tab_text)
    
    def _refresh_dashboard(self, force=False):
        if not hasattr(self, "dashboard_container"):
            return
        
        desired_state = self._dashboard_state()
        if (not force and self._dashboard_last_state == desired_state and 
            self._dashboard_notebook is not None and self._dashboard_data is not None and 
            not self._dashboard_data_loading):
            return
        
        self._dashboard_refresh_token += 1
        token = self._dashboard_refresh_token
        self._dashboard_data_loading = True
        self._dashboard_data = None
        self._dashboard_rendered_tabs = set()
        
        self._dashboard_cleanup_figures()
        for child in self.dashboard_container.winfo_children():
            child.destroy()
        self._dashboard_init_layout()
        
        threading.Thread(target=self._dashboard_load_data_worker, args=(token, desired_state), daemon=True).start()


# ================= MAIN ENTRY POINT =================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--block-url", default=None, help="Prefill blocking URL")
    args = parser.parse_args()
    
    root = tk.Tk()
    app = WebsiteBlockerApp(root)
    
    if args.block_url and hasattr(app, 'url_entry'):
        try:
            app.show_frame("blocking")
            app.url_entry.delete(0, tk.END)
            app.url_entry.insert(0, args.block_url)
        except:
            pass
    
    root.mainloop()
