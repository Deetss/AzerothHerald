#!/usr/bin/env python3
"""
Development runner for the Discord bot with auto-reload functionality.
This script watches for file changes and automatically restarts the bot.
"""

import os
import sys
import time
import subprocess
import signal
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class BotRestartHandler(FileSystemEventHandler):
    """Handler that restarts the bot when Python files change."""
    
    def __init__(self, restart_callback):
        self.restart_callback = restart_callback
        self.last_restart = 0
        self.restart_delay = 2  # Minimum seconds between restarts
        
    def on_modified(self, event):
        """Called when a file is modified."""
        if event.is_directory:
            return
            
        # Only restart for Python files
        if not event.src_path.endswith('.py'):
            return
            
        # Avoid rapid restarts
        current_time = time.time()
        if current_time - self.last_restart < self.restart_delay:
            return
            
        self.last_restart = current_time
        print(f"\n[RELOAD] File changed: {event.src_path}")
        print("[RELOAD] Restarting bot...")
        self.restart_callback()

class BotRunner:
    """Manages running and restarting the Discord bot."""
    
    def __init__(self, script_path="bot.py"):
        self.script_path = script_path
        self.process = None
        self.observer = None
        self.running = False
        
    def start_bot(self):
        """Start the bot process."""
        if self.process:
            self.stop_bot()
            
        try:
            print(f"[START] Starting bot: {self.script_path}")
            self.process = subprocess.Popen(
                [sys.executable, self.script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Start a thread to read and display output
            import threading
            output_thread = threading.Thread(target=self._read_output, daemon=True)
            output_thread.start()
            
            print(f"[OK] Bot started with PID: {self.process.pid}")
            
        except Exception as e:
            print(f"[ERROR] Failed to start bot: {e}")
            
    def stop_bot(self):
        """Stop the bot process."""
        if self.process:
            try:
                print("[STOP] Stopping bot...")
                if os.name == 'nt':  # Windows
                    self.process.terminate()
                else:  # Unix-like
                    self.process.send_signal(signal.SIGTERM)
                
                # Wait for graceful shutdown
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print("[WARN] Bot didn't stop gracefully, forcing shutdown...")
                    self.process.kill()
                    self.process.wait()
                    
                print("[OK] Bot stopped")
                
            except Exception as e:
                print(f"[ERROR] Error stopping bot: {e}")
            finally:
                self.process = None
                
    def restart_bot(self):
        """Restart the bot."""
        self.stop_bot()
        time.sleep(1)  # Brief pause between stop and start
        self.start_bot()
        
    def _read_output(self):
        """Read and display bot output in real-time."""
        if not self.process:
            return
            
        try:
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    print(f"[BOT] {line.rstrip()}")
                    
                # Check if process is still running
                if self.process.poll() is not None:
                    break
                    
        except Exception as e:
            print(f"[ERROR] Error reading bot output: {e}")
            
    def start_watching(self, watch_dir="."):
        """Start watching for file changes."""
        if self.observer:
            return
            
        watch_path = Path(watch_dir).resolve()
        print(f"[WATCH] Watching for changes in: {watch_path}")
        
        # Set up file watcher
        handler = BotRestartHandler(self.restart_bot)
        self.observer = Observer()
        self.observer.schedule(handler, str(watch_path), recursive=True)
        self.observer.start()
        
        print("[OK] File watcher started")
        
    def stop_watching(self):
        """Stop watching for file changes."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            print("[STOP] File watcher stopped")
            
    def run(self):
        """Main run loop."""
        print("Discord Bot Development Runner")
        print("=" * 40)
        print("Features:")
        print("  • Auto-restart on .py file changes")
        print("  • Real-time bot output")
        print("  • Graceful shutdown handling")
        print("=" * 40)
        
        try:
            # Start the bot
            self.start_bot()
            
            # Start watching for file changes
            self.start_watching()
            
            self.running = True
            print("\nBot is running in development mode!")
            print("Edit any .py file to automatically restart the bot")
            print("Press Ctrl+C to stop\n")
            
            # Keep the script running
            while self.running:
                time.sleep(1)
                
                # Check if bot process died unexpectedly
                if self.process and self.process.poll() is not None:
                    return_code = self.process.returncode
                    if return_code != 0:
                        print(f"\n[WARN] Bot exited with code {return_code}")
                        print("[RELOAD] Restarting in 3 seconds...")
                        time.sleep(3)
                        self.start_bot()
                        
        except KeyboardInterrupt:
            print("\n\n[STOP] Shutdown requested...")
            
        finally:
            self.running = False
            self.stop_watching()
            self.stop_bot()
            print("Development runner stopped")

def main():
    """Main entry point."""
    # Check if bot.py exists
    if not Path("bot.py").exists():
        print("[ERROR] bot.py not found in current directory")
        print("Make sure you're running this from the project root")
        sys.exit(1)
        
    # Check if watchdog is installed
    try:
        import watchdog
    except ImportError:
        print("[ERROR] watchdog library not found")
        print("Install it with: pip install watchdog")
        sys.exit(1)
        
    runner = BotRunner()
    runner.run()

if __name__ == "__main__":
    main()
