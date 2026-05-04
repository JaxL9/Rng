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

# ---------------- ANDROID (CRITICAL LOCKS) ----------------

android.api = 33
android.minapi = 21

# 🔥 FORCE STABLE TOOLCHAIN
android.build_tools = 33.0.2
android.ndk = 25b

# ❌ DO NOT USE THIS (causes 37 fallback)
# android.sdk = 33   <-- REMOVE IF IT EXISTS

# ---------------- FIX AUTO RESOLUTION ----------------
android.allow_sdk_build_tools_version = 33.0.2

# ---------------- PERFORMANCE ----------------
log_level = 2
warn_on_root = 1

# ---------------- P4A ----------------
p4a.branch = stable
