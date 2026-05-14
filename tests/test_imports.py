"""Smoke tests that every package module imports cleanly.

Catches broken refactors, circular imports, and missing dependencies
without needing a live Discord connection or any environment variables.
"""

import importlib

import pytest

MODULES = [
    "src",
    "src.commands",
    "src.commands.affixes",
    "src.commands.bluetrack",
    "src.commands.checklist",
    "src.commands.cutoffs",
    "src.commands.help",
    "src.commands.test",
    "src.commands.time",
    "src.commands.warning",
    "src.commands.wowhead_news",
    "src.tasks",
    "src.tasks.scheduler",
    "src.utils",
    "src.utils.api",
    "src.utils.blue_tracker",
    "src.utils.embeds",
    "src.utils.error_handler",
    "src.utils.wowhead_news",
]


@pytest.mark.parametrize("module_name", MODULES)
def test_module_imports(module_name):
    importlib.import_module(module_name)
