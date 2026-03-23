#!/usr/bin/osascript
# QuESt Professional Installer
# This creates a GUI installer with options

on run
    -- Display welcome dialog with logo
    set welcomeText to "Welcome to QuESt 2.0 Installer

QuESt is an open-source platform for energy storage simulation and analysis developed by Sandia National Laboratories.

This installer will:
• Install Python 3.9 and Git (via Homebrew)
• Download and configure QuESt
• Optionally install GLPK solver
• Create desktop shortcuts

Click Continue to begin installation."
    
    set welcomeButton to button returned of (display dialog welcomeText buttons {"Cancel", "Continue"} default button "Continue" with title "QuESt Installer" with icon note)
    
    if welcomeButton is "Cancel" then
        return
    end if
    
    -- Installation location selection
    set installLocations to {"Home Directory (Recommended)", "Applications Folder", "Custom Location"}
    set installChoice to choose from list installLocations with prompt "Where would you like to install QuESt?" default items {"Home Directory (Recommended)"} with title "Installation Location"
    
    if installChoice is false then
        return -- User cancelled
    end if
    
    set installLocation to item 1 of installChoice
    
    if installLocation is "Home Directory (Recommended)" then
        set installPath to (path to home folder as text) & "Applications:QuESt"
    else if installLocation is "Applications Folder" then
        set installPath to (path to applications folder as text) & "QuESt"
    else
        set installPath to choose folder with prompt "Select installation directory:"
        set installPath to (installPath as text) & "QuESt"
    end if
    
    -- Convert to POSIX path
    set installDir to POSIX path of installPath
    
    -- GLPK installation option
    set glpkDialog to display dialog "Install GLPK Solver?

GLPK is required for optimization features in QuESt.

• Recommended for most users
• Adds ~10 MB to installation
• Can be installed later if needed

If you choose not to install now, you can download it from:
http://winglpk.sourceforge.net/" buttons {"Skip GLPK", "Install GLPK"} default button "Install GLPK" with title "GLPK Solver" with icon caution
    
    set installGLPK to button returned of glpkDialog is "Install GLPK"
    
    -- Desktop shortcut option
    set shortcutDialog to display dialog "Create Desktop Shortcut?

A shortcut will be added to your Desktop for quick access to QuESt." buttons {"No", "Yes"} default button "Yes" with title "Desktop Shortcut"
    
    set createShortcut to button returned of shortcutDialog is "Yes"
    
    -- Confirmation
    if installGLPK then
        set glpkText to "Yes"
    else
        set glpkText to "No"
    end if
    
    if createShortcut then
        set shortcutText to "Yes"
    else
        set shortcutText to "No"
    end if
    
    set confirmText to "Ready to Install QuESt

Installation Location:
" & installDir & "

GLPK Solver: " & glpkText & "
Desktop Shortcut: " & shortcutText & "

Installation will take 5-15 minutes.
An internet connection is required.

Click Install to begin."
    
    set confirmButton to button returned of (display dialog confirmText buttons {"Back", "Install"} default button "Install" with title "Confirm Installation")
    
    if confirmButton is "Back" then
        -- Could loop back, but for simplicity just exit
        return
    end if
    
    -- Get the script directory to find the actual installer
    tell application "Finder"
        set scriptPath to POSIX path of (container of (path to me) as text)
    end tell
    
    -- Run the actual installation script with parameters
    set shellScript to scriptPath & "Resources/install_quest_backend.sh"
    
    set installCommand to quoted form of shellScript
    set installCommand to installCommand & " --install-dir " & quoted form of installDir
    
    if installGLPK then
        set installCommand to installCommand & " --install-glpk"
    end if
    
    if createShortcut then
        set installCommand to installCommand & " --desktop-shortcut"
    end if
    
    set installCommand to installCommand & " --gui"
    
    -- Show progress
    display notification "Starting QuESt installation..." with title "QuESt Installer"
    
    -- Run installation in Terminal
    tell application "Terminal"
        activate
        do script installCommand
    end tell
    
end run
