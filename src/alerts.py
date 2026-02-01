"""
Alert system for monitoring thresholds
"""

import time
from typing import Dict, Callable
from datetime import datetime


class AlertManager:
    """Manages alerts and notifications for resource thresholds"""
    
    def __init__(self):
        self.thresholds = {
            'cpu': 85.0,
            'memory': 90.0,
            'disk': 95.0,
            'battery': 15.0  # Low battery warning
        }
        
        # Cooldown to prevent alert spam (seconds)
        self.alert_cooldown = 300  # 5 minutes
        self.last_alerts = {}
        
        # Alert callbacks
        self.alert_callbacks = []
    
    def set_threshold(self, metric: str, value: float):
        """Set threshold for a metric"""
        if metric in self.thresholds:
            self.thresholds[metric] = value
    
    def get_threshold(self, metric: str) -> float:
        """Get threshold for a metric"""
        return self.thresholds.get(metric, 0)
    
    def register_callback(self, callback: Callable):
        """Register a callback for alerts"""
        self.alert_callbacks.append(callback)
    
    def check_thresholds(self, cpu_percent: float, mem_percent: float, 
                        disk_percent: float, battery_info: Dict = None):
        """Check if any metrics exceed thresholds"""
        alerts = []
        current_time = time.time()
        
        # Check CPU
        if cpu_percent > self.thresholds['cpu']:
            if self._should_alert('cpu', current_time):
                alerts.append({
                    'type': 'cpu',
                    'level': 'warning' if cpu_percent < 95 else 'critical',
                    'title': 'High CPU Usage',
                    'message': f'CPU usage is at {cpu_percent:.1f}%',
                    'value': cpu_percent
                })
        
        # Check Memory
        if mem_percent > self.thresholds['memory']:
            if self._should_alert('memory', current_time):
                alerts.append({
                    'type': 'memory',
                    'level': 'warning' if mem_percent < 95 else 'critical',
                    'title': 'High Memory Usage',
                    'message': f'Memory usage is at {mem_percent:.1f}%',
                    'value': mem_percent
                })
        
        # Check Disk
        if disk_percent > self.thresholds['disk']:
            if self._should_alert('disk', current_time):
                alerts.append({
                    'type': 'disk',
                    'level': 'critical',
                    'title': 'Low Disk Space',
                    'message': f'Disk usage is at {disk_percent:.1f}%',
                    'value': disk_percent
                })
        
        # Check Battery (low battery)
        if battery_info and not battery_info.get('plugged', True):
            battery_percent = battery_info.get('percent', 100)
            if battery_percent < self.thresholds['battery']:
                if self._should_alert('battery', current_time):
                    alerts.append({
                        'type': 'battery',
                        'level': 'warning',
                        'title': 'Low Battery',
                        'message': f'Battery is at {battery_percent:.0f}%',
                        'value': battery_percent
                    })
        
        # Trigger callbacks for all alerts
        for alert in alerts:
            for callback in self.alert_callbacks:
                try:
                    callback(alert)
                except Exception as e:
                    print(f"Error in alert callback: {e}")
        
        return alerts
    
    def _should_alert(self, metric: str, current_time: float) -> bool:
        """Check if enough time has passed since last alert"""
        last_time = self.last_alerts.get(metric, 0)
        if current_time - last_time >= self.alert_cooldown:
            self.last_alerts[metric] = current_time
            return True
        return False
    
    def reset_cooldown(self, metric: str = None):
        """Reset alert cooldown for a metric or all metrics"""
        if metric:
            self.last_alerts[metric] = 0
        else:
            self.last_alerts.clear()
