# macOS System Preferences Reference

Batch configure macOS system preferences using `defaults` commands. All changes take effect after restarting the relevant app or logging out/in.

Apply all settings at once:

```bash
/System/Library/PrivateFrameworks/SystemAdministration.framework/Resources/activateSettings -u
```

## Dock

```bash
# Auto-hide Dock
defaults write com.apple.dock autohide -bool true

# Remove auto-hide delay
defaults write com.apple.dock autohide-delay -float 0
defaults write com.apple.dock autohide-time-modifier -float 0

# Show recent apps in Dock
defaults write com.apple.dock show-recents -bool false

# Make Dock icons smaller/larger
defaults write com.apple.dock tilesize -int 48

# Show only active applications
defaults write com.apple.dock static-only -bool true

# Reset Dock to defaults
defaults delete com.apple.dock
killall Dock
```

## Finder

```bash
# Show path bar at bottom
defaults write com.apple.finder ShowPathbar -bool true

# Show status bar
defaults write com.apple.finder ShowStatusBar -bool true

# Show hidden files
defaults write com.apple.finder AppleShowAllFiles -bool true

# Keep folders on top (when sorting by name)
defaults write com.apple.finder _FXSortFoldersFirst -bool true

# Keep folders on top on Desktop
defaults write com.apple.finder _FXSortFoldersFirstOnDesktop -bool true

# Use list view as default
defaults write com.apple.finder FXPreferredViewStyle -string "Nlsv"

# Use column view as default
defaults write com.apple.finder FXPreferredViewStyle -string "clmv"

# Search in current folder by default
defaults write com.apple.finder FXDefaultSearchScope -string "SCcf"

# Show all file extensions
defaults write NSGlobalDomain AppleShowAllExtensions -bool true

# Prevent creating .DS_Store on network volumes
defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true

# Prevent creating .DS_Store on USB drives
defaults write com.apple.desktopservices DSDontWriteUSBStores -bool true

# Apply changes
killall Finder
```

## Trackpad

```bash
# Enable tap to click
defaults write com.apple.AppleMultitouchTrackpad Clicking -bool true
defaults -currentHost write -g com.apple.mouse.tapBehavior -int 1

# Enable right-click (two-finger click)
defaults write com.apple.AppleMultitouchTrackpad TrackpadRightClick -bool true

# Enable three-finger drag
defaults write com.apple.AppleMultitouchTrackpad TrackpadThreeFingerDrag -bool true
```

## Keyboard

```bash
# Set keyboard repeat rate (faster)
defaults write NSGlobalDomain KeyRepeat -int 2

# Set initial repeat delay (shorter)
defaults write NSGlobalDomain InitialKeyRepeat -int 15

# Enable full keyboard access (Tab in all controls)
defaults write NSGlobalDomain AppleKeyboardUIMode -int 3
```

## Screenshots

```bash
# Change screenshot save location
defaults write com.apple.screencapture location ~/Documents/Screenshots

# Disable screenshot shadow
defaults write com.apple.screencapture disable-shadow -bool true

# Save screenshots as PNG (default)
defaults write com.apple.screencapture type -string "png"

# Save screenshots as JPG
defaults write com.apple.screencapture type -string "jpg"

# Apply screenshot changes
killall SystemUIServer
```

## Security & Privacy

```bash
# Require password immediately after sleep/screensaver
defaults write com.apple.screensaver askForPassword -int 1
defaults write com.apple.screensaver askForPasswordDelay -int 0

# Disable automatic login
# (Set via System Settings > Users & Groups)

# Show hidden files (also in Finder section above)
defaults write com.apple.finder AppleShowAllFiles -bool true
```

## General UI

```bash
# Reduce transparency
defaults write com.apple.universalaccess reduceTransparency -bool true

# Expand save/print dialogs by default
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode -bool true
defaults write NSGlobalDomain PMPrintingExpandedStateForPrint -bool true

# Save to disk by default (not iCloud)
defaults write NSGlobalDomain NSDocumentSaveNewDocumentsToCloud -bool false

# Close windows when quitting an app
defaults write NSGlobalDomain NSQuitAlwaysKeepsWindows -bool false

# Disable automatic capitalization
defaults write NSGlobalDomain NSAutomaticCapitalizationEnabled -bool false

# Disable automatic period substitution
defaults write NSGlobalDomain NSAutomaticPeriodSubstitutionEnabled -bool false

# Disable smart quotes
defaults write NSGlobalDomain NSAutomaticQuoteSubstitutionEnabled -bool false

# Disable smart dashes
defaults write NSGlobalDomain NSAutomaticDashSubstitutionEnabled -bool false
```

## Bluetooth & AirDrop

```bash
# Increase Bluetooth sound quality (requires restart)
defaults write com.apple.BluetoothAudioAgent "Apple Bitpool Min (editable)" -int 40

# Enable AirDrop over Ethernet
defaults write com.apple.NetworkBrowser BrowseAllInterfaces -bool true
```

## Time Machine

```bash
# Prevent Time Machine from prompting to use new drives
defaults write com.apple.TimeMachine DoNotOfferNewDisksForBackup -bool true

# Disable local Time Machine snapshots
sudo tmutil disablelocal
```

## Apply All Changes

```bash
# Restart affected apps
killall Finder
killall Dock
killall SystemUIServer

# Or apply all system settings
/System/Library/PrivateFrameworks/SystemAdministration.framework/Resources/activateSettings -u
```
