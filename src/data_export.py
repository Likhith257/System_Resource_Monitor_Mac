"""
Data export and logging functionality
"""

import csv
import json
import os
from datetime import datetime
from typing import Dict, List


class DataExporter:
    """Export system metrics to various formats"""
    
    def __init__(self, export_dir: str = None):
        """Initialize exporter with directory path"""
        if export_dir is None:
            home = os.path.expanduser("~")
            export_dir = os.path.join(home, "Documents", "ResourceMonitor_Exports")
        
        self.export_dir = export_dir
        
        # Create export directory if it doesn't exist
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
    
    def export_to_csv(self, data_points: List[Dict], filename: str = None) -> str:
        """
        Export data points to CSV file
        
        Args:
            data_points: List of dictionaries containing metrics
            filename: Optional custom filename
        
        Returns:
            Path to the created file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resource_monitor_{timestamp}.csv"
        
        filepath = os.path.join(self.export_dir, filename)
        
        if not data_points:
            return filepath
        
        # Get all unique keys from data points
        fieldnames = set()
        for point in data_points:
            fieldnames.update(point.keys())
        fieldnames = sorted(list(fieldnames))
        
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_points)
        
        return filepath
    
    def export_to_json(self, data: Dict, filename: str = None) -> str:
        """
        Export data to JSON file
        
        Args:
            data: Dictionary containing metrics
            filename: Optional custom filename
        
        Returns:
            Path to the created file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resource_monitor_{timestamp}.json"
        
        filepath = os.path.join(self.export_dir, filename)
        
        with open(filepath, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=2, default=str)
        
        return filepath
    
    def create_snapshot(self, system_monitor) -> str:
        """
        Create a complete snapshot of current system state
        
        Args:
            system_monitor: SystemMonitor instance
        
        Returns:
            Path to the created JSON file
        """
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'cpu': system_monitor.get_cpu_info(),
            'memory': system_monitor.get_memory_info(),
            'disk': system_monitor.get_disk_info(),
            'network': system_monitor.get_network_info(),
            'battery': system_monitor.get_battery_info(),
            'system_info': system_monitor.get_system_info(),
            'top_processes': system_monitor.get_process_list(limit=20)
        }
        
        return self.export_to_json(snapshot, 
                                   f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")


class MetricsLogger:
    """Continuous logging of system metrics"""
    
    def __init__(self, log_dir: str = None, max_entries: int = 1000):
        """
        Initialize metrics logger
        
        Args:
            log_dir: Directory for log files
            max_entries: Maximum entries before creating new file
        """
        if log_dir is None:
            home = os.path.expanduser("~")
            log_dir = os.path.join(home, "Documents", "ResourceMonitor_Logs")
        
        self.log_dir = log_dir
        self.max_entries = max_entries
        self.current_log = []
        
        # Create log directory if it doesn't exist
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def log_metrics(self, cpu: float, memory: float, disk: float, 
                   network_up: float, network_down: float):
        """Log current metrics"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': round(cpu, 2),
            'memory_percent': round(memory, 2),
            'disk_percent': round(disk, 2),
            'network_upload_bps': round(network_up, 2),
            'network_download_bps': round(network_down, 2)
        }
        
        self.current_log.append(entry)
        
        # Auto-save if we hit max entries
        if len(self.current_log) >= self.max_entries:
            self.save_log()
    
    def save_log(self) -> str:
        """Save current log to file and clear buffer"""
        if not self.current_log:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"metrics_log_{timestamp}.csv"
        filepath = os.path.join(self.log_dir, filename)
        
        fieldnames = ['timestamp', 'cpu_percent', 'memory_percent', 'disk_percent',
                     'network_upload_bps', 'network_download_bps']
        
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.current_log)
        
        self.current_log.clear()
        return filepath
    
    def get_log_count(self) -> int:
        """Get number of entries in current log"""
        return len(self.current_log)
