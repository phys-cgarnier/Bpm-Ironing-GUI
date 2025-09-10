
import os
from pathlib import Path
import logging
from typing import Optional, List, Dict, Any
from iron_bpms import MainDisplay as IroningGui


def configure_logger(logging_file: Path) -> None:
    """
    Configures the logger for the application.
    """
    log_level = os.getenv("IRONING_GUI_LOG_LEVEL", "INFO").upper()
    log_file = os.getenv("IRONING_GUI_LOG_FILE", logging_file)
    logger = logging.getLogger(__name__)
    logger.basicConfig(filename=log_file, level=log_level)
    logger.setLevel(logging.DEBUG)

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(ch)

def create_gui(parent: Optional[object] = None,
               args: Optional[List[str]] = None,
               macros: Optional[Dict[str, Any]] = None) -> IroningGui:
    """
    Factory function to create an instance of the MainDisplay class from iron_bpms.py.

    Parameters:
    - parent: Optional parent widget.
    - args: Optional list of command-line arguments.
    - macros: Optional dictionary of macros for the GUI.

    Returns:
    - An instance of MainDisplay.
    """
    try:
        logging.getLogger(__name__).info("Starting MainDisplay with macros=%s", macros)
        gui_instance = IroningGui(parent=parent, args=args, macros=macros)
        return gui_instance
    except Exception as e:
        logging.error(f"Error creating GUI instance: {e}")
        raise



