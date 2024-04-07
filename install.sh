#!/usr/bin/env bash
set -eu -o pipefail
cd "$(dirname "$(realpath "${0}")")"

DATADIR=${DATADIR:-/usr/share}
LIBDIR=${LIBDIR:-/usr/lib}

# The actual executable
install -Dm 0755 gnome-duckduckgo-search-provider.py "${LIBDIR}"/gnome-duckduckgo-search-provider/gnome-duckduckgo-search-provider.py

# Search provider definition
install -Dm 0644 conf/org.gnome.DuckDuckGo.SearchProvider.ini "${DATADIR}"/gnome-shell/search-providers/org.gnome.DuckDuckGo.SearchProvider.ini

# Desktop file (for having an icon)
install -Dm 0644 conf/org.gnome.DuckDuckGo.SearchProvider.desktop "${DATADIR}"/applications/org.gnome.DuckDuckGo.SearchProvider.desktop

# DBus configuration (no-systemd)
install -Dm 0644 conf/org.gnome.DuckDuckGo.SearchProvider.service.dbus "${DATADIR}"/dbus-1/services/org.gnome.DuckDuckGo.SearchProvider.service

# DBus configuration (systemd)
install -Dm 0644 conf/org.gnome.DuckDuckGo.SearchProvider.service.systemd "${LIBDIR}"/systemd/user/org.gnome.DuckDuckGo.SearchProvider.service
