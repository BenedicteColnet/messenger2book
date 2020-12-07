import pandas as pd

time_col_name = 'datetime'


def add_timing_to_df(concatenated_table):
    # format datetime
    concatenated_table[time_col_name] = pd.to_datetime(
        concatenated_table[time_col_name])

    # sort by datetime
    concatenated_table = concatenated_table.sort_values(
        time_col_name).reset_index(drop=True)

    # add 'date' column
    concatenated_table['date'] = concatenated_table[time_col_name].dt.date

    # add columns for pretty date and time as strings
    concatenated_table['dateStr'] = concatenated_table[time_col_name].apply(
        lambda x: x.strftime("%A %d %B").replace(' 0', ' '))  # "%A %d %B %Y": +year
    concatenated_table['timeStr'] = concatenated_table[time_col_name].apply(
        lambda x: x.strftime("%H:%M"))

    # add boolean colum specifying who is the "right" (as opposed to "left") sender
    right_sender = "M"  # Hard coded for Marc
    concatenated_table['right'] = (
        concatenated_table['sender'] == right_sender)

    # add sender group id column (on a given date, helper column to handle consecutive messages by the same sender)
    def f(concatenated_table):
        s = (concatenated_table['right'].shift()
             != concatenated_table['right'])
        s.iloc[0] = False
        return s.cumsum()

    concatenated_table['senderGroup'] = concatenated_table.groupby(
        'date', as_index=False).apply(f).reset_index(drop=True)

    return concatenated_table
