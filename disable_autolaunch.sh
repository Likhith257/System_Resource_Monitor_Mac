#!/bin/bash
# Disable auto-launch for Resource Monitor widget

PLIST_NAME="com.resourcemonitor.widget"
PLIST_PATH="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"

echo "Disabling auto-launch for Resource Monitor..."

if [ -f "$PLIST_PATH" ]; then
    launchctl unload "$PLIST_PATH"
    rm "$PLIST_PATH"
    echo "✓ Auto-launch disabled successfully!"
else
    echo "Auto-launch was not enabled."
fi
