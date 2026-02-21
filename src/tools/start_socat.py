#!/usr/bin/env python3
import sys
import platform
import subprocess
import shutil
import re


def check_dependencies():
    """Checks the operating system and if socat is installed."""
    os_name = platform.system()
    
    if not shutil.which("socat"):
        print("[-] Error: 'socat' is not installed.")
        if os_name == "Darwin":
            print("    Fix for Mac: brew install socat")
        elif os_name == "Linux":
            print("    Fix for Linux/Pi: sudo apt install socat")
        elif os_name == "Windows":
            print("    Fix for Windows: socat has poor native support (please use WSL).")
        else:
            print(f"    Please install socat for your OS ({os_name}).")
        sys.exit(1)
    
    return os_name


def main():
    os_name = check_dependencies()
    print(f"[*] OS detected: {os_name}")
    print("[*] Starting virtual serial tunnel...")
    
    cmd = ["socat", "-d", "-d", "pty,raw,echo=0", "pty,raw,echo=0"]
    
    try:
        # Popen runs the command in the background. socat writes logs to stderr.
        proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)
        
        ports = []
        # Read the output line by line until we find both ports
        while True:
            line = proc.stderr.readline()
            if not line and proc.poll() is not None:
                break
            
            # Look for "PTY is /dev/pts/X" or "PTY is /dev/ttys00X" (Mac)
            match = re.search(r"PTY is (\S+)", line)
            if match:
                ports.append(match.group(1))
                
            # As soon as we have both ends, print them nicely formatted
            if len(ports) == 2:
                print("\n" + "="*55)
                print("✅ VIRTUAL SERIAL TUNNEL ACTIVE")
                print("="*55)
                print(f"🔌 Port 1 (Add this to your growatt.cfg) : {ports[0]}")
                print(f"🔌 Port 2 (Start the simulator with this) : {ports[1]}")
                print("="*55)
                print("\nPress CTRL+C to close the tunnel.")
                break  # Exit the loop, we have our ports
        
        # Keep the script alive as long as socat is running
        proc.wait() 
        
    except KeyboardInterrupt:
        print("\n[*] Stopping virtual tunnel...")
        proc.terminate()
        sys.exit(0)
    except Exception as e:
        print(f"[-] An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()