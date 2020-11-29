# OctoPrint-MMU_load_events

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

    https://github.com/cgspeck/OctoPrint-MMU_load_events/archive/master.zip

Subscribe to events by creating/adding to the events section in Octoprint's `~/.octoprint/config.yaml`:

```yaml

```

## Configuration

There is no configuration.

## Testing with Virtual printer

Use the following commands in the Terminal to trigger this plugin:

```
!!DEBUG:send MMU can_load:OOOooooooOOOOOOOOOOO succeeded.
!!DEBUG:send MMU can_load:OOOooooooOOOOOOOOOOO failed.
!!DEBUG:send MMU can_load:OOOooooooOOOOOOOOOOO foo bar
```
