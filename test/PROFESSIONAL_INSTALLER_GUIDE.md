# QuESt Professional Mac Installer - Build Guide

This creates a **professional, user-friendly DMG installer** with:
- ✅ GUI installer with dialog boxes
- ✅ Installation location selection
- ✅ GLPK install option with download link
- ✅ Desktop shortcut option
- ✅ Custom DMG background
- ✅ Professional documentation
- ✅ Beautiful presentation

## What Users See

### 1. Opening the DMG
```
QuESt 2.0/
├── Install QuESt.app  (128x128 icon, centered)
└── README.html        (Documentation)
```

### 2. Installation Wizard Dialogs

**Welcome Screen:**
```
┌─────────────────────────────────────┐
│       QuESt 2.0 Installer           │
├─────────────────────────────────────┤
│ Welcome to QuESt 2.0!              │
│                                     │
│ This installer will:                │
│ • Install Python 3.9 and Git       │
│ • Download and configure QuESt     │
│ • Optionally install GLPK solver   │
│ • Create desktop shortcuts          │
│                                     │
│          [Cancel] [Continue]        │
└─────────────────────────────────────┘
```

**Installation Location:**
```
┌─────────────────────────────────────┐
│    Installation Location            │
├─────────────────────────────────────┤
│ Where would you like to install?    │
│                                     │
│ ○ Home Directory (Recommended)     │
│ ○ Applications Folder              │
│ ○ Custom Location                  │
│                                     │
│              [Back] [Continue]      │
└─────────────────────────────────────┘
```

**GLPK Option:**
```
┌─────────────────────────────────────┐
│         Install GLPK Solver?        │
├─────────────────────────────────────┤
│ GLPK is required for optimization.  │
│                                     │
│ • Recommended for most users       │
│ • Adds ~10 MB to installation      │
│ • Can be installed later           │
│                                     │
│ If you choose not to install now:   │
│ http://winglpk.sourceforge.net/     │
│                                     │
│        [Skip GLPK] [Install GLPK]  │
└─────────────────────────────────────┘
```

**Desktop Shortcut:**
```
┌─────────────────────────────────────┐
│      Create Desktop Shortcut?       │
├─────────────────────────────────────┤
│ A shortcut will be added to your   │
│ Desktop for quick access to QuESt.  │
│                                     │
│              [No] [Yes]             │
└─────────────────────────────────────┘
```

**Confirmation:**
```
┌─────────────────────────────────────┐
│        Ready to Install QuESt       │
├─────────────────────────────────────┤
│ Installation Location:              │
│   ~/Applications/QuESt              │
│                                     │
│ GLPK Solver: Yes                   │
│ Desktop Shortcut: Yes              │
│                                     │
│ Installation will take 5-15 minutes │
│ Internet connection required        │
│                                     │
│            [Back] [Install]         │
└─────────────────────────────────────┘
```

## Building the Installer

### Prerequisites

1. **macOS** (to build)
2. **Xcode Command Line Tools:**
   ```bash
   xcode-select --install
   ```
3. **Python 3 with PIL** (for custom background):
   ```bash
   pip3 install Pillow
   ```

### File Structure

```
quest-pro-installer/
├── QuESt_Installer.applescript    # GUI installer
├── install_quest_backend.sh        # Backend installation script
└── build_professional_dmg.sh       # DMG builder
```

### Build Steps

1. **Download all files** to `quest-pro-installer/`

2. **Make scripts executable:**
   ```bash
   chmod +x install_quest_backend.sh
   chmod +x build_professional_dmg.sh
   ```

3. **Build the DMG:**
   ```bash
   ./build_professional_dmg.sh
   ```

4. **Result:**
   ```
   QuESt-2.0-Installer.dmg created! (~2-5 MB)
   ```

### Build Process

The builder:
1. ✓ Cleans previous builds
2. ✓ Creates installer app bundle
3. ✓ Generates custom background image
4. ✓ Creates beautiful HTML documentation
5. ✓ Builds temporary DMG
6. ✓ Customizes appearance & layout
7. ✓ Compresses final DMG

## Testing the Installer

```bash
# Open the DMG
open QuESt-2.0-Installer.dmg

# The DMG window appears with custom background
# Double-click "Install QuESt.app"
# Follow the wizard
```

## Customization Options

### Change App Icon

1. Create or download a `.icns` icon file
2. Name it `AppIcon.icns`
3. Before building, run:
   ```bash
   cp AppIcon.icns quest-pro-installer/
   # Edit build_professional_dmg.sh to copy it
   ```

### Customize Background

Edit `build_professional_dmg.sh`, modify the Python script section:
```python
# Change colors
background = Image.new('RGB', (width, height), '#YOUR_COLOR')

# Change text
text = "Your Custom Title"
subtitle = "Your Subtitle"
```

### Change DMG Window Size

In `build_professional_dmg.sh`, edit the AppleScript section:
```applescript
set the bounds of container window to {100, 100, 900, 700}
#                                      left top  right bottom
```

### Modify Installation Defaults

In `QuESt_Installer.applescript`:

**Change default location:**
```applescript
# Line ~20
set installPath to (path to applications folder as text) & "QuESt"
```

**Auto-select GLPK:**
```applescript
# Line ~45
set installGLPK to true  # Skip dialog
```

### Add More Dialogs

Add to `QuESt_Installer.applescript`:
```applescript
-- New dialog example
set myDialog to display dialog "Your question?" buttons {"No", "Yes"} default button "Yes"
set myChoice to button returned of myDialog is "Yes"
```

## Distribution

### Upload to GitHub Releases

```bash
# Create a release
gh release create v2.0 QuESt-2.0-Installer.dmg \
  --title "QuESt 2.0" \
  --notes "Professional installer for macOS"
```

### Provide Download Instructions

```markdown
## Download QuESt for macOS

[Download QuESt-2.0-Installer.dmg](https://github.com/user/repo/releases/latest)

### Installation

1. Open the downloaded DMG
2. Double-click "Install QuESt"
3. Follow the installation wizard
4. Launch from Desktop or Applications folder

### First Launch

Right-click "Install QuESt" → Open → Open (first time only)
```

## Advanced: Adding Logo to DMG

### Create Logo Icon

1. **Get a PNG logo** (512x512 recommended)

2. **Convert to .icns:**
   ```bash
   mkdir MyIcon.iconset
   sips -z 16 16     logo.png --out MyIcon.iconset/icon_16x16.png
   sips -z 32 32     logo.png --out MyIcon.iconset/icon_16x16@2x.png
   sips -z 32 32     logo.png --out MyIcon.iconset/icon_32x32.png
   sips -z 64 64     logo.png --out MyIcon.iconset/icon_32x32@2x.png
   sips -z 128 128   logo.png --out MyIcon.iconset/icon_128x128.png
   sips -z 256 256   logo.png --out MyIcon.iconset/icon_128x128@2x.png
   sips -z 256 256   logo.png --out MyIcon.iconset/icon_256x256.png
   sips -z 512 512   logo.png --out MyIcon.iconset/icon_256x256@2x.png
   sips -z 512 512   logo.png --out MyIcon.iconset/icon_512x512.png
   sips -z 1024 1024 logo.png --out MyIcon.iconset/icon_512x512@2x.png
   
   iconutil -c icns MyIcon.iconset
   ```

3. **Add to installer:**
   ```bash
   cp MyIcon.icns "$INSTALLER_APP/Contents/Resources/AppIcon.icns"
   ```

### Embed Logo in Background

Modify the Python background script in `build_professional_dmg.sh`:
```python
# After creating background
logo = Image.open('logo.png')
logo = logo.resize((200, 200))
background.paste(logo, (300, 150), logo if logo.mode == 'RGBA' else None)
```

## Troubleshooting

### Issue: "Operation not permitted" when building

**Solution:** Give Terminal Full Disk Access:
1. System Preferences → Security & Privacy → Privacy
2. Full Disk Access → Add Terminal
3. Rebuild

### Issue: AppleScript won't compile

**Solution:** Make sure script has correct line endings:
```bash
dos2unix QuESt_Installer.applescript
```

### Issue: DMG customization fails

**Solution:** The AppleScript customization is cosmetic. If it fails:
- The DMG still works
- Files are still accessible
- Installation proceeds normally

### Issue: Background image not showing

**Solution:** Pillow library needed:
```bash
pip3 install Pillow
# Or skip background - installer still works
```

### Issue: "Cannot verify developer" warning

This is normal for unsigned apps. Users need to:
1. Right-click → Open
2. Click "Open" in dialog

**To fix permanently:** Code sign with Apple Developer account

## File Sizes

| Component | Size |
|-----------|------|
| installer scripts | ~20 KB |
| DMG (uncompressed) | ~100 MB |
| DMG (compressed) | ~2-5 MB |
| After installation | ~500 MB |

## Comparison: Simple vs Professional

| Feature | Simple Script | Professional DMG |
|---------|--------------|------------------|
| Installation | Terminal-based | GUI wizard |
| Options | Command-line prompts | Dialog boxes |
| Appearance | Plain text | Custom background |
| Documentation | Text file | HTML webpage |
| User experience | Tech-savvy users | Everyone |
| Distribution | Single .sh file | Polished .dmg |

## Next Steps

1. Build and test the installer
2. Get feedback from users
3. Consider code signing ($99/year Apple Developer)
4. Create demo video
5. Update QuESt documentation

## Code Signing (Optional)

To remove security warnings:

1. **Get Apple Developer certificate** ($99/year)

2. **Sign the app:**
   ```bash
   codesign --force --deep --sign "Developer ID Application: Your Name" \
     "Install QuESt.app"
   ```

3. **Notarize:**
   ```bash
   # Create zip
   ditto -c -k --keepParent "Install QuESt.app" "Install QuESt.zip"
   
   # Submit for notarization
   xcrun notarytool submit "Install QuESt.zip" \
     --apple-id your@email.com \
     --password app-specific-password \
     --team-id TEAMID \
     --wait
   
   # Staple
   xcrun stapler staple "Install QuESt.app"
   ```

4. **Rebuild DMG** with signed app

## Support

- GitHub: https://github.com/sandialabs/snl-quest
- Issues: https://github.com/sandialabs/snl-quest/issues
- Email: tunguy@sandia.gov
