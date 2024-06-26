import customtkinter as tk


class LabelGrid(tk.Frame):
    """
    Creates a grid of labels that have their cells populated by content.
    """
    def __init__(self, master, content=([0, 0], [0, 0]), *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.content = content
        self.content_size = (len(content), len(content[0]))
        self._create_labels()
        self._display_labels()


    def _create_labels(self):
        def __put_content_in_label(row, column):
            content = self.content[row][column]
            content_type = type(content).__name__
            if content_type in ('str', 'int'):
                self.labels[row][column]['text'] = content
            elif content_type == 'PhotoImage':
                self.labels[row][column]['image'] = content


        self.labels = list()
        for i in range(self.content_size[0]):
            self.labels.append(list())
            for j in range(self.content_size[1]):
                self.labels[i].append(tk.Label(self))
                __put_content_in_label(i, j)


    def _display_labels(self):
        for i in range(self.content_size[0]):
            for j in range(self.content_size[1]):
                self.labels[i][j].grid(row=i, column=j)