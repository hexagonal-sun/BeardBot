import re

class on_match(object):
    def __init__(self, expression, search=False, *flags):
        self.re = re.compile(expression, *flags)
        self.search = False


    def __call__(self, func):
        self.func = func
        return self


    def call_if_match(self, other_self, source_name, source_host, message):
        if self.search: 
            match = self.re.search(message)
        else:
            match = self.re.match(message)
        if match:
            self.func(other_self, source_name, source_host, message, *match.groups())


class on_channel_match(on_match):
    pass

class on_addressed_match(on_match):
    pass

class on_private_match(on_match):
    pass


def test_for_matches(self, match_type, source_name, source_host, message):
    for attribute in (getattr(self, attr_name) for attr_name in dir(self)):
        if isinstance(attribute, match_type):
            attribute.call_if_match(self, source_name, source_host, message)

