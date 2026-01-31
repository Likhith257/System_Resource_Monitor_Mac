"""
System Resource Monitor - Core monitoring module
Collects system metrics using psutil
"""

import psutil
import platform
from datetime import datetime
from typing import Dict, List, Tuple


class SystemMonitor:
    """Core system monitoring class for collecting resource metrics"""
    
    def __init__(self, history_size: int = 60):
        """
        Initialize the system monitor
        
        Args:
            history_size: Number of historical data points to keep
        """
        self.history_size = history_size
        self.cpu_history = []
        self.memory_history = []
        self.network_history = []
        self.disk_io_history = []
        
        # Initialize network and disk counters
        self.last_net_io = psutil.net_io_counters()
        self.last_disk_io = psutil.disk_io_counters()
        self.last_check_time = datetime.now()
    
    def get_cpu_info(self) -> Dict:
        """Get CPU usage information"""
        cpu_percent = psutil.cpu_percent(interval=0.1, percpu=False)
        cpu_per_core = psutil.cpu_percent(interval=0.1, percpu=True)
        cpu_freq = psutil.cpu_freq()
        
        self.cpu_history.append(cpu_percent)
        if len(self.cpu_history) > self.history_size:
            self.cpu_history.pop(0)
        
        return {
            'percent': cpu_percent,
            'per_core': cpu_per_core,
            'cores': psutil.cpu_count(logical=False),
            'threads': psutil.cpu_count(logical=True),
            'frequency': cpu_freq.current if cpu_freq else 0,
            'history': self.cpu_history.copy()
        }
    
    def get_memory_info(self) -> Dict:
        """Get memory usage information"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        self.memory_history.append(mem.percent)
        if len(self.memory_history) > self.history_size:
            self.memory_history.pop(0)
        
        return {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'percent': mem.percent,
            'swap_total': swap.total,
            'swap_used': swap.used,
            'swap_percent': swap.percent,
            'history': self.memory_history.copy()
        }
    
    def get_disk_info(self) -> Dict:
        """Get disk usage and I/O information"""
        disk_usage = psutil.disk_usage('/')
        
        # Calculate disk I/O rates
        current_disk_io = psutil.disk_io_counters()
        current_time = datetime.now()
        time_delta = (current_time - self.last_check_time).total_seconds()
        
        if time_delta > 0 and self.last_disk_io:
            read_rate = (current_disk_io.read_bytes - self.last_disk_io.read_bytes) / time_delta
            write_rate = (current_disk_io.write_bytes - self.last_disk_io.write_bytes) / time_delta
        else:
            read_rate = 0
            write_rate = 0
        
        self.last_disk_io = current_disk_io
        
        return {
            'total': disk_usage.total,
            'used': disk_usage.used,
            'free': disk_usage.free,
            'percent': disk_usage.percent,
            'read_rate': read_rate,
            'write_rate': write_rate,
            'read_count': current_disk_io.read_count,
            'write_count': current_disk_io.write_count
        }
    
    def get_network_info(self) -> Dict:
        """Get network usage information"""
        current_net_io = psutil.net_io_counters()
        current_time = datetime.now()
        time_delta = (current_time - self.last_check_time).total_seconds()
        
        if time_delta > 0 and self.last_net_io:
            sent_rate = (current_net_io.bytes_sent - self.last_net_io.bytes_sent) / time_delta
            recv_rate = (current_net_io.bytes_recv - self.last_net_io.bytes_recv) / time_delta
        else:
            sent_rate = 0
            recv_rate = 0
        
        self.last_net_io = current_net_io
        self.last_check_time = current_time
        
        self.network_history.append((sent_rate, recv_rate))
        if len(self.network_history) > self.history_size:
            self.network_history.pop(0)
        
        return {
            'bytes_sent': current_net_io.bytes_sent,
            'bytes_recv': current_net_io.bytes_recv,
            'sent_rate': sent_rate,
            'recv_rate': recv_rate,
            'packets_sent': current_net_io.packets_sent,
            'packets_recv': current_net_io.packets_recv,
            'history': self.network_history.copy()
        }
    
    def get_battery_info(self) -> Dict:
        """Get battery information (macOS specific)"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    'percent': battery.percent,
                    'plugged': battery.power_plugged,
                    'time_left': battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
                }
        except (AttributeError, NotImplementedError):
            pass
        
        return None
    
    def get_process_list(self, sort_by: str = 'cpu', limit: int = 10) -> List[Dict]:
        """
        Get list of top processes
        
        Args:
            sort_by: Sort key ('cpu', 'memory', 'name')
            limit: Maximum number of processes to return
        """
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                pinfo = proc.info
                processes.append({
                    'pid': pinfo['pid'],
                    'name': pinfo['name'],
                    'cpu': pinfo['cpu_percent'] or 0,
                    'memory': pinfo['memory_percent'] or 0,
                    'status': pinfo['status']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort processes
        if sort_by == 'cpu':
            processes.sort(key=lambda x: x['cpu'], reverse=True)
        elif sort_by == 'memory':
            processes.sort(key=lambda x: x['memory'], reverse=True)
        elif sort_by == 'name':
            processes.sort(key=lambda x: x['name'].lower())
        
        return processes[:limit]
    
    def get_system_info(self) -> Dict:
        """Get general system information"""
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        return {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'hostname': platform.node(),
            'processor': platform.processor(),
            'boot_time': boot_time,
            'uptime': str(uptime).split('.')[0]  # Remove microseconds
        }
    
    @staticmethod
    def format_bytes(bytes_value: float) -> str:
        """Format bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"
    
    @staticmethod
    def format_speed(bytes_per_sec: float) -> str:
        """Format bytes per second to human readable format"""
        return f"{SystemMonitor.format_bytes(bytes_per_sec)}/s"
