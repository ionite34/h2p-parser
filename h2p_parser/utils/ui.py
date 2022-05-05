# Extended Main User Interface Methods
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
# noinspection PyProtectedMember
from InquirerPy.base.control import Separator
from InquirerPy.utils import color_print as cp
from .. import dict_cache
from .parse_line import UIParseLine
from .diff_check import UIDiffCheck
from .parse_file import UIParseFile


# Prompt choices of parsing
def prompt_parsing_choices():
    choices = [
        Choice("use-cache", name="Use Cache", enabled=True),
        Separator(),
        Choice("ft_numbers", name="Numbers | (i.e. 8,100 -> (eighty-one hundred)", enabled=True),
        Choice("ft_currency", name="Currency | (i.e. $1.56 -> (one dollar, fifty-six cents)", enabled=True),
        Separator(),
        Choice("ft_plural", name="Plurals", enabled=True),
        Choice("ft_possessive", name="Possessives | ('s)", enabled=True),
        Choice("ft_contractions", name="Contractions | ('ll, 'd)", enabled=True),
        Choice("ft_hyphenated", name="Hyphenated | (i.e. Check-in -> (check, in)", enabled=True),
        Choice("ft_compound", name="Compound Words | (i.e. Riverwood -> (river, wood)", enabled=True),
        Choice("ft_compound", name="Stemming (Morphological Affixes) | (i.e. Shockingly -> (shock + ing + ly)",
               enabled=True),
        Separator(),
        Choice("ft_compound_l2", name="Compound Words Lv2 | [Experimental]", enabled=False),
    ]
    features = inquirer.checkbox(
        message="Algorithmic Resolver options:",
        long_instruction="(space to toggle, enter to confirm)",
        choices=choices,
        cycle=False,
        max_height="80%",
        transformer=lambda result: f"{len(result)} option{'s' if len(result) > 1 else ''} selected",
    ).execute()

    return features


def menu_main():
    choices = [
        Choice("parse", name="Grapheme-Phoneme Parsing", enabled=True),
        Choice("local", name="Edit Custom Dictionary"),
        Choice("tests", name="Testing and Validation Tools"),
        Choice("cache", name="Cache Options"),
        Choice(value=None, name="Exit"),
    ]
    selections = inquirer.select(
        message="Main Menu:",
        choices=choices,
    ).execute()
    if selections is None:
        exit(0)  # Direct Exit
    if selections == "parse":
        menu_parse()
    elif selections == "local":
        print("Local Dictionary Editing is not yet implemented.")
        menu_main()
    elif selections == "tests":
        menu_tests()
    elif selections == "cache":
        menu_cache()


def menu_tests():
    choices = [
        Choice("diff_check", name="Check Dictionaries against CMUDict"),
        Choice(value=None, name="[Back]"),
    ]
    selections = inquirer.select(
        message="Tests and Validation Tools:",
        choices=choices,
        default="diff_check",
    ).execute()
    if selections is None:
        menu_main()
    elif selections == "diff_check":
        UIDiffCheck().execute()


def menu_parse():
    choices = [
        Choice("cmu_only", name="CMUDict | Parse text using only CMUDict", enabled=True),
        Choice("from_text", name="Text | Parses using standard features"),
        Choice("from_file", name="File | Parses text annotation .csv files"),
        Choice(value=None, name="[Back]"),
    ]
    selections = inquirer.select(
        message="Parsing modes:",
        choices=choices,
    ).execute()
    if selections is None:
        menu_main()
    elif selections == "cmu_only":
        pl = UIParseLine()
        pl.execute_cmu()
        menu_parse()
    elif selections == "from_text":
        print("Text Parsing is not yet implemented.")
        menu_parse()
    elif selections == "from_file":
        menu_parse_file()


def menu_parse_file():
    choices = [
        Choice("info", name="Coverage Info | Shows predicted conversion coverage and feature usage"),
        Choice("to_file", name="File Conversion | Converts text annotation .csv files to graphemes"),
        Separator("-" * 5),
        Choice(value=None, name="[Back]"),
    ]
    selections = inquirer.select(
        message="Grapheme to Phoneme Parsing, from .csv file:",
        choices=choices,
        default=choices[0],
    ).execute()
    if selections is None:
        menu_main()  # Back to main menu
    if selections == "to_file":
        print("File Conversion is not yet implemented.")
        menu_parse_file()
    elif selections == "info":
        UIParseFile().execute_info()
        menu_parse_file()


def menu_cache():
    choices = [
        Choice("clear-generated", name="Remove generated non-verified entries", enabled=True),
        Choice("clear-all", name="Remove all entries"),
        Separator("-" * 5),
        Choice(value=None, name="[Back]"),
    ]
    selections = inquirer.select(
        message="Cache Options:",
    ).execute()
    if selections is None:
        menu_main()  # Back to main menu
    # Create cache link
    cache = dict_cache.DictCache()
    if selections == "clear-generated":
        cache.clear_generated()
        print("Generated entries removed.")
