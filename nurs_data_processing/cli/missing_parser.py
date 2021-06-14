"""
Arg parsers for missing mining cli.
"""
import argparse


def missing_parser(argv=None) -> argparse.Namespace:
    """
    Implement a command line parser for `nurs_reference_spider`.
    Returns
    -------
    argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        argv,
        description="Report on patterns in 'missingness' of data"
    )

    parser.add_argument(
        'FilePath', metavar='path',
        type=str, help='the path to the data set'
    )

    parser.add_argument(
        "-s", "--sheet",
        default=0,
        dest="sheet_name",
        required=False,
        type=str,
        help='Sheet name if calling excel data [optional]'
    )

    parser.add_argument(
        "-m", '--method',
        default="",
        dest="method",
        required=False,
        type=str,
        help='method for processing results'
    )

    parser.add_argument(
        "-e", '--export_path',
        default=".md", required=False,
        dest="markdown_path",
        type=str,
        help='File path to write results to'
    )

    return parser.parse_args(argv)
