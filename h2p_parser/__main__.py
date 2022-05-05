from collections import Counter

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from h2p_parser.utils import converter
from h2p_parser.utils import ui


def convert_h2p(input_file, output_file, delimiter):
    """
    Converts a h2p dictionary file from one format to another.
    """
    converter.bin_delim_to_json(input_file, output_file, delimiter)
    print('Converted h2p_dict to json.')


def prompt_action() -> str:
    action = inquirer.select(
        message='Select action:',
        choices=[
            "Convert",
            "Parse",
            Choice(value=None, name='Exit')
        ],
        default=0,
    ).execute()
    if not action:
        exit(0)
    return action


def action_convert():
    pass
    """
    Converts a h2p dictionary file from one format to another.
    """
    # Select input file
    input_file = prompt_f_input()
    if not input_file:
        return

    # Select output file
    output_file = prompt_f_output()
    if not output_file:
        return

    # Ask for delimiter
    delimiter = inquirer.text(
        message='Enter delimiter:',
        default='|'
    ).execute()
    if not delimiter:
        return

    # Run Process
    convert_h2p(input_file, output_file, delimiter)


if __name__ == "__main__":
    ui.menu_main()
