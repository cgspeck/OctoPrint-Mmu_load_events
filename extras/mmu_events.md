---
layout: plugin

id: mmu_load_events
title: MMU Load Events
description: Triggers Octoprint events in response to Prusa MMU2s filament load events
authors:
  - Chris Speck
license: AGPLv3

date: 2020-11-29

homepage: https://github.com/cgspeck/OctoPrint-Mmu_load_events
source: https://github.com/cgspeck/OctoPrint-Mmu_load_events
archive: https://github.com/cgspeck/OctoPrint-Mmu_load_events/archive/main.zip

tags:
  - notifications
  - events
  - prusa
  - mmu
  - mmu2s
  - node-red
  - nodered
  - pushover
  - push-over

compatibility:
  # List of compatible versions
  #
  # A single version number will be interpretated as a minimum version requirement,
  # e.g. "1.3.1" will show the plugin as compatible to OctoPrint versions 1.3.1 and up.
  # More sophisticated version requirements can be modelled too by using PEP440
  # compatible version specifiers.
  #
  # You can also remove the whole "octoprint" block. Removing it will default to all
  # OctoPrint versions being supported.

  octoprint:
    - 1.4.0

  python: ">=2.7,<4"
---

# MMU load events

This plugin monitors serial communication from your printer and dispatches the following events when it sees that the MMU2s has attempted a filament load, depending on the outcome:

```python
PLUGIN_MMU_LOAD_EVENTS_FAILED
PLUGIN_MMU_LOAD_EVENTS_SUCCESS
PLUGIN_MMU_LOAD_EVENTS_UNKNOWN
```

In the case of `SUCCESS` and `FAILED`, the event payload will contain the following members:

- `line`: what was recieved from your printer
- `filamentDetect`: the string describing IR Sensor readings:
  - `o` = no filament detected
  - `O` = filament detected
- `success`: true or false depending on what happened

In the case of a `FAILED` message, only `line` will be present.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/cgspeck/OctoPrint-MMU_load_events/archive/main.zip

Subscribe to events by creating/adding to the events section in Octoprint's `~/.octoprint/config.yaml`:

```yaml
events:
  enabled: true
  subscriptions:
    - command:
        - /home/pi/bin/notify-nodered-mmu "{__eventname}" "{line}" "{success}" "{filamentDetect}"
      event: PLUGIN_MMU_LOAD_EVENTS_SUCCESS
      type: system
    - command:
        - /home/pi/bin/notify-nodered-mmu "{__eventname}" "{line}" "{success}" "{filamentDetect}"
      event: PLUGIN_MMU_LOAD_EVENTS_FAILED
      type: system
    - command:
        - /home/pi/bin/notify-nodered-mmu "{__eventname}" "{line}"
      event: PLUGIN_MMU_LOAD_EVENTS_UNKNOWN
      type: system
```

The `node-red/` folder contains a sample flow and the helper script I use to dispatch these events via email and [Pushover](https://pushover.net/).

## Configuration

There is no configuration.

## Testing with Virtual printer

Use the following commands in the Terminal to trigger this plugin:

```
!!DEBUG:send MMU can_load:OOOooooooOOOOOOOOOOO succeeded.
!!DEBUG:send MMU can_load:OOOooooooOOOOOOOOOOO failed.
!!DEBUG:send MMU can_load:OOOooooooOOOOOOOOOOO foo bar
```
