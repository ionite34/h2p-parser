# __main__.py

import asyncio
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from h2p_parser.utils import converter


async def convert(file_type, input_file, output_file):
    """
    Converts a dictionary file from one format to another.
    """
    if file_type == 'h2p_dict':
        await asyncio.run(converter.bin_delim_to_json(input_file, output_file))
        print('Converted h2p_dict to json.')


async def entry():
    """
    Prints help information.
    """
    # Select action type
    action = await inquirer.select(
        message='Select action:',
        choices=[
            "Convert delimited h2p_dict to json",
            Choice(value=None, name='Exit')
        ],
        default=0,
    ).execute_async()

    if not action:
        return

    # Select input file
    input_file = await inquirer.filepath(
        message='Select input file:'
    ).execute_async()

    if not input_file:
        return

    # Select output file
    output_file = await inquirer.filepath(
        message='Select output file:'
    ).execute_async()

    if not output_file:
        return

    # Ask for delimiter
    delimiter = await inquirer.text(
        message='Enter delimiter:',
        default='|'
    ).execute_async()

    if not delimiter:
        return

    # Run Process
    converter.bin_delim_to_json(input_file, output_file, delimiter)
    print('Converted h2p_dict to json.')


def main():
    """
    Main function for the h2p_parser package.
    """
    # check cli arguments
    pass


if __name__ == "__main__":
    asyncio.run(entry())
