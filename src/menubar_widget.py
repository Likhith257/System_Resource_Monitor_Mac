"""
System Resource Monitor - macOS Menu Bar Widget
Lightweight menu bar application showing system metrics
"""

import rumps
import time
from system_monitor import SystemMonitor


class ResourceMonitorMenuBar(rumps.App):
    """macOS Menu Bar Widget for System Monitoring"""
    
    def __init__(self):
        super(ResourceMonitorMenuBar, self).__init__(
            name="Resource Monitor",
            title="⚡ ---%",
            quit_button=None
        )
        
        # Initialize monitor
        self.monitor = SystemMonitor(history_size=30)
        
        # Menu items
        self.cpu_item = rumps.MenuItem("CPU: ---%")
        self.memory_item = rumps.MenuItem("Memory: ---%")
        self.disk_item = rumps.MenuItem("Disk: ---%")
        self.network_up_item = rumps.MenuItem("Upload: ---")
        self.network_down_item = rumps.MenuItem("Download: ---")
        self.battery_item = rumps.MenuItem("Battery: ---%")
        
        self.separator1 = rumps.separator
        self.separator2 = rumps.separator
        
        # Top processes - static items for now
        self.top_processes_item = rumps.MenuItem("Top Processes")
        
        # Actions
        self.open_dashboard_item = rumps.MenuItem("Open Dashboard", callback=self.open_dashboard)
        self.preferences_item = rumps.MenuItem("Preferences", callback=self.show_preferences)
        self.quit_item = rumps.MenuItem("Quit", callback=rumps.quit_application)
        
        # Build menu
        self.menu = [
            self.cpu_item,
            self.memory_item,
            self.disk_item,
            self.separator1,
            self.network_up_item,
            self.network_down_item,
            self.separator2,
            self.battery_item,
            rumps.separator,
            self.top_processes_item,
            rumps.separator,
            self.open_dashboard_item,
            self.preferences_item,
            rumps.separator,
            self.quit_item
        ]
        
        # Update interval (seconds)
        self.update_interval = 2
        
        # Start timer for updates (rumps built-in timer)
        self.timer = rumps.Timer(self.update_metrics, self.update_interval)
        self.timer.start()
    
    @rumps.clicked("Top Processes")
    def show_top_processes(self, _):
        """Show top processes in a notification"""
        cpu_procs = self.monitor.get_process_list(sort_by='cpu', limit=5)
        
        message = "Top CPU Processes:\n"
        for i, proc in enumerate(cpu_procs[:5], 1):
            message += f"{i}. {proc['name'][:20]}: {proc['cpu']:.1f}%\n"
        
        rumps.notification(
            title="Resource Monitor",
            subtitle="Process Information",
            message=message
        )
    
    def update_metrics(self, _=None):
        """Update all menu bar metrics"""
        try:
            # Get system data
            cpu_info = self.monitor.get_cpu_info()
            mem_info = self.monitor.get_memory_info()
            disk_info = self.monitor.get_disk_info()
            net_info = self.monitor.get_network_info()
            battery_info = self.monitor.get_battery_info()
            
            # Update title bar icon with CPU percentage
            cpu_percent = cpu_info['percent']
            if cpu_percent > 80:
                icon = "🔴"  # High usage
            elif cpu_percent > 50:
                icon = "🟡"  # Medium usage
            else:
                icon = "🟢"  # Low usage
            
            self.title = f"{icon} {cpu_percent:.0f}%"
            
            # Update CPU item
            cpu_text = f"CPU: {cpu_percent:.1f}%"
            cpu_cores = " | ".join([f"{c:.0f}%" for c in cpu_info['per_core'][:4]])  # First 4 cores
            if len(cpu_info['per_core']) > 4:
                cpu_cores += "..."
            self.cpu_item.title = f"{cpu_text} ({cpu_cores})"
            
            # Update Memory item
            mem_used = self.monitor.format_bytes(mem_info['used'])
            mem_total = self.monitor.format_bytes(mem_info['total'])
            self.memory_item.title = f"Memory: {mem_info['percent']:.1f}% ({mem_used} / {mem_total})"
            
            # Update Disk item
            disk_used = self.monitor.format_bytes(disk_info['used'])
            disk_total = self.monitor.format_bytes(disk_info['total'])
            disk_read = self.monitor.format_speed(disk_info['read_rate'])
            disk_write = self.monitor.format_speed(disk_info['write_rate'])
            self.disk_item.title = f"Disk: {disk_info['percent']:.1f}% | R: {disk_read} W: {disk_write}"
            
            # Update Network items
            self.network_up_item.title = f"Upload: {self.monitor.format_speed(net_info['sent_rate'])}"
            self.network_down_item.title = f"Download: {self.monitor.format_speed(net_info['recv_rate'])}"
            
            # Update Battery item
            if battery_info:
                status = "🔌" if battery_info['plugged'] else "🔋"
                time_left = ""
                if battery_info['time_left'] and not battery_info['plugged']:
                    hours = battery_info['time_left'] // 3600
                    minutes = (battery_info['time_left'] % 3600) // 60
                    time_left = f" ({hours}h {minutes}m)"
                self.battery_item.title = f"{status} Battery: {battery_info['percent']:.0f}%{time_left}"
            else:
                self.battery_item.title = "Battery: N/A"
                
        except Exception as e:
            print(f"Error updating metrics: {e}")
            import traceback
            traceback.print_exc()
    
    def open_dashboard(self, _):
        """Open the full GUI dashboard"""
        import subprocess
        import os
        
        # Get the path to gui.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        gui_path = os.path.join(current_dir, 'gui.py')
        
        # Launch dashboard in separate process
        try:
            subprocess.Popen(['python3', gui_path])
            rumps.notification(
                title="Resource Monitor",
                subtitle="Dashboard Opened",
                message="The full dashboard window has been launched."
            )
        except Exception as e:
            rumps.alert(
                title="Error",
                message=f"Could not open dashboard: {e}"
            )
    
    def show_preferences(self, _):
        """Show preferences dialog"""
        response = rumps.Window(
            title="Update Interval",
            message="Enter update interval in seconds:",
            default_text=str(self.update_interval),
            ok="Save",
            cancel="Cancel",
            dimensions=(200, 20)
        ).run()
        
        if response.clicked:
            try:
                new_interval = float(response.text)
                if 1 <= new_interval <= 60:
                    self.update_interval = new_interval
                    rumps.notification(
                        title="Preferences Updated",
                        subtitle="Update Interval Changed",
                        message=f"Now updating every {new_interval} seconds"
                    )
                else:
                    rumps.alert(
                        title="Invalid Value",
                        message="Update interval must be between 1 and 60 seconds"
                    )
            except ValueError:
                rumps.alert(
                    title="Invalid Value",
                    message="Please enter a valid number"
                )
    
    def cleanup(self):
        """Cleanup before quitting"""
        self.running = False
        if self.update_thread.is_alive():
            self.update_thread.join(timeout=2)


def main():
    """Main entry point for menu bar widget"""
    app = ResourceMonitorMenuBar()
    app.run()


if __name__ == '__main__':
    main()


def main():
    """Main entry point for menu bar widget"""
    try:
        app = ResourceMonitorMenuBar()
        app.run()
    except Exception as e:
        print(f"Failed to start menu bar widget: {e}")
        import traceback
        traceback.print_exc