# -*- coding: utf-8 -*-
"""
Example module that demonstrates status string placeholders

Configuration parameters:
    format: Initial format to use
        (default 'Click me')
    format_clicked: Display format to use when we are clicked
        (default 'You pressed button {button}')

Format placeholders:
    {button} The button that was pressed
"""


class Py3status:
    format = 'Click me'
    format_clicked = 'You pressed button {button}'

    def __init__(self):
        self.button = None

    def click_info(self):
        if self.button:
            data = {'button': self.button}
            full_text = self.py3.safe_format(self.format_clicked, data)
        else:
            full_text = self.format

        return {
            'full_text': full_text,
            'cached_until': self.py3.CACHE_FOREVER
        }

    def on_click(self, event):
        """
        event will be a dict like
        {'y': 13, 'x': 1737, 'button': 1, 'name': 'example', 'instance': 'first'}
        """
        self.button = event['x']
        # Our modules update methods will get called automatically.
