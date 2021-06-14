"""
CLI end point functions
"""

from ..api import mine_missing_from_file
from .missing_parser import missing_parser


def main(argv=None):
    """
    End point for mine_missing_features CLI.
    Parameters
    ----------
    argv: list of command line arguments.

    Returns
    -------
    0
    """
    args = missing_parser(argv)

    missing_results = mine_missing_from_file(args.FilePath, args.sheet_name)
    if args.method.lower() == "markdown":
        markdown = missing_results.to_markdown()
        with open(args.markdown_path, "w") as file:
            file.write(markdown)
    else:
        print(missing_results)

    return 0
