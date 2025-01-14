# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2024 FPGAwars
# -- Authors
# --  * Jesús Arroyo (2016-2019)
# --  * Juan Gonzalez (obijuan) (2019-2024)
# -- Licence GPLv2
"""Implement the apio upload command"""

from pathlib import Path
import click
from click.core import Context
from apio.managers.scons import SCons
from apio.managers.drivers import Drivers
from apio import util
from apio.commands import options


# ---------------------------
# -- COMMAND SPECIFIC OPTIONS
# ---------------------------
sram_option = click.option(
    "sram",  # Var name.
    "-s",
    "--sram",
    is_flag=True,
    help="Perform SRAM programming.",
)

flash_option = click.option(
    "flash",  # Var name.
    "-f",
    "--flash",
    is_flag=True,
    help="Perform FLASH programming.",
)


# ---------------------------
# -- COMMAND
# ---------------------------

HELP = """
The uploade command builds the bitstream file (similar to the
build command) and uploaded it to the FPGA board.
The commands is typically used in the root directory
of the project that that contains the apio.ini file.

\b
Examples:
  apio upload

[Note] The flags marked with (deprecated) are not recomanded.
Instead, use an apio.ini project config file and if neaded, add
to the project custom boards.json and fpga.json files.
"""


# R0913: Too many arguments (6/5)
# pylint: disable=R0913
# R0914: Too many local variables (16/15) (too-many-locals)
# pylint: disable=R0914
@click.command(
    "upload",
    short_help="Upload the bitstream to the FPGA.",
    help=HELP,
    context_settings=util.context_settings(),
)
@click.pass_context
@options.project_dir_option
@options.serial_port_option
@options.ftdi_id
@sram_option
@flash_option
@options.verbose_option
@options.verbose_yosys_option
@options.verbose_pnr_option
@options.top_module_option_gen()
@options.board_option_gen()
def cli(
    ctx: Context,
    # Options
    project_dir: Path,
    serial_port: str,
    ftdi_id: str,
    sram: bool,
    flash: bool,
    verbose: bool,
    verbose_yosys: bool,
    verbose_pnr: bool,
    # Deprecated options
    top_module: str,
    board: str,
):
    """Implements the upload command."""

    # -- Create a drivers object
    drivers = Drivers()

    # -- Only for MAC
    # -- Operation to do before uploading a design in MAC
    drivers.pre_upload()

    # -- Create the SCons object
    scons = SCons(project_dir)

    # -- Construct the configuration params to pass to SCons
    # -- from the arguments
    config = {
        "board": board,
        "verbose": {
            "all": verbose,
            "yosys": verbose_yosys,
            "pnr": verbose_pnr,
        },
        "top-module": top_module,
    }

    # -- Construct the programming configuration
    prog = {
        "serial_port": serial_port,
        "ftdi_id": ftdi_id,
        "sram": sram,
        "flash": flash,
    }

    # Run scons: upload command
    exit_code = scons.upload(config, prog)

    # -- Only for MAC
    # -- Operation to do after uploading a design in MAC
    drivers.post_upload()

    # -- Done!
    ctx.exit(exit_code)


# Advanced notes: https://github.com/FPGAwars/apio/wiki/Commands#apio-upload
