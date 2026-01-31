"""
System Resource Monitor - GUI Module
Real-time dashboard with graphs and metrics
"""

import tkinter as tk
from tkinter import ttk, font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time
from datetime import datetime
import sys
import os

# Add parent directory to path to import system_monitor
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.system_monitor import SystemMonitor


class ResourceMonitorGUI:
    """Main GUI application for system resource monitoring"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("System Resource Monitor")
        self.root.geometry("1200x800")
        
        # Initialize monitor
        self.monitor = SystemMonitor(history_size=60)
        self.running = True
        self.update_interval = 1000  # milliseconds
        
        # Configure style
        self.setup_style()
        
        # Create main layout
        self.create_layout()
        
        # Start monitoring
        self.update_data()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_style(self):
        """Configure GUI style"""
        style = ttk.Style()
        style.theme_use('aqua' if sys.platform == 'darwin' else 'clam')
        
        # Custom colors
        self.bg_color = '#1e1e1e'
        self.fg_color = '#ffffff'
        self.accent_color = '#007acc'
        self.warning_color = '#ff6b6b'
        self.success_color = '#51cf66'
        
        # Configure root
        self.root.configure(bg=self.bg_color)
    
    def create_layout(self):
        """Create the main GUI layout"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Overview tab
        self.overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.overview_frame, text='Overview')
        self.create_overview_tab()
        
        # Processes tab
        self.processes_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.processes_frame, text='Processes')
        self.create_processes_tab()
        
        # System Info tab
        self.info_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.info_frame, text='System Info')
        self.create_info_tab()
    
    def create_overview_tab(self):
        """Create the overview tab with graphs and metrics"""
        # Left panel - Metrics
        left_panel = tk.Frame(self.overview_frame, bg='#2d2d2d', width=300)
        left_panel.pack(side='left', fill='y', padx=5, pady=5)
        left_panel.pack_propagate(False)
        
        # CPU Section
        self.create_metric_section(left_panel, "CPU", "cpu")
        
        # Memory Section
        self.create_metric_section(left_panel, "Memory", "memory")
        
        # Disk Section
        self.create_metric_section(left_panel, "Disk", "disk")
        
        # Network Section
        self.create_metric_section(left_panel, "Network", "network")
        
        # Battery Section (if available)
        self.create_metric_section(left_panel, "Battery", "battery")
        
        # Right panel - Graphs
        right_panel = tk.Frame(self.overview_frame, bg='#2d2d2d')
        right_panel.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # Create matplotlib figures
        self.fig = Figure(figsize=(10, 8), facecolor='#2d2d2d')
        
        # CPU Graph
        self.ax_cpu = self.fig.add_subplot(3, 1, 1)
        self.ax_cpu.set_facecolor('#1e1e1e')
        self.ax_cpu.set_title('CPU Usage (%)', color='white', fontsize=10)
        self.ax_cpu.set_ylim(0, 100)
        self.ax_cpu.grid(True, alpha=0.3)
        self.cpu_line, = self.ax_cpu.plot([], [], color='#51cf66', linewidth=2)
        self.ax_cpu.tick_params(colors='white', labelsize=8)
        
        # Memory Graph
        self.ax_memory = self.fig.add_subplot(3, 1, 2)
        self.ax_memory.set_facecolor('#1e1e1e')
        self.ax_memory.set_title('Memory Usage (%)', color='white', fontsize=10)
        self.ax_memory.set_ylim(0, 100)
        self.ax_memory.grid(True, alpha=0.3)
        self.memory_line, = self.ax_memory.plot([], [], color='#339af0', linewidth=2)
        self.ax_memory.tick_params(colors='white', labelsize=8)
        
        # Network Graph
        self.ax_network = self.fig.add_subplot(3, 1, 3)
        self.ax_network.set_facecolor('#1e1e1e')
        self.ax_network.set_title('Network Usage (MB/s)', color='white', fontsize=10)
        self.ax_network.grid(True, alpha=0.3)
        self.network_line_up, = self.ax_network.plot([], [], color='#ff6b6b', linewidth=2, label='Upload')
        self.network_line_down, = self.ax_network.plot([], [], color='#51cf66', linewidth=2, label='Download')
        self.ax_network.legend(loc='upper right', fontsize=8)
        self.ax_network.tick_params(colors='white', labelsize=8)
        
        self.fig.tight_layout()
        
        # Embed matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_panel)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def create_metric_section(self, parent, title, metric_type):
        """Create a metric display section"""
        frame = tk.Frame(parent, bg='#3d3d3d', relief='raised', borderwidth=1)
        frame.pack(fill='x', padx=5, pady=5)
        
        # Title
        title_label = tk.Label(frame, text=title, bg='#3d3d3d', fg='white',
                               font=('Helvetica', 12, 'bold'))
        title_label.pack(anchor='w', padx=10, pady=(10, 5))
        
        # Percentage bar
        progress_frame = tk.Frame(frame, bg='#3d3d3d')
        progress_frame.pack(fill='x', padx=10, pady=5)
        
        progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=200)
        progress_bar.pack(fill='x')
        
        # Details label
        details_label = tk.Label(frame, text="", bg='#3d3d3d', fg='#cccccc',
                                font=('Helvetica', 9), justify='left')
        details_label.pack(anchor='w', padx=10, pady=(5, 10))
        
        # Store references
        setattr(self, f'{metric_type}_progress', progress_bar)
        setattr(self, f'{metric_type}_details', details_label)
    
    def create_processes_tab(self):
        """Create the processes tab with sortable table"""
        # Control panel
        control_frame = tk.Frame(self.processes_frame, bg='#2d2d2d')
        control_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(control_frame, text="Sort by:", bg='#2d2d2d', fg='white').pack(side='left', padx=5)
        
        self.sort_var = tk.StringVar(value='cpu')
        sort_options = ['cpu', 'memory', 'name']
        sort_menu = ttk.Combobox(control_frame, textvariable=self.sort_var,
                                 values=sort_options, state='readonly', width=10)
        sort_menu.pack(side='left', padx=5)
        
        tk.Label(control_frame, text="Limit:", bg='#2d2d2d', fg='white').pack(side='left', padx=5)
        
        self.limit_var = tk.StringVar(value='20')
        limit_spinbox = ttk.Spinbox(control_frame, from_=5, to=100, textvariable=self.limit_var,
                                    width=8)
        limit_spinbox.pack(side='left', padx=5)
        
        # Process table
        table_frame = tk.Frame(self.processes_frame, bg='#2d2d2d')
        table_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        columns = ('PID', 'Name', 'CPU %', 'Memory %', 'Status')
        self.process_tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                                         yscrollcommand=scrollbar.set)
        
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=150)
        
        self.process_tree.pack(fill='both', expand=True)
        scrollbar.config(command=self.process_tree.yview)
    
    def create_info_tab(self):
        """Create the system info tab"""
        info_text = tk.Text(self.info_frame, bg='#2d2d2d', fg='white',
                           font=('Courier', 10), wrap='word')
        info_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Get system info
        info = self.monitor.get_system_info()
        
        info_str = f"""
System Information
{'=' * 50}

Platform: {info['platform']}
Release: {info['platform_release']}
Version: {info['platform_version']}
Architecture: {info['architecture']}
Hostname: {info['hostname']}
Processor: {info['processor']}

Boot Time: {info['boot_time']}
Uptime: {info['uptime']}
        """
        
        info_text.insert('1.0', info_str)
        info_text.config(state='disabled')
    
    def update_data(self):
        """Update all data and GUI elements"""
        if not self.running:
            return
        
        # Get data
        cpu_info = self.monitor.get_cpu_info()
        mem_info = self.monitor.get_memory_info()
        disk_info = self.monitor.get_disk_info()
        net_info = self.monitor.get_network_info()
        battery_info = self.monitor.get_battery_info()
        
        # Update CPU
        self.cpu_progress['value'] = cpu_info['percent']
        cpu_details = f"{cpu_info['percent']:.1f}%\n"
        cpu_details += f"Cores: {cpu_info['cores']} / Threads: {cpu_info['threads']}\n"
        cpu_details += f"Frequency: {cpu_info['frequency']:.0f} MHz"
        self.cpu_details.config(text=cpu_details)
        
        # Update Memory
        self.memory_progress['value'] = mem_info['percent']
        mem_details = f"{mem_info['percent']:.1f}%\n"
        mem_details += f"Used: {self.monitor.format_bytes(mem_info['used'])}\n"
        mem_details += f"Available: {self.monitor.format_bytes(mem_info['available'])}"
        self.memory_details.config(text=mem_details)
        
        # Update Disk
        self.disk_progress['value'] = disk_info['percent']
        disk_details = f"{disk_info['percent']:.1f}%\n"
        disk_details += f"Read: {self.monitor.format_speed(disk_info['read_rate'])}\n"
        disk_details += f"Write: {self.monitor.format_speed(disk_info['write_rate'])}"
        self.disk_details.config(text=disk_details)
        
        # Update Network
        net_percent = min(100, (net_info['sent_rate'] + net_info['recv_rate']) / (1024 * 1024))
        self.network_progress['value'] = net_percent
        net_details = f"Up: {self.monitor.format_speed(net_info['sent_rate'])}\n"
        net_details += f"Down: {self.monitor.format_speed(net_info['recv_rate'])}\n"
        net_details += f"Total: {self.monitor.format_bytes(net_info['bytes_sent'] + net_info['bytes_recv'])}"
        self.network_details.config(text=net_details)
        
        # Update Battery
        if battery_info:
            self.battery_progress['value'] = battery_info['percent']
            batt_details = f"{battery_info['percent']:.1f}%\n"
            batt_details += f"Status: {'Charging' if battery_info['plugged'] else 'Discharging'}\n"
            if battery_info['time_left']:
                hours = battery_info['time_left'] // 3600
                minutes = (battery_info['time_left'] % 3600) // 60
                batt_details += f"Time left: {hours}h {minutes}m"
            self.battery_details.config(text=batt_details)
        
        # Update graphs
        self.update_graphs(cpu_info, mem_info, net_info)
        
        # Update process list
        self.update_process_list()
        
        # Schedule next update
        self.root.after(self.update_interval, self.update_data)
    
    def update_graphs(self, cpu_info, mem_info, net_info):
        """Update the matplotlib graphs"""
        # CPU graph
        x_data = list(range(len(cpu_info['history'])))
        self.cpu_line.set_data(x_data, cpu_info['history'])
        self.ax_cpu.set_xlim(0, max(60, len(cpu_info['history'])))
        
        # Memory graph
        x_data = list(range(len(mem_info['history'])))
        self.memory_line.set_data(x_data, mem_info['history'])
        self.ax_memory.set_xlim(0, max(60, len(mem_info['history'])))
        
        # Network graph
        if net_info['history']:
            x_data = list(range(len(net_info['history'])))
            upload_data = [s / (1024 * 1024) for s, r in net_info['history']]  # Convert to MB/s
            download_data = [r / (1024 * 1024) for s, r in net_info['history']]
            
            self.network_line_up.set_data(x_data, upload_data)
            self.network_line_down.set_data(x_data, download_data)
            self.ax_network.set_xlim(0, max(60, len(net_info['history'])))
            
            max_val = max(max(upload_data + download_data, default=1), 1)
            self.ax_network.set_ylim(0, max_val * 1.2)
        
        self.canvas.draw()
    
    def update_process_list(self):
        """Update the process list table"""
        # Clear existing items
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        
        # Get processes
        sort_by = self.sort_var.get()
        try:
            limit = int(self.limit_var.get())
        except ValueError:
            limit = 20
        
        processes = self.monitor.get_process_list(sort_by=sort_by, limit=limit)
        
        # Insert new data
        for proc in processes:
            self.process_tree.insert('', 'end', values=(
                proc['pid'],
                proc['name'],
                f"{proc['cpu']:.1f}",
                f"{proc['memory']:.1f}",
                proc['status']
            ))
    
    def on_closing(self):
        """Handle window closing"""
        self.running = False
        self.root.quit()
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ResourceMonitorGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
