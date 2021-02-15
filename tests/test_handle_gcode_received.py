import sys
from pathlib import Path
from os.path import dirname

sys.path.append(str(Path(dirname(__file__), "../").absolute()))
sys.path.append(str(Path(dirname(__file__), "../../OctoPrint/src").absolute()))
sys.path.append(
    str(
        Path(
            dirname(__file__), "../../OctoPrint/venv/lib/python3.8/site-packages"
        ).absolute()
    )
)

import pytest
from mock import call

from octoprint_mmu_load_events import Mmu_load_eventsPlugin


@pytest.fixture()
def mock_eventManager(mocker):
    mock_fire = mocker.Mock()
    mock_constructor = mocker.Mock(return_value=mock_fire)
    mocker.patch(
        "octoprint_mmu_load_events.eventManager", return_value=mock_constructor
    )
    return mock_constructor


def test_ideal(mock_eventManager):
    comm_instance = None
    line = "MMU can_load:OOOooooooOOOOOOOOOOO succeeded."
    plugin = Mmu_load_eventsPlugin()
    plugin.handle_gcode_received(comm_instance, line=line)
    assert mock_eventManager.fire.call_args_list == [
        call(
            "PLUGIN_MMU_LOAD_EVENTS_SUCCESS",
            {
                "line": "MMU can_load:OOOooooooOOOOOOOOOOO succeeded.",
                "filamentDetect": "OOOooooooOOOOOOOOOOO",
                "success": True,
            },
        )
    ]


MMU_SUCCESS_SAMPLES = [
    [
        "echo:busy: processing\n",
        "MMU can_load:\n",
        "OOOOOOOOOOOOOOOOOecho:busy: processing\n",
        "OOOOOOOOOOOOO succeeded.\n",
        "tmc2130_home_enter(axes_mask=0x04)\n",
        "echo:busy: processing\n",
    ],
    [
        "echo:busy: processing\n",
        "MMU can_load:\n",
        "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO succeeded.\n",
        "echo:busy: processing\n",
    ],
    [
        "MMU can_load:\n",
        "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO succeeded.\n",
        "echo:busy: processing\n",
    ],
    [
        "echo:busy: processing\n",
        "MMU can_load:\n",
        "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO succeeded.\n",
        "tmc2130_home_enter(axes_mask=0x04)\n",
    ],
    [
        "echo:busy: processing\n",
        "MMU can_load:\n",
        "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO succeeded.\n",
        "echo:busy: processing\n",
    ],
    [
        "MMU can_load:\n",
        "OOOOOOOOOOOOOOOOOOOOOOOOOOOOecho:busy: processing\n",
        "OO succeeded.",
    ],
]


MMU_FAIL_SAMPLES = [
    [
        "echo:busy: processing\n",
        "MMU can_load:\n",
        "OOOOOOOOOOOOOOOOOecho:busy: processing\n",
        "OOOOO11111111 failed.\n",
        "tmc2130_home_enter(axes_mask=0x04)\n",
        "echo:busy: processing\n",
    ],
    [
        "echo:busy: processing\n",
        "MMU can_load:\n",
        "OOOOOOOOOOOOOOOOOOOOOO11111111 failed.\n",
        "echo:busy: processing\n",
    ],
    [
        "MMU can_load:\n",
        "OOOOOOOOOOOOOOOOOOOOOO11111111 failed.\n",
        "echo:busy: processing\n",
    ],
    [
        "echo:busy: processing\n",
        "MMU can_load:\n",
        "OOOOOOOOOOOOOOOOOOOOOO11111111 failed.\n",
        "tmc2130_home_enter(axes_mask=0x04)\n",
    ],
    [
        "echo:busy: processing\n",
        "MMU can_load:\n",
        "OOOOOOOOOOOOOOOOOOOOOO11111111 failed.\n",
        "echo:busy: processing\n",
    ],
]

FIRMWARE_UPGRADE_SAMPLES = [
    "ok",
    "ok",
    "ok",
    "ok",
    "echo:busy: paused for user",
    "echo:busy: paused for user",
    "echo:busy: paused for user",
    "echo:busy: paused for user",
    "MMU not responding - DISABLED",
    "echo:busy: paused for user",
    "echo:busy: paused for user",
    "echo:busy: paused for user",
    "echo:busy: paused for user",
    "echo:busy: paused for user",
    "echo:busy: paused for user",
    "echo:busy: paused for user",
    "echo:busy: paused for user",
    "echo:busy: paused for user",
    "echo:busy: paused for user",
    "ok",
    "ok T:209.6 /0.0 B:94.9 /0.0 T0:209.6 /0.0 @:0 B@:0 P:53.5 A:42.2",
    "ok",
    "ok",
    "ok",
    "ok",
]


@pytest.mark.parametrize("log_lines", MMU_SUCCESS_SAMPLES)
def test_success_real_world(mock_eventManager, log_lines):
    plugin = Mmu_load_eventsPlugin()
    for line in log_lines:
        plugin.handle_gcode_received(None, line=line)

    assert (
        mock_eventManager.fire.call_args_list[0][0][0]
        == "PLUGIN_MMU_LOAD_EVENTS_SUCCESS"
    )
    assert (
        mock_eventManager.fire.call_args_list[0][0][1]["filamentDetect"]
        == "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
    )


@pytest.mark.parametrize("log_lines", MMU_FAIL_SAMPLES)
def test_failed_real_world(mock_eventManager, log_lines):
    plugin = Mmu_load_eventsPlugin()
    for line in log_lines:
        plugin.handle_gcode_received(None, line=line)

    assert (
        mock_eventManager.fire.call_args_list[0][0][0]
        == "PLUGIN_MMU_LOAD_EVENTS_FAILED"
    )
    assert (
        mock_eventManager.fire.call_args_list[0][0][1]["filamentDetect"]
        == "OOOOOOOOOOOOOOOOOOOOOO11111111"
    )


def test_firmware_error_then_recover(
    mock_eventManager,
):
    plugin = Mmu_load_eventsPlugin()
    for line in FIRMWARE_UPGRADE_SAMPLES:
        plugin.handle_gcode_received(None, line=line)

    assert mock_eventManager.fire.call_args_list == [
        call("PLUGIN_MMU_LOAD_EVENTS_PAUSED"),
        call("PLUGIN_MMU_LOAD_EVENTS_RESUMED"),
    ]
