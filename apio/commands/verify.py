# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2024 FPGAwars
# -- Authors
# --  * Jesús Arroyo (2016-2019)
# --  * Juan Gonzalez (obijuan) (2019-2024)
# -- Licence GPLv2
"""Main implementation of APIO VERIFY command"""

from pathlib import Path
import click
from click.core import Context
from apio.managers.scons import SCons
from apio import util
from apio.commands import options


# ---------------------------
# -- COMMAND
# ---------------------------

HELP = """
The verify command performs a shallow verification of the verilog code
it finds without requiring a top module or a constraint file.
Is useful mainly in early stages of the project, before the
strictier build and lint commands can be used.
The verify commands is typically used in the root directory
of the project that that contains the apio.ini file.

\b
Examples:
  apio verify

"""


@click.command(
    "verify",
    short_help="Verify project's verilog code.",
    help=HELP,
    context_settings=util.context_settings(),
)
@click.pass_context
@options.project_dir_option
@options.verbose_option
@options.board_option_gen()
def cli(
    ctx: Context,
    # Options
    project_dir: Path,
    verbose: bool,
    # Deprecated options
    board: str,
):
    """Implements the verify command."""

    # -- Crete the scons object
    scons = SCons(project_dir)

    # -- Verify the project with the given parameters
    exit_code = scons.verify(
        {
            "board": board,
            "verbose": {"all": verbose, "yosys": False, "pnr": False},
        }
    )

    # -- Done!
    ctx.exit(exit_code)
