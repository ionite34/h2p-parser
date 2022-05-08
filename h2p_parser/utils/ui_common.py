from InquirerPy import inquirer
from InquirerPy.validator import PathValidator
from InquirerPy.utils import color_print as cp


def prompt_d_input():
    """
    Prompts for input directory.
    """
    return inquirer.filepath(
        message='Select input directory:',
        mandatory=True,
        validate=PathValidator(is_dir=True, message='Input must be a directory.')
    ).execute()


def prompt_f_input():
    """
    Prompts for input file.
    """
    return inquirer.filepath(
        message='Select input file:',
        mandatory=True,
        validate=PathValidator(is_file=True, message='Input must be a file.')
    ).execute()


def prompt_f_output():
    """
    Prompts for output file.
    """
    return inquirer.filepath(
        message='Select output file:',
        mandatory=True,
        validate=PathValidator(is_file=True, message='Output must be a file.')
    ).execute()


def pr_sep():
    """Print separator line"""
    cp([("#4ce5c8", "-" * 10)])
