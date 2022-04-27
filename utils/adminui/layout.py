from .element import Element

class Card(Element):
    """A white-boxed container to hold content in sections
    
    Args:
        title: the title of the card container
        content: list of page elements inside the container
    """
    def __init__(self, title=None, content=None, id=None):
        super().__init__('Card', title=None, content=content, id=id)

class ChartCard(Element):
    """A card container with values, tooltips and a footer. Mostly used in dashboards
    
    Args:
        title: the container title
        value: (str), the big text shown on the card
        tooltip: the text shown when the user hover on the tooltip icon
        footer: list of page elements shown on the footer of the card
        content: list of page elements shown as the content of the card
        height: the height of the card, to make it looks consistant across columns
    """
    def __init__(self, title=None, value=None, tooltip=None, footer=None, content=None, height=46, id=None):
        super().__init__('ChartCard', title=title, value=value, tooltip=tooltip, footer=footer, content=content, height=height, id=id)

class DetailGroup(Element):
    """The container for DetailItem, used to display a record with multiple fields
    
    Args:
        title: the title of the detail group
        content: a list of DetailItem
    """
    def __init__(self, title='', content=None, id=None):
        super().__init__('DetailGroup', title=title, content=content, id=id)

class DetailItem(Element):
    """A little piece of text with a title and a value, used to display a field in a record
    
    Args:
        title: the title of the field
        value: the value of the field
    """
    def __init__(self, title='', value='', id=None):
        super().__init__('DetailItem', title=title, value=value, id=id)

class Divider(Element):
    """Place a divider on the screen"""
    def __init__(self, id=None):
        super().__init__('Divider', id=id)

class Header(Element):
    """Display a header text on the screen
    
    Args:
        text: text body of the header
        level: the header level. level=1 means a first level header(h1)
    """
    def __init__(self, text='', level=4, id=None):
        super().__init__('Header', text=text, level=level, id=id)

class Paragraph(Element):
    """Display a paragraph of text"""
    def __init__(self, text='', id=None, color=None):
        super().__init__('Paragraph', text=text, id=id, color=color)

class RawHTML(Element):
    """Display a (dangerous) HTML to the page"""
    def __init__(self, text='', id=None):
        super().__init__('RawHTML', text=text, id=id)

class Row(Element):
    """Display a row with multiple Columns for layout purpose

    the width of the row will be automatically calculated by len(content). 
    e.g. a row with four columns will make a 4-column layout. 
    It is also adaptive in small screens and mobile devices. 
    
    Args:
        content: a list of Column objects
    """
    def __init__(self, content=None, id=None):
        super().__init__('Row', content=content, id=id)

class Column(Element):
    """Column in the Row for multi-column layout
    
    Args:
        content: a list of page elements
        size: the "weight" of the column width. for example, 
            2 columns with both size=1 will have the same width;
            but a column with size=2 and one with size=1 will make 
            a 2:1 layout.
    """
    def __init__(self, content=None, size=1, id=None):
        super().__init__('Column', size=size, content=content, id=id)

class Statistic(Element):
    """A piece of text for showing a statistic number, may include a little trend arrow (up or down)
    
    Args:
        title: the title of the statistic number
        value: the number itself
        show_trend: if set True, a upper arrow will appear for positive numbers, and a down for negative numbers
        inline: if set True, the title and the value will be in the same line and the font size will be smaller
    """
    def __init__(self, title='', value=0, show_trend=False, inline=False, id=None):
        super().__init__('Statistic', title=title, value=value, show_trend=show_trend, inline=inline, id=id)
