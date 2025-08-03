@echo off
echo Starting Firebase Emulator...
firebase emulators:start --only firestore --port 8080
pause