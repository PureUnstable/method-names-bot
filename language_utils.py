import regex_utils as regex_utils

languages = {
    "java": {
        "ends_with": ".java",
        "regex": regex_utils.c_like_regex
    }
}

# Languages
languages = {
    "java",
    "cs",
    "cpp",
    "c",
    "rust"
}

languages_extensions = {
    '(\.java$)',
    '(\.cs$)',
    '(\.[c|h][p]{2}$)',
    '(\.[c|h]$)',
}