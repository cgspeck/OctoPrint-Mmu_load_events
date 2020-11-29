# coding=utf-8
from __future__ import absolute_import, unicode_literals
import logging

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
    UNKNOWN_EVENT = "PLUGIN_MMU_LOAD_EVENTS_UNKNOWN"

    ##~~ To process recieved gcode
    @staticmethod
    def handle_gcode_received(comm_instance, line: str, *args, **kwargs):
        if line.startswith("MMU can_load:"):
            logger = logging.getLogger("octoprint.plugin." + __name__)
            parts = line.split(" ")
            result_part = parts[-1]

            if result_part in ["succeeded.", "failed."]:
                succeeded = result_part == "succeeded."
                result_str = ("failed", "succeded")[succeeded]
                result_evt = (
                    Mmu_load_eventsPlugin.FAILED_EVENT,
                    Mmu_load_eventsPlugin.SUCCESS_EVENT)[succeeded]

                filament_detect = parts[-2].split(":")[-1]
                logger.info("Load MMU status: {}, filament detected: '{}'".format(result_str, filament_detect))
                eventManager().fire(result_evt, {"line": line, "filamentDetect": filament_detect, "success": succeeded})
                pass
            else:
                logger.warning("Unable to determine MMU status, received '{}'".format(line))
                eventManager().fire(Mmu_load_eventsPlugin.UNKNOWN_EVENT, {"line": line})

        return line

    ##~~ These events are sent by the hook above
    @staticmethod
    def register_custom_events_hook(*args, **kwargs):
        # PLUGIN_MMU_LOAD_EVENTS_SUCCESS, PLUGIN_MMU_LOAD_EVENTS_FAILED, PLUGIN_MMU_LOAD_EVENTS_UNKNOWN
        return ["success", "failed", "unknown"]

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
    global __plugin_implementation__
    __plugin_implementation__ = Mmu_load_eventsPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.comm.protocol.gcode.received": Mmu_load_eventsPlugin.handle_gcode_received
    }

