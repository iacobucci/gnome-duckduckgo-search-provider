#!/usr/bin/python3
import re
import subprocess
from os import getenv
from os import walk
from os.path import expanduser
from os.path import join as path_join

from fuzzywuzzy import process
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

from gi.repository import GLib

import duckduckgo_search

# Convenience shorthand for declaring dbus interface methods.
# s.b.n. -> search_bus_name
search_bus_name = "org.gnome.Shell.SearchProvider2"
sbn = dict(dbus_interface=search_bus_name)


class SearchEngine():
    def __init__(self):
        self.url = "https://duckduckgo.com/?q="
        self.cache = []

    def search(self, query: str):
        if (len(self.cache) > 100):
            self.cache = self.cache[4:]

        newresults = []
        
        directresult = {"title": "Search DuckDuckGo for " + query, "href": self.url + query}
        newresults.append((str(id(directresult)), directresult))

        if (query[0] != "!"):
            results = duckduckgo_search.ddg(query)[:4]
            for result in results:
                r = {"title": result["title"], "href": result["href"]}
                i = str(id(r))
                newresults.append((i, r))

        self.cache += newresults
        return [i[0] for i in newresults]

    def get_metas(self, ids):
        metas = []
        for i in ids:
            for r in self.cache:
                if i == r[0]:
                    metas.append(
                        {"id": r[0], "name": r[1]["title"], "description": r[1]["href"]})
        return metas

    def open(self, id):
        for r in self.cache:
            if id == r[0]:
                subprocess.Popen(["xdg-open", r[1]["href"]])
                break


class SearchPassService(dbus.service.Object):

    bus_name = "org.gnome.DuckDuckGo.SearchProvider"
    _object_path = "/" + bus_name.replace(".", "/")

    def __init__(self):
        self.session_bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(self.bus_name, bus=self.session_bus)
        dbus.service.Object.__init__(self, bus_name, self._object_path)
        self.se = SearchEngine()

    @dbus.service.method(in_signature="asu", terms="as", timestamp="u", **sbn)
    def LaunchSearch(self, terms, timestamp):
        pass

    @dbus.service.method(in_signature="as", out_signature="as", **sbn)
    def GetInitialResultSet(self, terms):
        return dbus.Array(self.se.search(" ".join(terms)), signature="as")

    @dbus.service.method(in_signature="asas", out_signature="as", **sbn)
    def GetSubsearchResultSet(self, previous_results, new_terms):
        return dbus.Array(self.se.search(" ".join(new_terms)), signature="as")

    @dbus.service.method(in_signature="as", out_signature="aa{sv}", **sbn)
    def GetResultMetas(self, ids):
        return dbus.Array(self.se.get_metas(ids), signature="a{sv}")

    @dbus.service.method(in_signature="sasu", **sbn)
    def ActivateResult(self, id, terms, timestamp):
        self.se.open(id)


if __name__ == "__main__":
    DBusGMainLoop(set_as_default=True)
    SearchPassService()
    GLib.MainLoop().run()
