
import sys
from shutil import get_terminal_size


def progress(count, total=0, status=''):

    def fit_terminal_size(s: str) -> str:
        terminal_line_len, _ = get_terminal_size(fallback=(123, 456))
        if len(s) > terminal_line_len:
            s = s[:(terminal_line_len - 10)]
        else:
            s = s + " " * (terminal_line_len - len(s)-10)
        return s

    if total > 0:
        bar_len = 60

        if count > total:
            count = total

        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        if percents > 100:
            percents = 100

        bar = '[' + '=' * filled_len + '-' * (bar_len - filled_len) + ']'

        output_str = fit_terminal_size(bar + " {0}% {1}".format(percents, status))

        sys.stdout.write('%s\r' % output_str)
        sys.stdout.flush()
    else:
        output_str = fit_terminal_size("{0} {1}".format(count, status))
        sys.stdout.write('%s\r' % output_str)
        sys.stdout.flush()
