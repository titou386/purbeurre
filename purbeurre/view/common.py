"""Common methodes to pages."""
import os


class GenericFormatting:
    """Fomatting results in terminal."""

    def __init__(self):
        """Constructor."""
        self.term_columns = 0

    def get_terminal_size(self):
        """Determine and fill values terminal width and height."""
        self.term_columns = os.get_terminal_size().columns

    def format_results(self, iterable):
        """Try to display on a maximum of columns.

        Parameters:
            irerable(list): A list of str.
        """
        if not iterable:
            print("\nAucun résultat à votre recherche")
            return
        iterable = [i.replace('\n', ' ') for i in iterable]
        self.get_terminal_size()

        narrowest = min(len(x) for x in iterable)
        nb_col = self.term_columns // (narrowest + 8)

        # Calculate the nb of columns and lines
        while True:
            nb_lines = len(iterable) // nb_col
            if (len(iterable) % nb_col):
                nb_lines += 1
            nb_col = len(iterable) // nb_lines
            if len(iterable) % nb_lines:
                nb_col += 1

            col_widths = [max(len(item) + 8 for i, item in enumerate(iterable)
                          if i // nb_lines == col) for col in range(nb_col)]
            if sum(col_widths) <= self.term_columns:
                break
            else:
                nb_col -= 1

        # Output formating
        for line in range(nb_lines):
            for col in range(nb_col):
                index = col * nb_lines + line
                if index >= len(iterable):
                    continue
                print("%*d- %-*s" % (3, index, col_widths[col] - 6,
                      iterable[index]), end='')
            print()
