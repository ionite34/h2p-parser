# File parse interface
from collections import Counter
from .ui_common import *
from . import parser
from InquirerPy.utils import color_print as cp


class UIParseFile:
    def __init__(self):
        pass

    def execute_info(self):
        # Select input file
        input_file = prompt_f_input()
        if not input_file:
            return

        # Ask for delimiter
        delimiter = inquirer.text(
            message='Enter delimiter:',
            default='|'
        ).execute()
        if not delimiter:
            return

        self.parse_file(input_file, delimiter)

    def parse_file(self, input_file, delimiter):
        # Run Process
        rs = parser.parse_file(input_file, delimiter)

        # Print results
        cp([("#e5c07b", "Unresolved Words")])
        cp([("red", "[All]: "),
            ("white", f"{len(rs.unres_all_words)}/{len(rs.all_words)}")])
        cp([("lightblue", "[Unique]: "),
            ("white", f"{len(rs.unres_words)}/{len(rs.words)}")])
        pr_sep()
        cp([("#e5c07b", "Unresolved Lines")])
        cp([("red", "[All]: "),
            ("white", f"{len(rs.unres_all_lines)}/{len(rs.all_lines)}")])
        cp([("lightblue", "[Unique]: "),
            ("white", f"{len(rs.unres_lines)}/{len(rs.lines)}")])
        pr_sep()
        cp([("#e5c07b", "Expected Coverage")])
        cp([("#d21205", "[Lines, CMUDict only]: "),
            ("white", f"{len(rs.all_lines_only_cmu)}/{len(rs.all_lines)} | {rs.line_coverage_cmu()}%")])
        cp([("#d21205", "[Lines, CMUDict + H2p]: "),
            ("white", f"{rs.get_lines_cmu_h2p()}/{len(rs.all_lines)} | {rs.line_coverage_cmu_het()}%")])
        cp([("#c8bd20", "[Lines, All features]: "),
            ("white", f"{rs.get_lines_res()}/{len(rs.all_lines)} | {rs.line_coverage()}%")])
        cp([("#25a0c8", "[Words]: "),
            ("white", f"{rs.word_coverage()}%")])
        pr_sep()
        cp([("#e5c07b", "H2p parser")])
        cp([("#d21205", "[Lines with Heteronyms]: "),
            ("white", f"{len(rs.all_lines_cont_het)}/{len(rs.all_lines)} | {rs.percent_line_het()}%")])
        cp([("#7e3b41", "[Words Resolved by H2p]: "),
            ("white", f"{rs.n_words_het}/{rs.n_words_res} | {rs.percent_word_h2p()}%")])
        # Calcs
        feature_res = rs.n_words_fet
        feature_percent = round(feature_res / rs.n_words_res * 100, 2)
        cmu_res = rs.n_words_cmu
        cmu_percent = round(cmu_res / rs.n_words_res * 100, 2)
        cp([("#c8bd20", "[Transformed Resolves]: "),
            ("white", f"{feature_res}/{rs.n_words_res} | {feature_percent}%")])
        cp([("#25a0c8", "[Words in CMUDict]: "),
            ("white", f"{cmu_res}/{rs.n_words_res} | {cmu_percent}%")])
        pr_sep()
        cp([("#e5c07b", "Feature Usage")])
        # Loop through feature results
        for ft in rs.ft_stats:
            cp([("#d21205", f"{ft}: "), ("white", f"{rs.ft_stats[ft]}/{rs.n_words_res}"
                                                  f" | {round(rs.ft_stats[ft] / rs.n_words_res * 100, 2)}%")])
        pr_sep()
        # Print 100 sampled unresolved words by frequency
        cp([("#e5c07b", "Top 100 most frequent unresolved words")])
        # Count frequency of words
        word_freq = Counter(rs.unres_all_words)
        # Sort by frequency
        word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        # Print top 100
        for word, freq in word_freq[:100]:
            cp([("#d21205", f"{word}: "),
                ("#ffffff", f"{freq}")])
