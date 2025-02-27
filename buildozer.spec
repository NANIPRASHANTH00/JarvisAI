[app]
title = JarvisAI
package.name = jarvis_ai
package.domain = com.yourname.jarvis
source.include_exts = py,png,jpg,kv,atlas

requirements = python3,kivy,vosk,transformers,torch,sounddevice,pyttsx3
android.permissions = INTERNET, RECORD_AUDIO
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 0

[android]
android.api = 31
android.minapi = 21
android.ndk = 23b
android.arch = arm64-v8a, armeabi-v7a

