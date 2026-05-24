import threading
import time
import sys
import os
import psutil

# Initialize Windows Console to support ANSI escape codes
if os.name == 'nt':
    os.system('')

# Global State Variables
running = True
system_stats = {}

# ANSI Color Codes for Terminal UI
CLEAR_SCREEN = "\033[2J\033[H"
HIDE_CURSOR  = "\033[?25l"
SHOW_CURSOR  = "\033[?25h"
RESET        = "\033[0m"
BOLD         = "\033[1m"
CYAN         = "\033[36m"
GREEN        = "\033[32m"
YELLOW       = "\033[33m"
RED          = "\033[31m"
MAGENTA      = "\033[35m"

def get_color(percentage):
    """Returns a color code based on resource severity."""
    if percentage < 50:
        return GREEN
    elif percentage < 80:
        return YELLOW
    return RED

def make_bar(percentage:int, length=15):
    """Generates a colored ASCII progress bar."""
    color = get_color(percentage)
    colored_length = int(length * percentage // 100)
    filled_length = "█" * colored_length
    unfilled_length = "░" * (length - colored_length)
    bar = filled_length + unfilled_length
    return f"{color}[{bar}]{RESET}"

def system_metrics_loader():
    """Background thread to capture metrics instantly without blocking."""
    root_drive = "C:\\" if os.name == 'nt' else '/'
    
    # Establish baseline for CPU tracking
    psutil.cpu_percent(interval=None)
    
    while running:
        system_stats["cpu_usage"] = psutil.cpu_percent(interval=None)
        system_stats["ram_usage"] = psutil.virtual_memory().percent
        try:
            system_stats["disk_usage"] = psutil.disk_usage(root_drive).percent
        except Exception:
            system_stats["disk_usage"] = 0.0
            
        time.sleep(0.25) 

def screen_renderer():
    """Renders a structured, clean terminal interface at ~50 FPS."""
    # Wipe screen once and hide cursor for a premium UI feel
    sys.stdout.write(CLEAR_SCREEN + HIDE_CURSOR)
    sys.stdout.flush()

    while running:
        cpu = system_stats.get('cpu_usage', 0.0)
        ram = system_stats.get('ram_usage', 0.0)
        disk = system_stats.get('disk_usage', 0.0)
        
        # Build UI Strings
        header = f"{BOLD}{CYAN}⚡ SYSTEM PERFORMANCE DASHBOARD ⚡{RESET}\n"
        divider = f"{MAGENTA}=" * 70 + f"{RESET}\n"
        
        cpu_str  = f"  {BOLD}CPU Usage:{RESET}  {make_bar(cpu)} {get_color(cpu)}{cpu:5.1f}%{RESET}"
        ram_str  = f"  {BOLD}RAM Usage:{RESET}  {make_bar(ram)} {get_color(ram)}{ram:5.1f}%{RESET}"
        disk_str = f"  {BOLD}Disk Usage:{RESET} {make_bar(disk)} {get_color(disk)}{disk:5.1f}%{RESET}"
        
        footer = f"\n{divider}  {BOLD}Press [Ctrl + C] to exit safely.{RESET}"
        
        # Assemble frame
        full_frame = f"\033[H{header}{divider}\n{cpu_str}\n{ram_str}\n{disk_str}\n{footer}"
        
        sys.stdout.write(full_frame)
        sys.stdout.flush()

        time.sleep(0.02)

def main():
    global running

    # Start background tasks
    threading.Thread(target=system_metrics_loader, daemon=True).start()
    threading.Thread(target=screen_renderer, daemon=True).start()

    try:
        while running:
            time.sleep(0.1)
    except KeyboardInterrupt:
        running = False
    finally:
        # 1. FLUSH PENDING KEYSTROKES (Prevents spilled text on exit)
        try:
            if os.name == 'nt':
                import msvcrt
                # Read out every character stuck in Windows buffer
                while msvcrt.kbhit():
                    msvcrt.getch()
            else:
                import termios
                # Flush Linux/macOS input buffer completely
                termios.tcflush(sys.stdin, termios.TCIFLUSH)
        except Exception:
            pass # Fail-safe if imports/calls miss on niche terminals
        
        # Restore terminal defaults on exit
        sys.stdout.write(CLEAR_SCREEN + SHOW_CURSOR + "Dashboard closed. Goodbye!\n")
        sys.stdout.flush()
    
if __name__ == "__main__":
    main()
