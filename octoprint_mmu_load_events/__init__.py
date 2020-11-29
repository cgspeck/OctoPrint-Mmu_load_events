# coding=utf-8
from __future__ import absolute_import, unicode_literals
import logging

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
from octoprint.events import eventManager

class Mmu_load_eventsPlugin(
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
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

    ##~~ EventHandlerPlugin
    def on_event(self, event, payload):
        pass

    ##~~ StartupPlugin
    def on_after_startup(self):
        self._logger.info("MMU Load Events plugin saying g'day!")

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(
            enabled=True
        )

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(
            js=["js/mmu_load_events.js"],
            css=["css/mmu_load_events.css"],
            less=["less/mmu_load_events.less"]
        )

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return dict(
            mmu_load_events=dict(
                displayName="Mmu_load_events Plugin",
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


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "MMU Load Events"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
#__plugin_pythoncompat__ = ">=3,<4" # only python 3
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Mmu_load_eventsPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.comm.protocol.gcode.received": Mmu_load_eventsPlugin.handle_gcode_received
    }

