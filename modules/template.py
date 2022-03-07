class Template:
    def __init__(self, path: str ) -> None:
        if path == '':        
            raise TypeError
        with open(path, 'r') as f:
            self.template = f.read()

    def replace_content(self, key: str, value: str) -> None:
        self.template = self.template.replace(key, value)


    def write_to_file(self, slug: str):
        if slug == '':
            raise TypeError("Slug is empty")
        path = f'assets/prod/{slug}.html'
        # print(self.data_obj)
        f = open(path, "w")
        f.write(self.template)
        f.close()
    
        


    