def print_all(df):
    for row in df.alt_name:
        print(row)

    print(len(df))

def greek_letter(df, greek_letter):
    '''
    Exclude rows where the alt_name in the data frame contains a greek letter
    for example:

    Taurus constellations is Tau (a greek letter but also short for Taurus)
    The data_j2000.csv contains alt_names such as Tau Alp and UMa Tau
    '''
    pattern = r"(?!.*" + greek_letter + " " + greek_letter + ").*" + greek_letter + r"$"

    filtered_df = df[~df.alt_name.str.match(pattern)]

    return filtered_df

