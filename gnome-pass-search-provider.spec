Name:           gnome-duckduckgo-search-provider
Version:        master
Release:        1
License:        GPL-3.0+
Summary:        Gnome Shell search provider for DuckDuckGo
Url:            https://github.com/iacobucci/%{name}
Source:         https://github.com/iacobucci/%{name}/archive/master.tar.gz
Requires:       gnome-shell
Requires:       python3-gobject
Requires:       python3-dbus
Requires:       python3-fuzzywuzzy
Requires:       python3-Levenshtein
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%global debug_package %{nil}

%description
A Gnome Shell DuckDuckGo search provider

%prep
%setup -q -n %{name}-%{version}

%build

%install
sed -i -e 's|DATADIR=|DATADIR=$RPM_BUILD_ROOT|' install.sh
sed -i -e 's|LIBDIR=|LIBDIR=$RPM_BUILD_ROOT|' install.sh
./install.sh

%files
%defattr(-,root,root,-)
%doc README.md
%{_prefix}/lib/gnome-duckduckgo-search-provider/gnome-duckduckgo-search-provider.py
%{_prefix}/lib/systemd/user/org.gnome.DuckDuckGo.SearchProvider.service
%{_prefix}/share/dbus-1/services/org.gnome.DuckDuckGo.SearchProvider.service
%{_prefix}/share/applications/org.gnome.DuckDuckGo.SearchProvider.desktop
%{_prefix}/share/gnome-shell/search-providers/org.gnome.DuckDuckGo.SearchProvider.ini
