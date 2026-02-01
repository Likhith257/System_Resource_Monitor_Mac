"""
System Resource Monitor - macOS Menu Bar Widget
"""
import rumps
from system_monitor import SystemMonitor
from config import Config
from data_export import DataExporter, MetricsLogger
from alerts import AlertManager

class ResourceMonitorMenuBar(rumps.App):
    def __init__(self):
        super(ResourceMonitorMenuBar, self).__init__(name="Resource Monitor", title="⚡ ---% 🧠 ---%", quit_button=None)
        self.config = Config()
        self.monitor = SystemMonitor(history_size=60)
        self.alert_manager = AlertManager()
        self.exporter = DataExporter()
        self.logger = None
        
        # Create menu items
        self.cpu_item = rumps.MenuItem("⚡ CPU: ---%")
        self.memory_item = rumps.MenuItem("🧠 Memory: ---%")
        self.disk_item = rumps.MenuItem("💾 Disk: ---%")
        self.network_up = rumps.MenuItem("⬆️  Upload: ---")
        self.network_down = rumps.MenuItem("⬇️  Download: ---")
        
        self.menu = [
            self.cpu_item,
            self.memory_item,
            self.disk_item,
            rumps.separator,
            self.network_up,
            self.network_down,
        ]
        
        # Initial update
        self.update_metrics(None)
        
        # Timer for continuous updates
        self.update_timer = rumps.Timer(self.update_metrics, 1)
        self.update_timer.start()
    
    def update_metrics(self, sender):
        """Update menu bar with real metrics"""
        try:
            # Get all data
            cpu = self.monitor.get_cpu_info()
            mem = self.monitor.get_memory_info()
            disk = self.monitor.get_disk_info()
            net = self.monitor.get_network_info()
            
            cpu_pct = cpu['percent']
            mem_pct = mem['percent']
            
            # Update menu bar title
            self.title = f"⚡{cpu_pct:.0f}% 🧠{mem_pct:.0f}%"
            
            # Update menu items
            cpu_icon = "🔴" if cpu_pct > 80 else "🟡" if cpu_pct > 50 else "🟢"
            self.cpu_item.title = f"⚡ CPU: {cpu_pct:.1f}% {cpu_icon}"
            self.memory_item.title = f"🧠 Memory: {mem_pct:.1f}%"
            self.disk_item.title = f"💾 Disk: {disk['percent']:.1f}%"
            self.network_up.title = f"⬆️  Upload: {self.monitor.format_speed(net['sent_rate'])}"
            self.network_down.title = f"⬇️  Download: {self.monitor.format_speed(net['recv_rate'])}"
        except Exception as e:
            print(f"Error updating metrics: {e}")

def main():
    app = ResourceMonitorMenuBar()
    app.run()

if __name__ == '__main__': main()
