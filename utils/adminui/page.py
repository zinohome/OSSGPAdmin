from inspect import signature 

class Page:
    def __init__(self, url, name, builder, auth_needed=None, description=''):
        self.name = name
        self.url = url
        self.auth_needed = auth_needed
        self.builder = builder
    
    def as_list(self, param=''):
        def call_builder():
            if len(signature(self.builder).parameters) > 0:
                return self.builder(param)
            else:
                return self.builder()
        return {
            'name': self.name,
            'content': call_builder()
        }