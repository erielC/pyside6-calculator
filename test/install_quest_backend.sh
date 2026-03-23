#!/bin/bash
# QuESt Backend Installer
# Called by the GUI installer with parameters

set -e

# Parse command line arguments
INSTALL_DIR="$HOME/Applications/QuESt"
INSTALL_GLPK=false
DESKTOP_SHORTCUT=false
GUI_MODE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --install-dir)
            INSTALL_DIR="$2"
            shift 2
            ;;
        --install-glpk)
            INSTALL_GLPK=true
            shift
            ;;
        --desktop-shortcut)
            DESKTOP_SHORTCUT=true
            shift
            ;;
        --gui)
            GUI_MODE=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

VENV_DIR="$INSTALL_DIR/venv"
QUEST_DIR="$INSTALL_DIR/quest"

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   QuESt Installation for macOS        ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo ""
echo "Installation Directory: $INSTALL_DIR"
echo "Install GLPK: $INSTALL_GLPK"
echo "Desktop Shortcut: $DESKTOP_SHORTCUT"
echo ""

# Detect architecture
ARCH=$(uname -m)
if [ "$ARCH" = "arm64" ]; then
    echo -e "${YELLOW}● Detected Apple Silicon (M1/M2/M3)${NC}"
    IS_APPLE_SILICON=true
else
    echo -e "${YELLOW}● Detected Intel Mac${NC}"
    IS_APPLE_SILICON=false
fi
echo ""

# Progress indicator function
show_progress() {
    local current=$1
    local total=$2
    local msg=$3
    echo -e "${BLUE}[${current}/${total}] ${msg}${NC}"
}

# Step 1: Check for Rosetta (Apple Silicon only)
show_progress 1 8 "Checking system requirements..."
if [ "$IS_APPLE_SILICON" = true ]; then
    if ! /usr/bin/pgrep -q oahd; then
        echo -e "${YELLOW}  Installing Rosetta 2...${NC}"
        softwareupdate --install-rosetta --agree-to-license
        echo -e "${GREEN}  ✓ Rosetta 2 installed${NC}"
    else
        echo -e "${GREEN}  ✓ Rosetta 2 already installed${NC}"
    fi
fi
echo ""

# Step 2: Check for Homebrew
show_progress 2 8 "Checking for Homebrew..."
if [ "$IS_APPLE_SILICON" = true ]; then
    HOMEBREW_PREFIX="/usr/local"
    if [ ! -f "$HOMEBREW_PREFIX/bin/brew" ]; then
        echo -e "${YELLOW}  Installing Intel Homebrew...${NC}"
        arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        echo -e "${GREEN}  ✓ Homebrew installed${NC}"
    else
        echo -e "${GREEN}  ✓ Homebrew found${NC}"
    fi
else
    HOMEBREW_PREFIX="/usr/local"
    if ! command -v brew &> /dev/null; then
        echo -e "${YELLOW}  Installing Homebrew...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        echo -e "${GREEN}  ✓ Homebrew installed${NC}"
    else
        echo -e "${GREEN}  ✓ Homebrew found${NC}"
    fi
fi
echo ""

# Step 3: Install Python 3.9
show_progress 3 8 "Installing Python 3.9..."
if [ "$IS_APPLE_SILICON" = true ]; then
    if [ ! -f "$HOMEBREW_PREFIX/opt/python@3.9/bin/python3.9" ]; then
        echo -e "${YELLOW}  Installing Intel Python 3.9...${NC}"
        arch -x86_64 $HOMEBREW_PREFIX/bin/brew install python@3.9
        echo -e "${GREEN}  ✓ Python 3.9 installed${NC}"
    else
        echo -e "${GREEN}  ✓ Python 3.9 already installed${NC}"
    fi
    PYTHON_BIN="$HOMEBREW_PREFIX/opt/python@3.9/bin/python3.9"
else
    if ! brew list python@3.9 &> /dev/null; then
        echo -e "${YELLOW}  Installing Python 3.9...${NC}"
        brew install python@3.9
        echo -e "${GREEN}  ✓ Python 3.9 installed${NC}"
    else
        echo -e "${GREEN}  ✓ Python 3.9 already installed${NC}"
    fi
    PYTHON_BIN="$HOMEBREW_PREFIX/opt/python@3.9/bin/python3.9"
fi
echo ""

# Step 4: Install Git
show_progress 4 8 "Installing Git..."
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}  Installing Git...${NC}"
    if [ "$IS_APPLE_SILICON" = true ]; then
        arch -x86_64 $HOMEBREW_PREFIX/bin/brew install git
    else
        brew install git
    fi
    echo -e "${GREEN}  ✓ Git installed${NC}"
else
    echo -e "${GREEN}  ✓ Git already installed${NC}"
fi
echo ""

# Step 5: Install GLPK (if requested)
show_progress 5 8 "Installing GLPK solver..."
if [ "$INSTALL_GLPK" = true ]; then
    if ! brew list glpk &> /dev/null; then
        echo -e "${YELLOW}  Installing GLPK...${NC}"
        if [ "$IS_APPLE_SILICON" = true ]; then
            arch -x86_64 $HOMEBREW_PREFIX/bin/brew install glpk
        else
            brew install glpk
        fi
        echo -e "${GREEN}  ✓ GLPK installed${NC}"
    else
        echo -e "${GREEN}  ✓ GLPK already installed${NC}"
    fi
else
    echo -e "${YELLOW}  ⊘ GLPK installation skipped${NC}"
    echo ""
    echo -e "${BLUE}  To install GLPK later, visit:${NC}"
    echo -e "${BLUE}  http://winglpk.sourceforge.net/${NC}"
fi
echo ""

# Step 6: Create installation directory & clone QuESt
show_progress 6 8 "Downloading QuESt..."
mkdir -p "$INSTALL_DIR"

if [ -d "$QUEST_DIR" ]; then
    echo -e "${YELLOW}  Updating existing QuESt installation...${NC}"
    cd "$QUEST_DIR"
    git pull origin QuESt_2.0.c
    echo -e "${GREEN}  ✓ QuESt updated${NC}"
else
    echo -e "${YELLOW}  Cloning QuESt from GitHub...${NC}"
    git clone -b QuESt_2.0.c https://github.com/sandialabs/snl-quest.git "$QUEST_DIR"
    echo -e "${GREEN}  ✓ QuESt downloaded${NC}"
fi
echo ""

# Step 7: Set up Python virtual environment
show_progress 7 8 "Setting up Python environment..."
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}  Creating virtual environment...${NC}"
    if [ "$IS_APPLE_SILICON" = true ]; then
        arch -x86_64 $PYTHON_BIN -m venv "$VENV_DIR"
    else
        $PYTHON_BIN -m venv "$VENV_DIR"
    fi
fi

source "$VENV_DIR/bin/activate"

echo -e "${YELLOW}  Installing QuESt dependencies (this may take a few minutes)...${NC}"
pip install --upgrade pip --quiet
cd "$QUEST_DIR"
pip install -e .[dev] --quiet

echo -e "${GREEN}  ✓ Python environment configured${NC}"
echo ""

# Step 8: Create launcher scripts
show_progress 8 8 "Creating launcher scripts..."

# Main launcher
cat > "$INSTALL_DIR/QuESt.command" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/venv/bin/activate"
cd "$SCRIPT_DIR/quest"
python -m quest
if [ $? -ne 0 ]; then
    echo ""
    read -p "Press Enter to close..."
fi
EOF
chmod +x "$INSTALL_DIR/QuESt.command"

# Update script
cat > "$INSTALL_DIR/Update QuESt.command" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Updating QuESt..."
cd "$SCRIPT_DIR/quest"
git pull origin QuESt_2.0.c
source "$SCRIPT_DIR/venv/bin/activate"
pip install -e .[dev] --upgrade
echo ""
echo "✓ Update complete!"
read -p "Press Enter to close..."
EOF
chmod +x "$INSTALL_DIR/Update QuESt.command"

# Uninstall script
cat > "$INSTALL_DIR/Uninstall QuESt.command" << EOF
#!/bin/bash
echo "This will remove QuESt from: $INSTALL_DIR"
read -p "Are you sure? [y/N]: " confirm
if [[ "\$confirm" =~ ^[Yy]\$ ]]; then
    rm -rf "$INSTALL_DIR"
    rm -f "$HOME/Desktop/QuESt.command"
    echo "✓ QuESt has been uninstalled"
fi
read -p "Press Enter to close..."
EOF
chmod +x "$INSTALL_DIR/Uninstall QuESt.command"

# Desktop shortcut
if [ "$DESKTOP_SHORTCUT" = true ]; then
    ln -sf "$INSTALL_DIR/QuESt.command" "$HOME/Desktop/QuESt.command"
    echo -e "${GREEN}  ✓ Desktop shortcut created${NC}"
fi

echo -e "${GREEN}  ✓ Launcher scripts created${NC}"
echo ""

# Installation complete
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Installation Complete!              ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo "QuESt has been installed to:"
echo "  $INSTALL_DIR"
echo ""
echo "To launch QuESt:"
if [ "$DESKTOP_SHORTCUT" = true ]; then
    echo "  • Double-click QuESt.command on your Desktop"
fi
echo "  • Double-click: $INSTALL_DIR/QuESt.command"
echo ""
echo "To update QuESt:"
echo "  • Double-click: $INSTALL_DIR/Update QuESt.command"
echo ""
echo "To uninstall QuESt:"
echo "  • Double-click: $INSTALL_DIR/Uninstall QuESt.command"
echo ""

if [ "$IS_APPLE_SILICON" = true ]; then
    echo -e "${YELLOW}Note: QuESt runs via Rosetta (Intel mode) for compatibility.${NC}"
    echo ""
fi

if [ "$INSTALL_GLPK" = false ]; then
    echo -e "${YELLOW}GLPK was not installed. To add it later:${NC}"
    echo "  brew install glpk"
    echo "  Or visit: http://winglpk.sourceforge.net/"
    echo ""
fi

echo -e "${BLUE}Developed by Sandia National Laboratories${NC}"
echo ""

if [ "$GUI_MODE" = true ]; then
    osascript -e 'display notification "QuESt installation complete!" with title "QuESt Installer"'
    osascript -e 'display dialog "QuESt has been installed successfully!\n\nYou can now launch QuESt from your Desktop or Applications folder." buttons {"Open Install Folder", "Done"} default button "Done"' > /tmp/quest_result
    
    if grep -q "Open Install Folder" /tmp/quest_result; then
        open "$INSTALL_DIR"
    fi
    rm -f /tmp/quest_result
fi

read -p "Press Enter to close this window..."
