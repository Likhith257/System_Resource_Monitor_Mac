# System Resource Monitor for macOS

> **⚠️ Work in Progress**: This is an active development project. The Python implementation is functional, with native Swift/SwiftUI support planned for future releases.

A comprehensive, real-time system resource monitoring application for macOS built with Python. Monitor CPU, memory, disk, network, and battery usage with beautiful real-time graphs and detailed metrics.

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
- **Battery**: Battery percentage, charging status, and time remaining (macOS)

### 📈 Visualization
- Beautiful real-time line graphs using matplotlib
- Historical data tracking (60 data points)
- Color-coded metrics with progress bars
- Clean, dark-themed modern interface

### 🔍 Process Manager
- View top processes by CPU or memory usage
- Sortable process list with PID, name, CPU%, memory%, and status
- Configurable number of processes to display

### ℹ️ System Information
- Platform and OS version
- Processor information
- System uptime and boot time
- Hostname and architecture

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
source venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Menu Bar Widget (Recommended)

Run the lightweight menu bar widget that sits in your macOS status bar:
```bash
python3 widget.py
```

Features:
- 🟢 Live CPU percentage in menu bar with color indicator
- 📊 Dropdown menu with all metrics (CPU, memory, disk, network, battery)
- 🔝 Top 5 CPU and memory consuming processes
- 🚀 Launch full dashboard from menu
- ⚙️ Adjustable update interval

### Option 2: Full Dashboard

Run the complete GUI with graphs:
```bash
python3 main.py
```

Or make it executable:
```bash
chmod +x main.py
./main.py
```

### Interface Overview

The application has three tabs:

1. **Overview Tab**
   - Left panel: Real-time metrics with progress bars
   - Right panel: Live graphs showing CPU, memory, and network trends
   Full dashboard entry point
├── widget.py               # Menu bar widget entry point
├── src/
│   ├── system_monitor.py   # Core monitoring logic
│   ├── gui.py              # Full GUI implementation
│   └── menubar_widget.py   # Menu bar widget
   - Adjustable limit for number of processes displayed

3. **System Info Tab**
   - Static system information
   - Platform details and uptime

## Project Structure

```
System_Resource_Monitor_Mac/
├── main.py                 # Entry point
├── src/
│   ├── system_monitor.py   # Core monitoring logic
│   └── gui.py              # GUI implementation
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── LICENSE                # MIT License
└── README.md              # This file
```

## Dependencies

- **psutil** (>=5.9.0): Cross-platform system and process utilit
- **rumps** (>=0.4.0): Ridiculously Uncomplicated macOS Python Statusbar apps (for menu bar widget)ies
- **matplotlib** (>=3.7.0): Plotting library for graphs
- **tkinter**: Built-in Python GUI framework (comes with Python)

## Technical Details

### Core Monitoring (`system_monitor.py`)

The `SystemMonitor` class provides:
- Real-time metric collection using `psutil`
- Historical data tracking with configurable buffer size
- Rate calculations for network and disk I/O
- Process enumeration and sorting
- Utility methods for formatting bytes and speeds

### GUI (`gui.py`)

Built with:
- **Tkinter**: Native GUI framework
- **matplotlib**: Embedded graphs with real-time updates
- **Threading-safe**: Updates at 1-second intervals
- **Responsive design**: Resizable windows and adaptive layouts

## Customization

### Change Update Interval

Edit `src/gui.py`:
```python
self.update_interval = 1000  # Change to desired milliseconds
```

### Adjust History Size

Edit `src/gui.py`:
```python
self.monitor = SystemMonitor(history_size=60)  # Change buffer size
```

### Modify Graph Colors

Edit the color scheme in `src/gui.py`:
```python
selProject Status & Roadmap

### Current Features (Python Implementation) ✅
- [x] Core monitoring functionality with psutil
- [x] Real-time GUI dashboard with graphs
- [x] Process manager with sorting
- [x] Menu bar widget integration
- [x] Live CPU, memory, disk, network, battery monitoring

### Upcoming Features (Python) 🚧
- [ ] System alerts and notifications for resource thresholds
- [ ] Historical data logging and export (CSV/JSON)
- [ ] Custom color themes
- [ ] Per-app resource tracking
- [ ] Configurable refresh rates
- [ ] Startup launch options

### Future: Native macOS Version (Swift/SwiftUI) 🔮
- [ ] Complete Swift + SwiftUI rewrite for native performance
- [ ] Native macOS menu bar app with system integration
- [ ] macOS Widgets (Desktop & Notification Center)
- [ ] Enhanced battery and thermal monitoring via IOKit
- [ ] Accessibility features and VoiceOver support
- [ ] Sandboxed App Store distribution
- [ ] M-series chip optimizationapp
- [ ] Widgets support
- [ ] Better battery and thermal monitoring
- [ ] Accessibility features

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

### Permission Issues
Some system metrics may require elevated permissions. If you encounter access errors, try:
```bash
sudo python3 main.py
```

### matplotlib Backend Issues
If graphs don't display, ensure you have tkinter support:
```bash
# On macOS with Homebrew Python
brew install python-tk
```

### High CPU Usage
The monitoring itself uses minimal CPU (~1-2%). If you experience high usage:
- Increase the update interval
- Reduce history buffer size
## Development Status

**Current Phase**: Python Implementation (Active Development)  
**Next Phase**: Swift/SwiftUI Native App (Planned)

This project is currently in active development. The Python version is functional and being enhanced with additional features. A native Swift implementation is planned for the future to provide better macOS integration and performance.

### Contributing

This is a work-in-progress project. Contributions, suggestions, and feedback are welcome! Feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Share your experience using the tool

---

**Current Implementation**: Python (psutil + tkinter/rumps)  
**Planned Implementation**: Swift + SwiftUI (native macOS)

## Acknowledgments

- Built with [psutil](https://github.com/giampaolo/psutil) for cross-platform system monitoring
- Graphs powered by [matplotlib](https://matplotlib.org/)
- Inspired by Activity Monitor (macOS) and htop

---

**Note**: This is the Python implementation. A native macOS version using Swift is planned for future development.