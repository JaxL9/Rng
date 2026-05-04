[app]

title = RNG Legends
package.name = rnglegends
package.domain = org.rng

source.dir = .
source.include_exts = py,png,jpg,kv

version = 1.0

# ---------------- PYTHON ----------------
requirements = python3,kivy

orientation = portrait
fullscreen = 1

# ---------------- ANDROID CORE ----------------

android.api = 33
android.minapi = 21

# 🔥 FORCE STABLE TOOLCHAIN (CRITICAL FIX)
android.build_tools = 33.0.2
android.ndk = 25b

# ---------------- IMPORTANT FIXES ----------------

# ❌ DO NOT USE (causes fallback to 37)
# android.sdk = 33   <-- MUST NOT EXIST

# Forces Buildozer not to auto-pick latest broken tools
android.allow_sdk_build_tools_version = 33.0.2

# ---------------- PERFORMANCE / LOGS ----------------
log_level = 2
warn_on_root = 1

# ---------------- PYTHON-FOR-ANDROID ----------------
p4a.branch = stable
