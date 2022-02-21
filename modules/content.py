from helper import convert_title_to_slug

from image import ImageList
        

class Content:
    def __init__(self, title: str,dek:str, visuals:str, words:str, content:str, images: list) -> None:
        # image list format: [inline, position]
        # Need to verify if the linebreak count as positioned or inline

        self.title = title
        self.dek = dek
        self.visuals = visuals
        self.words = words
        self.content = content
        self.slug = convert_title_to_slug(title)
        self.images = ImageList(images)

    def format_article(self):
        pass




def content_parser(g_doc_data: dict):
    pass
    