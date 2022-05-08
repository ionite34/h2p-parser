# Line parse interface
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
# noinspection PyProtectedMember
from InquirerPy.base.control import Separator
from InquirerPy.utils import color_print as cp

from . import ui
from .. import cmudictext
from .. import format_ph as fp


class UIParseLine:
    def __init__(self):
        self.cde = cmudictext.CMUDictExt()

    def execute_cmu(self, dict_source: dict = None):
        """
        Execute the line parse interface for CMU dictionary
        """

        if dict_source is None:
            dict_source = self.cde.dict

        while True:
            # Prompt user to select mode
            word = inquirer.fuzzy(
                message="Select word:",
                long_instruction="(Ctrl+C to exit)",
                choices=list(dict_source.keys()),
                keybindings={"toggle-exact": [{"key": "c-t"}]},
                raise_keyboard_interrupt=False,
                exact_symbol=" E",
                multiselect=False,
                validate=lambda result: (len(result) > 0 or result is None),
                invalid_message="Selection Required.",
                mandatory=False,
                max_height="70%",
            ).execute()

            if word is None:
                ui.menu_parse()  # Return to caller
                return
            else:
                # Get the word
                ph = fp.to_sds(dict_source.get(word))
                if ph is None:
                    cp([("#d21205", "No Entry Found.")])
                    print()
                    continue
                else:
                    # Print the word and pronunciation
                    cp([("crimson", f"{word}: "), ("white", ph)])
                    print()
                    continue
