# SyntaxP, the ANSI color library.

import re

# ANSI Colors
COLOR_BLACK="\033[0;30m"
COLOR_RED="\033[0;31m"
COLOR_GREEN="\033[0;32m"
COLOR_BROWN="\033[0;33m"
COLOR_BLUE="\033[0;34m"
COLOR_PURPLE="\033[0;35m"
COLOR_CYAN="\033[0;36m"
COLOR_LIGHT_GRAY="\033[0;37m"
COLOR_DARK_GRAY="\033[1;30m"
COLOR_LIGHT_RED="\033[1;31m"
COLOR_LIGHT_GREEN="\033[1;32m"
COLOR_YELLOW="\033[1;33m"
COLOR_LIGHT_BLUE="\033[1;34m"
COLOR_LIGHT_PURPLE="\033[1;35m"
COLOR_LIGHT_CYAN="\033[1;36m"
COLOR_LIGHT_WHITE="\033[1;37m"
COLOR_BOLD="\033[1m"
COLOR_FAINT="\033[2m"
COLOR_ITALIC="\033[3m"
COLOR_UNDERLINE="\033[4m"
COLOR_BLINK="\033[5m"
COLOR_NEGATIVE="\033[7m"
COLOR_CROSSED="\033[9m"
COLOR_RESET="\033[0m"

def cvert(string: str, colorbleed: bool = False) -> str:
    replacements = {
        "[syntaxp-black]": COLOR_BLACK,
        "[syntaxp-red]": COLOR_RED,
        "[syntaxp-green]": COLOR_GREEN,
        "[syntaxp-brown]": COLOR_BROWN,
        "[syntaxp-blue]": COLOR_BLUE,
        "[syntaxp-purple]": COLOR_PURPLE,
        "[syntaxp-cyan]": COLOR_CYAN,
        "[syntaxp-light-gray]": COLOR_LIGHT_GRAY,
        "[syntaxp-dark-gray]": COLOR_DARK_GRAY,
        "[syntaxp-light-red]": COLOR_LIGHT_RED,
        "[syntaxp-light-green]": COLOR_LIGHT_GREEN,
        "[syntaxp-yellow]": COLOR_YELLOW,
        "[syntaxp-light-blue]": COLOR_LIGHT_BLUE,
        "[syntaxp-light-purple]": COLOR_LIGHT_PURPLE,
        "[syntaxp-light-cyan]": COLOR_LIGHT_CYAN,
        "[syntaxp-light-white]": COLOR_LIGHT_WHITE,
        "[syntaxp-bold]": COLOR_BOLD,
        "[syntaxp-faint]": COLOR_FAINT,
        "[syntaxp-italic]": COLOR_ITALIC,
        "[syntaxp-underline]": COLOR_UNDERLINE,
        "[syntaxp-blink]": COLOR_BLINK,
        "[syntaxp-negative]": COLOR_NEGATIVE,
        "[syntaxp-crossed]": COLOR_CROSSED,
        "[syntaxp-reset]": COLOR_RESET,
    }
    for key, value in replacements.items():
        string = string.replace(key, value)
    return string if colorbleed else string + COLOR_RESET

def detect_language(filename: str) -> str:  # sourcery skip: use-next
    ext_map = {
        ".py": "python", ".c": "c", ".cpp": "c++", ".cc": "c++", ".rb": "ruby",
        ".rs": "rust", ".html": "html", ".htm": "html", ".css": "css",
        ".js": "javascript", ".sh": "shell", ".bash": "shell"
    }
    for ext, lang in ext_map.items():
        if filename.endswith(ext):
            return lang
    return "plain"

def highlight(code: str, lang: str = "python") -> str:
    def wrap_keywords(code: str, keywords: list) -> str:
        for kw in keywords:
            code = re.sub(rf'\b{kw}\b', f"{COLOR_YELLOW}{kw}{COLOR_RESET}", code)
        return code

    def highlight_common(code: str) -> str:
        code = re.sub(r'(\b\w+)(?=\s*\()', f"{COLOR_LIGHT_BLUE}\1{COLOR_RESET}", code)  # functions
        code = re.sub(r'(\b\d+(\.\d+)?\b)', f"{COLOR_CYAN}\1{COLOR_RESET}", code)      # numbers
        return code

    def highlight_python(code: str) -> str:
        code = re.sub(r'#.*', f"{COLOR_DARK_GRAY}\g<0>{COLOR_RESET}", code)
        code = re.sub(r'(\".*?\"|\'.*?\')', f"{COLOR_GREEN}\1{COLOR_RESET}", code)
        keywords = [
            "def", "return", "if", "elif", "else", "for", "while", "break", "continue",
            "import", "from", "as", "class", "try", "except", "finally", "with", "lambda",
            "True", "False", "None", "and", "or", "not", "in", "is", "pass", "yield", "raise"
        ]
        return highlight_common(wrap_keywords(code, keywords))

    def highlight_c(code: str) -> str:
        code = re.sub(r'//.*', f"{COLOR_DARK_GRAY}\g<0>{COLOR_RESET}", code)
        code = re.sub(r'(\".*?\")', f"{COLOR_GREEN}\g<0>{COLOR_RESET}", code)
        keywords = [
            "int", "float", "double", "char", "return", "if", "else", "for", "while", "break",
            "continue", "void", "struct", "typedef", "const", "include", "#define"
        ]
        return highlight_common(wrap_keywords(code, keywords))

    def highlight_ruby(code: str) -> str:
        code = re.sub(r'#.*', f"{COLOR_DARK_GRAY}\g<0>{COLOR_RESET}", code)
        code = re.sub(r'(\".*?\"|\'.*?\')', f"{COLOR_GREEN}\g<0>{COLOR_RESET}", code)
        keywords = [
            "def", "end", "if", "elsif", "else", "unless", "case", "when", "while", "until",
            "for", "in", "do", "begin", "rescue", "ensure", "yield", "return", "class", "module",
            "self", "nil", "true", "false", "and", "or", "not", "super", "then", "next", "redo", "retry"
        ]
        return highlight_common(wrap_keywords(code, keywords))

    def highlight_rust(code: str) -> str:
        code = re.sub(r'//.*', f"{COLOR_DARK_GRAY}\g<0>{COLOR_RESET}", code)
        code = re.sub(r'/\*.*?\*/', f"{COLOR_DARK_GRAY}\g<0>{COLOR_RESET}", code, flags=re.DOTALL)
        code = re.sub(r'(\".*?\"|\'.*?\')', f"{COLOR_GREEN}\g<0>{COLOR_RESET}", code)
        code = re.sub(r'(\b\w+!)', f"{COLOR_LIGHT_BLUE}\1{COLOR_RESET}", code)
        keywords = [
            "fn", "let", "mut", "const", "static", "match", "if", "else", "loop", "while",
            "for", "in", "break", "continue", "return", "impl", "trait", "struct", "enum",
            "use", "mod", "pub", "crate", "super", "self", "as", "ref", "type", "where",
            "move", "unsafe", "async", "await", "dyn", "true", "false"
        ]
        return highlight_common(wrap_keywords(code, keywords))

    def highlight_html(code: str) -> str:
        code = re.sub(r'<!--.*?-->', f"{COLOR_DARK_GRAY}\g<0>{COLOR_RESET}", code, flags=re.DOTALL)
        code = re.sub(r'(<\/?[a-zA-Z0-9]+)', f"{COLOR_BLUE}\1{COLOR_RESET}", code)
        code = re.sub(r'([a-zA-Z\-]+)(=)', f"{COLOR_PURPLE}\1{COLOR_RESET}\2", code)
        code = re.sub(r'(\".*?\"|\'.*?\')', f"{COLOR_GREEN}\1{COLOR_RESET}", code)
        return code

    def highlight_css(code: str) -> str:
        code = re.sub(r'/\*.*?\*/', f"{COLOR_DARK_GRAY}\g<0>{COLOR_RESET}", code, flags=re.DOTALL)
        code = re.sub(r'^([^\{\}\n]+)(\{)', f"{COLOR_BLUE}\1{COLOR_RESET}\2", code, flags=re.MULTILINE)
        code = re.sub(r'([a-zA-Z\-]+)(\s*:\s*)', f"{COLOR_PURPLE}\1{COLOR_RESET}\2", code)
        code = re.sub(r'(:\s*)([^;]+)(;)', f"\1{COLOR_GREEN}\2{COLOR_RESET}\3", code)
        return code

    def highlight_js(code: str) -> str:
        code = re.sub(r'//.*', f"{COLOR_DARK_GRAY}\g<0>{COLOR_RESET}", code)
        code = re.sub(r'/\*.*?\*/', f"{COLOR_DARK_GRAY}\g<0>{COLOR_RESET}", code, flags=re.DOTALL)
        code = re.sub(r'(\".*?\"|\'.*?\'|`.*?`)', f"{COLOR_GREEN}\1{COLOR_RESET}", code)
        code = re.sub(r'=>', f"{COLOR_LIGHT_PURPLE}=>{COLOR_RESET}", code)
        keywords = [
            "var", "let", "const", "function", "return", "if", "else", "for", "while", "do",
            "switch", "case", "break", "continue", "new", "try", "catch", "finally", "throw",
            "typeof", "instanceof", "in", "of", "this", "class", "extends", "super", "import",
            "export", "default", "await", "async", "true", "false", "null", "undefined"
        ]
        return highlight_common(wrap_keywords(code, keywords))

    def highlight_shell(code: str) -> str:
        code = re.sub(r'#.*', f"{COLOR_DARK_GRAY}\g<0>{COLOR_RESET}", code)
        code = re.sub(r'(\".*?\"|\'.*?\')', f"{COLOR_GREEN}\1{COLOR_RESET}", code)
        code = re.sub(r'(\$\{?[a-zA-Z_][a-zA-Z0-9_]*\}?)', f"{COLOR_CYAN}\1{COLOR_RESET}", code)
        code = re.sub(r'(\b\d+\b)', f"{COLOR_LIGHT_PURPLE}\1{COLOR_RESET}", code)
        keywords = [
            "echo", "cd", "ls", "pwd", "if", "then", "else", "elif", "fi", "for", "while", "in",
            "do", "done", "case", "esac", "function", "return", "exit", "read", "export", "unset",
            "source", "trap", "shift", "break", "continue", "true", "false"
        ]
        return highlight_common(wrap_keywords(code, keywords))

    highlighters = {
        "python": highlight_python,
        "c": highlight_c,
        "c+": highlight_c,
        "c++": highlight_c,
        "ruby": highlight_ruby,
        "rust": highlight_rust,
        "html": highlight_html,
        "css": highlight_css,
        "javascript": highlight_js,
        "js": highlight_js,
        "shell": highlight_shell,
        "sh": highlight_shell,
        "bash": highlight_shell
    }

    return highlighters.get(lang.lower(), lambda c: c)(code)
