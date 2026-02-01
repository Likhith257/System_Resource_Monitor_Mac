# System Resource Monitor for macOS

> **⚠️ Work in Progress**: This is an active development project. The Python implementation is functional, with native Swift/SwiftUI support planned for future releases.

A comprehensive, real-time system resource monitoring application for macOS built with Python. Monitor CPU, memory, disk, network, and battery usage with beautiful real-time graphs, smart alerts, and data export capabilities.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-WIP-yellow.svg)

## Features

### 📊 Real-Time Monitoring
- **CPU Usage**: Track overall and per-core CPU usage with live graphs
- **Memory**: Monitor RAM and swap usage with detailed statistics
- **Disk I/O**: Track read/write speeds and disk space usage
- **Network**: Monitor upload/download speeds in real-time
- **Battery**: Battery percentage, charging status, and time remaining

### 🔔 Smart Alerts
- **Threshold Monitoring**: Get notified when CPU, memory, or disk usage is high
- **Battery Warnings**: Low battery alerts when unplugged
- **Configurable Thresholds**: Customize alert levels for each metric
- **Alert Cooldown**: Prevents notification spam (5-minute intervals)

### 📈 Visualization
- Beautiful real-time line graphs using matplotlib
- Historical data tracking (60 data points by default)
- Color-coded metrics with progress bars
- Clean, dark-themed modern interface

### 💾 Data Export & Logging
- **Snapshot Export**: Save current system state to JSON
- **Continuous Logging**: Log metrics to CSV automatically
- **Historical Analysis**: Review past performance data
- **Export Directory**: `~/Documents/ResourceMonitor_Exports/`

### 🔍 Process Manager
- View top processes by CPU or memory usage
- Sortable process list with PID, name, CPU%, memory%, and status
- Quick access from menu bar

### ⚙️ Configuration
- **Persistent Settings**: Config saved to `~/.config/resource_monitor/config.json`
- **Customizable Update Interval**: 1-60 seconds
- **Toggle Features**: Enable/disable alerts and logging on the fly
- **Auto-launch**: Optional startup on login

## Installation

### Prerequisites
- Python 3.8 or higher
- macOS (tested on macOS 10.15+)

### Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd System_Resource_Monitor_Mac
```

2. **Create a virtual environment** (recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip3 install -r requirements.txt
```

## Usage

### Option 1: Menu Bar Widget (Recommended)

Run the lightweight menu bar widget that sits in your macOS status bar:
```bash
python3 widget.py
```

**Widget Features:**
- 🟢 Live CPU percentage in menu bar with color indicator
- 📊 Dropdown menu with all metrics (CPU, memory, disk, network, battery)
- 🔝 Top processes viewer
- 🔔 **Alert notifications** when resources exceed thresholds
- 💾 **Export snapshot** - save current system state
- 📝 **Toggle logging** - continuous metrics recording
- ⚡ **Enable/disable alerts** on demand
- 🚀 Launch full dashboard from menu

### Option 2: Full Dashboard

Run the complete GUI with graphs:
```bash
python3 main.py
```

**Dashboard Tabs:**
1. **Overview** - Real-time metrics with live graphs
2. **Processes** - Sortable process table
3. **System Info** - Platform details and uptime

### Auto-Launch Setup

To make the widget start automatically on login:
```bash
./setup_autolaunch.sh
```

To disable auto-launch:
```bash
./disable_autolaunch.sh
```

## Project Structure

```
System_Resource_Monitor_Mac/
├── main.py                   # Full dashboard entry point
├── widget.py                 # Menu bar widget entry point
├── setup_autolaunch.sh       # Enable auto-launch script
├── disable_autolaunch.sh     # Disable auto-launch script
├── src/
│   ├── system_monitor.py     # Core monitoring logic
│   ├── gui.py                # Full GUI implementation
│   ├── menubar_widget.py     # Menu bar widget
│   ├── alerts.py             # Alert system with thresholds
│   ├── data_export.py        # Export and logging functionality
│   └── config.py             # Configuration management
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
└── README.md                # This file
```

## Dependencies

- **psutil** (>=5.9.0): Cross-platform system and process utilities
- **matplotlib** (>=3.7.0): Plotting library for graphs
- **tkinter**: Built-in Python GUI framework
- **rumps** (>=0.4.0): macOS menu bar integration

## Configuration

### Alert Thresholds

Edit `~/.config/resource_monitor/config.json`:
```json
{
  "thresholds": {
    "cpu": 85.0,
    "memory": 90.0,
    "disk": 95.0,
    "battery": 15.0
  },
  "alert_enabled": true,
  "alert_cooldown": 300
}
```

### Update Interval

Via menu bar widget: Click → Preferences → Enter interval (1-60 seconds)

Or edit config:
```json
{
  "update_interval": 2
}
```

### File Locations

- **Snapshots**: `~/Documents/ResourceMonitor_Exports/`
- **Logs**: `~/Documents/ResourceMonitor_Logs/`
- **Config**: `~/.config/resource_monitor/config.json`

## Project Status & Roadmap

### Current Features (Python Implementation) ✅
- [x] Core monitoring functionality with psutil
- [x] Real-time GUI dashboard with graphs
- [x] Process manager with sorting
- [x] Menu bar widget integration
- [x] Smart alerts and threshold monitoring
- [x] Data export (JSON snapshots)
- [x] Continuous logging (CSV)
- [x] Configuration management
- [x] Auto-launch setup scripts

### Upcoming Features (Python) 🚧
- [ ] Custom color themes
- [ ] Per-app resource tracking
- [ ] Historical data viewer in GUI
- [ ] GPU monitoring (for M-series Macs)
- [ ] Network per-process tracking

### Future: Native macOS Version (Swift/SwiftUI) 🔮
- [ ] Complete Swift + SwiftUI rewrite
- [ ] Native menu bar app with system integration
- [ ] macOS Widgets (Desktop & Notification Center)
- [ ] Enhanced battery and thermal monitoring via IOKit
- [ ] Accessibility features and VoiceOver support
- [ ] App Store distribution

## Troubleshooting

### Permission Issues
Some metrics may require elevated permissions:
```bash
sudo python3 main.py
```

### matplotlib Backend Issues
If graphs don't display, install tkinter support:
```bash
brew install python-tk
```

### Widget Not Appearing
- Make sure rumps is installed: `pip3 install rumps`
- Check terminal for error messages
- Try restarting the app

### High CPU Usage
The monitor uses minimal CPU (~1-2%). If experiencing high usage:
- Increase update interval via Preferences
- Disable logging if enabled
- Check for other resource-intensive applications

## Development Status

**Current Phase**: Python Implementation (Active Development)  
**Next Phase**: Swift/SwiftUI Native App (Planned)

### Contributing

This is a work-in-progress project. Contributions welcome! Feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Share your experience

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [psutil](https://github.com/giampaolo/psutil) for system monitoring
- Graphs powered by [matplotlib](https://matplotlib.org/)
- Menu bar powered by [rumps](https://github.com/jaredks/rumps)
- Inspired by Activity Monitor (macOS) and htop

---

**Current Implementation**: Python (psutil + tkinter/rumps)  
**Planned Implementation**: Swift + SwiftUI (native macOS)
