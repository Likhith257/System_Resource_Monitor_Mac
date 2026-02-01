#!/bin/bash
# Setup auto-launch for Resource Monitor widget

APP_NAME="Resource Monitor"
PLIST_NAME="com.resourcemonitor.widget"
PLIST_PATH="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WIDGET_PATH="${SCRIPT_DIR}/widget.py"
PYTHON_PATH=$(which python3)

echo "Setting up auto-launch for Resource Monitor..."
echo "Widget path: $WIDGET_PATH"
echo "Python path: $PYTHON_PATH"

# Create the plist file
cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_NAME}</string>
    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON_PATH}</string>
        <string>${WIDGET_PATH}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StandardErrorPath</key>
    <string>/tmp/resource_monitor_error.log</string>
    <key>StandardOutPath</key>
    <string>/tmp/resource_monitor_out.log</string>
</dict>
</plist>
EOF

echo "Created launchd plist at: $PLIST_PATH"

# Load the launch agent
launchctl unload "$PLIST_PATH" 2>/dev/null
launchctl load "$PLIST_PATH"

if [ $? -eq 0 ]; then
    echo "✓ Auto-launch enabled successfully!"
    echo "The Resource Monitor widget will start automatically when you log in."
    echo ""
    echo "To disable auto-launch, run:"
    echo "  launchctl unload $PLIST_PATH"
    echo "  rm $PLIST_PATH"
else
    echo "✗ Failed to enable auto-launch"
    exit 1
fi
