# OctoPrint/Node-RED Integration

Copy and modify the scripts in this folder to point to your Node-RED instance then put them in `~/bin` on your OctoPrint installation and make them executable.

Subscriptions config snippet for `~/.oprint/config.yaml`:

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
        - /home/pi/bin/notify-nodered "{__eventname}" "{__filepath}" "{__filename}"
      event:
        - PrintDone
        - PrintFailed
        - PrintCancelled
        - PrintStarted
      type: system
    - command:
        - /home/pi/bin/notify-nodered "{__eventname}" "{__filepath}" "{__filename}"
      event: Startup
      type: system
```

[Persistent Context](https://discourse.nodered.org/t/a-guide-to-understanding-persistent-context/4115) storage (`localfilesystem`) in Node-RED to preserve stats between deploys and restarts.

View the dashboard at `${NODE_RED_IP_ADDRESS}/ui`.
