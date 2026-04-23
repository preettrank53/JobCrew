# demo/__init__.py
from .demo_controller import (
    is_demo_mode,
    activate_demo_mode,
    deactivate_demo_mode,
    run_demo_pipeline,
    get_demo_banner_html,
)

__all__ = [
    "is_demo_mode",
    "activate_demo_mode",
    "deactivate_demo_mode",
    "run_demo_pipeline",
    "get_demo_banner_html",
]
