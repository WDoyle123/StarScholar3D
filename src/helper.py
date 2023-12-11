def print_all(df):
    for row in df.alt_name:
        print(row)

    print(len(df))

import re

def greek_letter(df, greek_letter):
    '''
    Exclude rows where the alt_name in the data frame starts with a greek letter
    for the specified constellation and is improperly followed by another constellation abbreviation.
    Allow rows where the Greek letter is repeated or correctly used.
    '''
    # Adjusted pattern to use non-capturing groups
    pattern_remove = re.compile(r"(?:\d+" + re.escape(greek_letter) + r"(?:\d+\w+|\s+\w+))|(?:^" + re.escape(greek_letter) + r"(?:\s+)?(?:\d+\w+|\w+))")

    # Apply the pattern and filter
    filtered_df = df[~df['alt_name'].str.contains(pattern_remove, regex=True)]
    return filtered_df

