[app]

# (basic app info)
title = RNG Legends
package.name = rnglegends
package.domain = org.rng

# source
source.dir = .
source.include_exts = py,png,jpg,kv

# version
version = 1.0

# ---------------- PYTHON DEPENDENCIES ----------------
requirements = python3,kivy

# ---------------- SCREEN SETTINGS ----------------
orientation = portrait
fullscreen = 1

# ---------------- ANDROID SETTINGS (IMPORTANT FIXES) ----------------

android.api = 33
android.minapi = 21
android.sdk = 33

# 🔥 CRITICAL: FORCE STABLE BUILD-TOOLS (STOP 37 ISSUE)
android.build_tools = 33.0.2

# 🔥 CRITICAL: FORCE STABLE NDK
android.ndk = 25b

# ---------------- PERMISSIONS ----------------
android.permissions = INTERNET

# ---------------- PERFORMANCE / FIXES ----------------
log_level = 2
warn_on_root = 1

# 🔥 IMPORTANT: stop auto SDK guessing (prevents 37 install attempts)
android.allow_sdk_build_tools_version = 33.0.2

# ---------------- OPTIONAL (helps CI stability) ----------------
p4a.branch = stable
