from typing import List
from IPython import get_ipython
import matplotlib.pyplot as plt
from io import BytesIO
import binascii
import base64


class Image:
    def __init__(self, fig: plt.Figure):
        self.fig = fig

    def render(self):
        bio = BytesIO()
        self.fig.savefig(bio, format='png', bbox_inches="tight")
        bio.seek(0)
        s = base64.b64encode(bio.getvalue()).decode("utf-8").replace("\n", "")
        plt.close(self.fig)
        return '<img src="data:image/png;base64,%s">' % s


class Row:
    def __init__(self, elements: List):
        self.elements = elements

    def column_element(self, el):
        return (f"""<div>{el.render()}</div>""")

    def render(self):
        inner = ''.join(
            [self.column_element(element) for element in self.elements])
        return (f"""<div class="row">{inner}</div>""")


class Figure:
    def __init__(self, figure: plt.Figure, caption: str):
        self.figure = Image(figure)
        self.caption = caption

    def render(self):
        return (
f"""<figure>{self.figure.render()}
<figcaption> {self.caption} <figcaption>  
</figure> """)


def render_figure(fig: Figure):
    return fig.render()


def render_row(r: Row):
    return r.render()


html_formatter = get_ipython().display_formatter.formatters['text/html']
html_formatter.for_type(Figure, render_figure)
html_formatter.for_type(Row, render_row)