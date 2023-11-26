import cudf
import re
import argparse

# create parser
parser = argparse.ArgumentParser(
    description='Find regex matches in a file using cudf.')
parser.add_argument('file_path', help='The path to the file.')
parser.add_argument(
    '--regex', default=r"(?:(?:https?|ftp)://)?(?:www\.)?([a-zA-Z0-9\-]+\.[a-zA-Z]{2,})(?::\d+)?(?:/[^ \n]*)?", help='The regex pattern to match.')

# parse arguments
args = parser.parse_args()

# use cudf to read the file into memory
try:
    df = cudf.read_csv(args.file_path)
    print(df)
except Exception as e:
    print('Error: ', str(e))
    exit()

# compile regex and make it ok for cudf
try:
    regex_compiled = re.compile(args.regex)
    regex_pattern_cudf = regex_compiled.pattern
except re.error:
    print('Error: Invalid regex pattern')
    exit()

# Use cudf to find matches in the file using the regex pattern
try:
    for column in df.columns:
        if cudf.api.types.is_string_dtype(df[column]):
            df[column] = df[column].str.contains(regex_pattern_cudf)
    print(df)
except Exception as e:
    print('Error: ', str(e))
