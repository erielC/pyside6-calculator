#!/bin/bash
# Professional QuESt DMG Builder
# Creates a beautiful installer DMG with custom background and icons

set -e

echo "════════════════════════════════════════"
echo "QuESt Professional DMG Builder"
echo "════════════════════════════════════════"
echo ""

# Configuration
APP_NAME="QuESt"
VERSION="2.0"
DMG_NAME="QuESt-${VERSION}-Installer"
BUILD_DIR="dmg_build"
CONTENTS_DIR="$BUILD_DIR/contents"
RESOURCES_DIR="$BUILD_DIR/resources"
INSTALLER_APP="$CONTENTS_DIR/Install QuESt.app"

# Clean previous builds
echo "[1/7] Cleaning previous builds..."
rm -rf "$BUILD_DIR"
rm -f "${DMG_NAME}.dmg"
mkdir -p "$CONTENTS_DIR"
mkdir -p "$RESOURCES_DIR"
echo "✓ Build directory prepared"
echo ""

# Step 2: Create Installer.app bundle
echo "[2/7] Creating Installer application..."

# First compile the AppleScript
osacompile -o "$INSTALLER_APP" QuESt_Installer.applescript

# Create Info.plist to replace the default one
cat > "$INSTALLER_APP/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>applet</string>
    <key>CFBundleIdentifier</key>
    <string>gov.sandia.quest.installer</string>
    <key>CFBundleName</key>
    <string>QuESt Installer</string>
    <key>CFBundleVersion</key>
    <string>2.0</string>
    <key>CFBundleShortVersionString</key>
    <string>2.0</string>
    <key>CFBundleIconFile</key>
    <string>applet</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSUIElement</key>
    <false/>
</dict>
</plist>
EOF

# Ensure Resources directory exists
mkdir -p "$INSTALLER_APP/Contents/Resources"

# Copy backend script
cp install_quest_backend.sh "$INSTALLER_APP/Contents/Resources/"
chmod +x "$INSTALLER_APP/Contents/Resources/install_quest_backend.sh"

echo "✓ Installer app created"
echo ""

# Step 3: Create DMG background image
echo "[3/7] Creating DMG background..."
cat > "$RESOURCES_DIR/create_background.py" << 'PYTHON'
from PIL import Image, ImageDraw, ImageFont
import os

# Create a beautiful gradient background
width, height = 800, 600
background = Image.new('RGB', (width, height), '#F5F5F7')  # Apple-style light gray
draw = ImageDraw.Draw(background)

# Add gradient effect (subtle)
for y in range(height):
    gray_value = int(245 - (y / height) * 10)
    color = (gray_value, gray_value, gray_value + 2)
    draw.line([(0, y), (width, y)], fill=color)

# Add subtle grid pattern
grid_color = (235, 235, 237)
for x in range(0, width, 40):
    draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
for y in range(0, height, 40):
    draw.line([(0, y), (width, y)], fill=grid_color, width=1)

# Add text
try:
    # Try to use system font
    title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
    subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()

# Title
text = "QuESt 2.0"
bbox = draw.textbbox((0, 0), text, font=title_font)
text_width = bbox[2] - bbox[0]
draw.text(((width - text_width) // 2, 50), text, fill='#1D1D1F', font=title_font)

# Subtitle
subtitle = "Energy Storage Analytics Platform"
bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
text_width = bbox[2] - bbox[0]
draw.text(((width - text_width) // 2, 110), subtitle, fill='#86868B', font=subtitle_font)

# Installation instructions
instruction_font = subtitle_font
instructions = [
    "",
    "To install QuESt:",
    "1. Double-click 'Install QuESt' below",
    "2. Follow the installation wizard",
    "3. Choose your preferences",
    "",
    "Installation takes 5-15 minutes"
]

y_offset = 450
for line in instructions:
    bbox = draw.textbbox((0, 0), line, font=instruction_font)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, y_offset), line, fill='#1D1D1F', font=instruction_font)
    y_offset += 30

# Save
background.save('dmg_background.png')
print("✓ Background created: dmg_background.png")
PYTHON

# Try to create background with Python PIL
if command -v python3 &> /dev/null && python3 -c "import PIL" 2>/dev/null; then
    cd "$RESOURCES_DIR"
    python3 create_background.py
    cd - > /dev/null
    cp "$RESOURCES_DIR/dmg_background.png" "$BUILD_DIR/background.png"
    echo "✓ Custom background created"
else
    echo "⊘ PIL not available, using default background"
    # Create a simple colored background as fallback
    # (This would normally be done with sips or another tool)
fi
echo ""

# Step 4: Create README and documentation
echo "[4/7] Creating documentation files..."

cat > "$CONTENTS_DIR/README.html" << 'HTML'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>QuESt 2.0 - README</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            color: #333;
        }
        h1 {
            color: #1D1D1F;
            border-bottom: 3px solid #0071E3;
            padding-bottom: 10px;
        }
        h2 {
            color: #0071E3;
            margin-top: 30px;
        }
        .logo {
            text-align: center;
            font-size: 48px;
            color: #0071E3;
            margin: 20px 0;
        }
        .box {
            background: #F5F5F7;
            border-left: 4px solid #0071E3;
            padding: 15px;
            margin: 20px 0;
        }
        code {
            background: #F5F5F7;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'SF Mono', Monaco, monospace;
        }
        .button {
            display: inline-block;
            background: #0071E3;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 8px;
            margin: 10px 5px;
        }
        .warning {
            background: #FFF3CD;
            border-left: 4px solid #FFC107;
        }
    </style>
</head>
<body>
    <div class="logo">⚡ QuESt 2.0</div>
    
    <h1>Energy Storage Analytics Platform</h1>
    
    <p>Welcome to QuESt! This installer will set up everything you need to run QuESt on your Mac.</p>
    
    <div class="box">
        <h2>📋 What Gets Installed</h2>
        <ul>
            <li>Python 3.9 (via Homebrew)</li>
            <li>Git version control</li>
            <li>QuESt platform and dependencies</li>
            <li>GLPK solver (optional, recommended)</li>
            <li>Desktop shortcut (optional)</li>
        </ul>
    </div>
    
    <h2>🚀 Installation Steps</h2>
    <ol>
        <li>Double-click <strong>"Install QuESt"</strong> in the DMG window</li>
        <li>Choose installation location:
            <ul>
                <li><strong>Home Directory</strong> (Recommended) - No admin password needed</li>
                <li><strong>Applications Folder</strong> - May require admin password</li>
                <li><strong>Custom Location</strong> - Choose your own folder</li>
            </ul>
        </li>
        <li>Choose whether to install GLPK solver (recommended)</li>
        <li>Choose whether to create desktop shortcut</li>
        <li>Wait for installation to complete (5-15 minutes)</li>
    </ol>
    
    <div class="box warning">
        <h2>⚠️ First Launch Security</h2>
        <p>Since this installer is not signed with an Apple Developer certificate, you'll see a security warning on first launch:</p>
        <ol>
            <li><strong>Right-click</strong> on "Install QuESt"</li>
            <li>Select <strong>"Open"</strong></li>
            <li>Click <strong>"Open"</strong> in the dialog</li>
        </ol>
        <p>This is normal and only needed once.</p>
    </div>
    
    <h2>💻 System Requirements</h2>
    <ul>
        <li>macOS 10.15 (Catalina) or later</li>
        <li>Intel or Apple Silicon (M1/M2/M3) Mac</li>
        <li>~500 MB disk space</li>
        <li>Internet connection</li>
    </ul>
    
    <h2>📚 After Installation</h2>
    
    <p><strong>Launch QuESt:</strong></p>
    <ul>
        <li>Double-click Desktop shortcut (if created)</li>
        <li>Or: <code>~/Applications/QuESt/QuESt.command</code></li>
    </ul>
    
    <p><strong>Update QuESt:</strong></p>
    <ul>
        <li>Double-click: <code>~/Applications/QuESt/Update QuESt.command</code></li>
    </ul>
    
    <p><strong>Uninstall QuESt:</strong></p>
    <ul>
        <li>Double-click: <code>~/Applications/QuESt/Uninstall QuESt.command</code></li>
    </ul>
    
    <h2>🔗 GLPK Solver Information</h2>
    
    <p>GLPK (GNU Linear Programming Kit) is required for optimization features in QuESt.</p>
    
    <p>If you chose not to install it during setup, you can:</p>
    <ul>
        <li><strong>Install via Homebrew:</strong> <code>brew install glpk</code></li>
        <li><strong>Download manually:</strong> <a href="http://winglpk.sourceforge.net/">http://winglpk.sourceforge.net/</a></li>
        <li><strong>Official GLPK site:</strong> <a href="https://www.gnu.org/software/glpk/">https://www.gnu.org/software/glpk/</a></li>
    </ul>
    
    <h2>❓ Support & Documentation</h2>
    
    <p>
        <a href="https://github.com/sandialabs/snl-quest" class="button">GitHub Repository</a>
        <a href="https://github.com/sandialabs/snl-quest/issues" class="button">Report Issues</a>
    </p>
    
    <p><strong>Email:</strong> tunguy@sandia.gov</p>
    
    <h2>🏛️ About</h2>
    <p>QuESt is developed by <strong>Sandia National Laboratories</strong> and is open-source software for energy storage simulation and analysis.</p>
    
    <hr style="margin: 40px 0; border: none; border-top: 1px solid #D1D1D6;">
    
    <p style="text-align: center; color: #86868B;">
        © 2024 Sandia National Laboratories<br>
        QuESt 2.0 Installer
    </p>
</body>
</html>
HTML

echo "✓ Documentation created"
echo ""

# Step 5: Create the DMG
echo "[5/7] Creating DMG image..."

# Create temporary DMG
hdiutil create -volname "QuESt 2.0" \
               -srcfolder "$CONTENTS_DIR" \
               -ov \
               -format UDRW \
               -size 100m \
               "$BUILD_DIR/temp.dmg"

echo "✓ DMG created"
echo ""

# Step 6: Mount and customize
echo "[6/7] Customizing DMG appearance..."

# Unmount if already mounted
MOUNT_POINT="/Volumes/QuESt 2.0"
if [ -d "$MOUNT_POINT" ]; then
    hdiutil detach "$MOUNT_POINT" -force 2>/dev/null || true
    sleep 1
fi

# Mount DMG as read-write
DEV_NAME=$(hdiutil attach "$BUILD_DIR/temp.dmg" -readwrite -noverify -noautoopen | grep "/Volumes/QuESt 2.0" | awk '{print $1}')
sleep 2

# Enable writing
if [ -n "$DEV_NAME" ]; then
    echo "  Mounted at: $MOUNT_POINT"
    
    # Copy background if it exists
    if [ -f "$BUILD_DIR/background.png" ]; then
        mkdir -p "$MOUNT_POINT/.background" 2>/dev/null || true
        cp "$BUILD_DIR/background.png" "$MOUNT_POINT/.background/background.png" 2>/dev/null || true
    fi
else
    echo "  Warning: Could not mount DMG for customization"
fi

# Create AppleScript to set up the DMG window
cat > "$BUILD_DIR/customize.applescript" << 'APPLESCRIPT'
tell application "Finder"
    tell disk "QuESt 2.0"
        open
        set current view of container window to icon view
        set toolbar visible of container window to false
        set statusbar visible of container window to false
        set the bounds of container window to {100, 100, 900, 700}
        
        set viewOptions to the icon view options of container window
        set arrangement of viewOptions to not arranged
        set icon size of viewOptions to 128
        set background picture of viewOptions to file ".background:background.png"
        
        -- Position items
        set position of item "Install QuESt.app" to {250, 300}
        set position of item "README.html" to {550, 300}
        
        close
        open
        update without registering applications
        delay 2
    end tell
end tell
APPLESCRIPT

osascript "$BUILD_DIR/customize.applescript" 2>/dev/null || echo "  Note: Could not fully customize appearance"

# Set permissions
chmod -Rf go-w "$MOUNT_POINT" 2>/dev/null || true
sync
sync

# Unmount
echo "  Unmounting DMG..."
hdiutil detach "$MOUNT_POINT" -force 2>/dev/null || hdiutil detach "$DEV_NAME" -force 2>/dev/null || true
sleep 2

echo "✓ DMG customized"
echo ""

# Step 7: Convert to final compressed DMG
echo "[7/7] Compressing final DMG..."

hdiutil convert "$BUILD_DIR/temp.dmg" \
                -format UDZO \
                -imagekey zlib-level=9 \
                -o "${DMG_NAME}.dmg"

# Clean up
rm -rf "$BUILD_DIR"

DMG_SIZE=$(du -h "${DMG_NAME}.dmg" | cut -f1)

echo "✓ DMG compressed"
echo ""

echo "════════════════════════════════════════"
echo "✓ Professional DMG Created!"
echo "════════════════════════════════════════"
echo ""
echo "File: ${DMG_NAME}.dmg"
echo "Size: $DMG_SIZE"
echo ""
echo "Contents:"
echo "  • Install QuESt.app - GUI installer"
echo "  • README.html - Complete documentation"
echo ""
echo "To test:"
echo "  open ${DMG_NAME}.dmg"
echo ""
echo "The DMG includes:"
echo "  ✓ Professional appearance"
echo "  ✓ Custom background"
echo "  ✓ Interactive installer"
echo "  ✓ Complete documentation"
echo "  ✓ Installation options"
echo "  ✓ GLPK information"
echo ""