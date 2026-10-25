#!/usr/bin/env bash

# ==============================================================================
# CAR RENTAL MANAGEMENT SYSTEM
# Pure Java OOP Application with SQLite Database
# ==============================================================================

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# Locate Java Runtime
if [ -z "$JAVA_HOME" ]; then
    if [ -d "/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home" ]; then
        export JAVA_HOME="/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home"
        export PATH="$JAVA_HOME/bin:$PATH"
    elif command -v /usr/libexec/java_home >/dev/null 2>&1; then
        export JAVA_HOME="$(/usr/libexec/java_home 2>/dev/null || true)"
        if [ -n "$JAVA_HOME" ]; then
            export PATH="$JAVA_HOME/bin:$PATH"
        fi
    fi
fi

# 1. Compile Java files
mkdir -p bin
javac -cp "lib/*" -d bin $(find src/main/java -name "*.java")

# 2. Run the application
java --enable-native-access=ALL-UNNAMED -cp "bin:lib/*" com.carrental.CarRentalSystem
