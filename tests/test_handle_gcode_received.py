import sys
from pathlib import Path
from os.path import dirname

sys.path.append(str(Path(dirname(__file__), "../").absolute()))
sys.path.append(str(Path(dirname(__file__), "../../OctoPrint/src").absolute()))
sys.path.append(str(Path(dirname(__file__), "../../OctoPrint/venv/lib/python3.8/site-packages").absolute()))

import logging

import pytest
from mock import call

from octoprint_mmu_load_events import Mmu_load_eventsPlugin

@pytest.fixture()
def mock_eventManager(mocker):
    mock_fire = mocker.Mock()
    mock_constructor = mocker.Mock(return_value=mock_fire)
    mocker.patch("octoprint_mmu_load_events.eventManager", return_value=mock_constructor)
    return mock_constructor

def test_ideal(mock_eventManager):
    comm_instance = None
    line = "MMU can_load:OOOooooooOOOOOOOOOOO succeeded."
    plugin = Mmu_load_eventsPlugin()
    plugin._logger = logging.getLogger(__name__)
    plugin.handle_gcode_received(comm_instance, line=line)
    assert mock_eventManager.fire.call_args_list == [
        call('PLUGIN_MMU_LOAD_EVENTS_SUCCESS', {'line': 'MMU can_load:OOOooooooOOOOOOOOOOO succeeded.', 'filamentDetect': 'OOOooooooOOOOOOOOOOO', 'success': True})
    ]

SUCCESS_SAMPLES = [
    [
        "echo:busy: processing",
        "MMU can_load:",
        "OOOOOOOOOOOOOOOOOecho:busy: processing",
        "OOOOOOOOOOOOO succeeded.",
        "tmc2130_home_enter(axes_mask=0x04)",
        "echo:busy: processing",
    ],
    [
        "echo:busy: processing",
        "MMU can_load:",
        "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO succeeded.",
        "echo:busy: processing",
    ],
    [
        "MMU can_load:",
        "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO succeeded.",
        "echo:busy: processing",
    ],
    [
        "echo:busy: processing",
        "MMU can_load:",
        "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO succeeded.",
        "tmc2130_home_enter(axes_mask=0x04)",
    ],
    [
        "echo:busy: processing",
        "MMU can_load:",
        "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO succeeded.",
        "echo:busy: processing",
    ],
    [
        "MMU can_load:",
        "OOOOOOOOOOOOOOOOOOOOOOOOOOOOecho:busy: processing",
        "OO succeeded."
    ]
]


FAIL_SAMPLES = [
    [
        "echo:busy: processing",
        "MMU can_load:",
        "OOOOOOOOOOOOOOOOOecho:busy: processing",
        "OOOOO11111111 failed.",
        "tmc2130_home_enter(axes_mask=0x04)",
        "echo:busy: processing",
    ],
    [
        "echo:busy: processing",
        "MMU can_load:",
        "OOOOOOOOOOOOOOOOOOOOOO11111111 failed.",
        "echo:busy: processing",
    ],
    [
        "MMU can_load:",
        "OOOOOOOOOOOOOOOOOOOOOO11111111 failed.",
        "echo:busy: processing",
    ],
    [
        "echo:busy: processing",
        "MMU can_load:",
        "OOOOOOOOOOOOOOOOOOOOOO11111111 failed.",
        "tmc2130_home_enter(axes_mask=0x04)",
    ],
    [
        "echo:busy: processing",
        "MMU can_load:",
        "OOOOOOOOOOOOOOOOOOOOOO11111111 failed.",
        "echo:busy: processing",
    ]
]

@pytest.mark.parametrize("log_lines", SUCCESS_SAMPLES)
def test_success_real_world(mock_eventManager, log_lines):
    plugin = Mmu_load_eventsPlugin()
    plugin._logger = logging.getLogger(__name__)
    for line in log_lines:
        plugin.handle_gcode_received(None, line=line)

    assert mock_eventManager.fire.call_args_list[0][0][0] == "PLUGIN_MMU_LOAD_EVENTS_SUCCESS"
    assert mock_eventManager.fire.call_args_list[0][0][1]['filamentDetect'] == "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"

@pytest.mark.parametrize("log_lines", FAIL_SAMPLES)
def test_failed_real_world(mock_eventManager, log_lines):
    plugin = Mmu_load_eventsPlugin()
    plugin._logger = logging.getLogger(__name__)
    for line in log_lines:
        plugin.handle_gcode_received(None, line=line)

    assert mock_eventManager.fire.call_args_list[0][0][0] == "PLUGIN_MMU_LOAD_EVENTS_FAILED"
    assert mock_eventManager.fire.call_args_list[0][0][1]['filamentDetect'] == "OOOOOOOOOOOOOOOOOOOOOO11111111"
