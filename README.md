# OctoPrint-MMU_load_events

This plugin monitors serial communication from your printer and dispatches the following events when it sees that the MMU2s has attempted a filament load, depending on the outcome:

```python
PLUGIN_MMU_LOAD_EVENTS_FAILED  # MMU load failed
PLUGIN_MMU_LOAD_EVENTS_PAUSED  # generic "paused for user" from printer
PLUGIN_MMU_LOAD_EVENTS_RESUMED  # sent when printer appears to resume, if an 'ok' is seen after a pause
PLUGIN_MMU_LOAD_EVENTS_SUCCESS  # MMU load succeeded
```

In the case of `SUCCESS` and `FAILED`, the event payload will contain the following members:

- `line`: what was recieved from your printer
- `filamentDetect`: the string describing IR Sensor readings:
  - `o` = no filament detected
  - `O` = filament detected
- `success`: true or false depending on what happened

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
      event:
        - PLUGIN_MMU_LOAD_EVENTS_SUCCESS
        - PLUGIN_MMU_LOAD_EVENTS_FAILED
      type: system
    - command:
        - /home/pi/bin/notify-nodered-mmu "{__eventname}"
      event:
        - PLUGIN_MMU_LOAD_EVENTS_PAUSED
        - PLUGIN_MMU_LOAD_EVENTS_RESUMED
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
!!DEBUG:send MMU can_load:OOOooooooOOOOOOOOOOO succeeded.
!!DEBUG:send echo:busy: paused for user
```
