# coding=utf-8
from __future__ import absolute_import, unicode_literals

import octoprint.plugin
from octoprint.events import eventManager


__plugin_name__ = "MMU Load Events"
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

class Mmu_load_eventsPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.EventHandlerPlugin
):
    FAILED_EVENT = "PLUGIN_MMU_LOAD_EVENTS_FAILED"
    SUCCESS_EVENT = "PLUGIN_MMU_LOAD_EVENTS_SUCCESS"

    def __init__(self) -> None:
        super(Mmu_load_eventsPlugin).__init__()
        self._hunting = False
        self._line = ""

    def _dispatch_if_complete(self, line: str) -> bool:
        parts = self._line.split(" ")
        result_part = parts[-1]
        if result_part in ["succeeded.", "failed."]:
            self._logger.info("succeded or failed!!!!!!!!!!!")
            succeeded = result_part == "succeeded."
            result_evt = (
                Mmu_load_eventsPlugin.FAILED_EVENT,
                Mmu_load_eventsPlugin.SUCCESS_EVENT)[succeeded]

            cleaned_line = self._line.replace("echo:busy: processing", "")
            filament_detect = cleaned_line.split(" ")[-2].split(":")[-1]
            self._logger.info("firing event!!!!!")
            eventManager().fire(result_evt, {"line": self._line, "filamentDetect": filament_detect, "success": succeeded})
            return True

        return False

    ##~~ To process recieved gcode
    def handle_gcode_received(self, _comm_instance, line: str, *args, **kwargs):
        complete = False
        self._logger.info("line: '{}'".format(line))

        if line.startswith("MMU can_load:"):
            self._logger.info("xxxxxxxxxxxx FOUND STARTING STRING xxxxxxxxxxxx")
            self._hunting = True
            self._line = line
            complete = self._dispatch_if_complete(line)
        elif self._hunting:
            self._line += line
            complete = self._dispatch_if_complete(line)

        if complete:
            self._hunting = False

        return line

    ##~~ These events are sent by the hook above
    @staticmethod
    def register_custom_events_hook(*args, **kwargs):
        # PLUGIN_MMU_LOAD_EVENTS_SUCCESS, PLUGIN_MMU_LOAD_EVENTS_FAILED
        return ["success", "failed"]

    ##~~ StartupPlugin
    def on_after_startup(self):
        self._logger.info("MMU Load Events plugin saying g'day!")

    ##~~ Softwareupdate hook
    def get_update_information(self):
        # See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        return dict(
            mmu_load_events=dict(
                displayName=__plugin_name__,
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="cgspeck",
                repo="OctoPrint-Mmu_load_events",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/cgspeck/OctoPrint-Mmu_load_events/archive/{target_version}.zip"
            )
        )

def __plugin_load__():
    plugin = Mmu_load_eventsPlugin()

    global __plugin_implementation__
    __plugin_implementation__ = Mmu_load_eventsPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.comm.protocol.gcode.received": plugin.handle_gcode_received
    }
