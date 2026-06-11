[app]

# (str) Title of your application
title = Airplane Battle

# (str) Package name
package.name = airplanebattle

# (str) Package domain (needed for android/ios packaging)
package.domain = org.luo235

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let the pygame game assets be copied too)
source.include_exts = py,png,jpg,jpeg,bmp,wav,ogg,txt

# Keep development-only GA files out of the Android package.
source.exclude_patterns = ga.py
source.exclude_dirs = __pycache__,.git,.github,.venv,venv,build,dist,p4a-recipes

# (str) Application versioning
version = 1.0

# (list) Application requirements
# pygame uses python-for-android's SDL2 bootstrap/recipes.
requirements = python3,pygame

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Hide the Android status bar
fullscreen = 1

# (list) Permissions
android.permissions = VIBRATE

# Accept Android SDK licenses non-interactively in CI.
android.accept_sdk_license = True

# Build the modern 64-bit Android ABI first to keep CI time and native build
# surface area low. Add armeabi-v7a later only if a 32-bit APK is required.
android.archs = arm64-v8a

# Pin API/min API to versions supported by current python-for-android/Buildozer
# and GitHub-hosted runners.
android.api = 35
android.minapi = 23
android.ndk = 25b

# Use python-for-android's SDL2 bootstrap, which is required for pygame.
p4a.bootstrap = sdl2
p4a.local_recipes = ./p4a-recipes

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
