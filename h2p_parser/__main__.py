from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator
from h2p_parser.utils import converter


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
            Choice(value=None, name='Exit')
        ],
        default=0,
    ).execute()
    if not action:
        exit(0)
    return action


def prompt_f_input():
    """
    Prompts for input file.
    """
    return inquirer.filepath(
        message='Select input file:',
        validate=PathValidator(is_file=True, message='Input must be a file.')
    ).execute()


def prompt_f_output():
    """
    Prompts for output file.
    """
    return inquirer.filepath(
        message='Select output file:',
        validate=PathValidator(is_file=True, message='Output must be a file.')
    ).execute()


def action_convert():
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


def entry():
    """
    Prints help information.
    """
    # Select action type
    action = prompt_action()
    if action == 'Convert':
        action_convert()


if __name__ == "__main__":
    entry()
