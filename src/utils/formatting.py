import re
import pandas as pd


def process_for_latex(text: str):
    """Process text message for latex, adapt bold, italic, code and underline delimiters"""
    # telegram formating documentation: https://core.telegram.org/api/entities
    regexs = [
        (r"\*\*\*(:?.*?(?<!\*))\*\*\*",
         r"\\textbf{\\textit{\g<1>}}")  # bold & italic
        # bold & italic
        # bold
        # bold
        # bold
        , (r"___(:?.*?(?<!_))___", r"\\textbf{\\textit{\g<1>}}"), (r"\*\*(:?.*?(?<!\*))\*\*", r"\\textbf{\g<1>}"), (r"__(:?.*?(?<!_))__", r"\\textbf{\g<1>}"), (r"<b>(:?.*?)<\\b>", r"\\textbf{\g<1>}"), (r"<strong>(:?.*?)<\\strong>", r"\\textbf{\g<1>}")  # bold
        , (r"\*(:?.*?(?<!\*))\*", r"\\textit{\g<1>}")  # italic
        , (r"_(:?.*?(?<!_))_", r"\\textit{\g<1>}")  # italic
        , (r"<i>(:?.*?)<\\i>", r"\\textit{\g<1>}")  # italic
        , (r"<em>(:?.*?)<\\em>", r"\\textit{\g<1>}")  # italic
        , (r"<u>(:?.*?)<\\u>", r"\\underline{\g<1>}")  # underline
        , (r"<code>(:?.*?)<\\code>", r"\\texttt{\g<1>}")  # code
    ]  # Beware, regex sustitution order is important

    for regex, subst in regexs:
        text = re.sub(regex, subst, text, 0, re.MULTILINE)

    return text

def left_formating(df):
    if isinstance(df, pd.Series):
        df = pd.DataFrame(df).T
    
    table_rows = df.apply(
        lambda x: f'{x.timeStr}&{x.message}\\\\',  # format for left rows
        axis=1
    ).tolist()
    
    text = '\n'.join(
        ['\\noindent', '\\begin{tabular}{p{0.05\\textwidth}p{0.55\\textwidth}}'] +
        table_rows
        + ['\\end{tabular}'])
    
    return text

def left_formating_with_bubbles(df):
    if isinstance(df, pd.Series):
        df = pd.DataFrame(df).T
    
    table_rows = df.apply(
        lambda x: f'{x.message}\\',  # format for left rows
        axis=1
    ).tolist()
    
    text = '\n'.join(
        ['\\begin{leftbubbles}'] +
        table_rows
        + ['\\end{leftbubbles}']) 
    return text


def right_formating(df):
    if isinstance(df, pd.Series):
        df = pd.DataFrame(df).T
    
    table_rows = df.apply(
        lambda x: f'{x.message}&{x.timeStr}\\\\' if len(x.message) > 45 
                  else '\multicolumn{1}{r}' + f'{x.message}&{x.timeStr}\\\\',  # format for right rows
        axis=1
    ).tolist()
    
    text = '\n'.join(
        ['\\begin{flushright}', '\\noindent', '\\begin{tabular}{p{0.55\\textwidth}p{0.1\\textwidth}}'] +
        table_rows
        + ['\\end{tabular}', '\\end{flushright}'])

    return text

def right_formating_with_bubbles(df):
    if isinstance(df, pd.Series):
        df = pd.DataFrame(df).T

    
    table_rows = df.apply(
        lambda x: f'{x.message}\\', 
        axis=1
    ).tolist()
    
    text = '\n'.join(
        ['\\begin{rightbubbles}'] +
        table_rows
        + ['\\end{rightbubbles}'])

    return text

# By default it will apply bubbles style
def format_msg(df, bubbles = True):
    if bubbles:
        if df['right'].unique()[0]:
            return right_formating_with_bubbles(df)
        return left_formating_with_bubbles(df)
    else:
        if df['right'].unique()[0]:
            return right_formating(df)
        return left_formating(df)
