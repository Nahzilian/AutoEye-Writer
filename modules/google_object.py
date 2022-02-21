from modules.image import Image
from helper import html_font_class

class GoogleContentObject:
    """
    Type:
    inline object
    paragraph
        - With bold/italic
        - With image
        - With 
    """
    def __init__(self, obj: dict, slug: str, id: str, main_font: str) -> None:
        self.id = id
        self.obj = obj.get('paragraph')
        self.style = obj.get('paragraphStyle')
        self.html_content = ''
        self.slug = slug or ''
        self.main_font = main_font
        self.tag = 'p'

    def bold_text_html(self,content: str) -> str:
        return f"<b>{content}</b>"

    def italic_text_html(self, content: str) -> str:
        return f"<em>{content}</em>"

    def style(self, obj: dict, content: str) -> str:
        """
        Check style object to add certain text decor
        Also add specific font family if not match with the original
        """
        formatted = ''
        font = obj.get("weightedFontFamily")
        if "weightedFontFamily" and "fontFamily" in font:
            font_fam = font.get("fontFamily")
            if not font_fam == self.main_font:
                font_class = html_font_class(font_fam)
                formatted += f"<span class='{font_class}'>{content}</span>"

        if "bold" in obj and obj.get("bold") == True:
            formatted = self.bold_text_html(formatted)
        
        if "italic" in obj and obj.get("italic") == True:
            formatted = self.italic_text_html(formatted)

        return formatted
        

    def build_content(self):
        elements = self.obj.get('elements')
        main_content = ''
        for e in elements:
            text_run = e.get('textRun')
            if text_run:
                content = self.style(text_run.get("content"), text_run.get("textStyle"))
                main_content += content
        
        self.html_content = f"<{self.tag} class='{html_font_class(self.main_font)}'>{main_content}</{self.tag}>"


class GoogleContentWithImage(GoogleContentObject):
    def __init__(self, obj: dict, slug: str, id: str, img_data: dict) -> None:
        super().__init__(obj, slug, id)
        if not img_data:
            raise TypeError
        """
        ie: img_data = ""kix.od0i30v76o2p": {...}"
        """
        self.img_data = img_data

        # File slug should be path to product folder
        self.image = Image(type='inline')
        self.image.get_image_atr(img_data, self.slug)

        

    def get_html_formmat(self):
        # This will become overall format
        formatted_img = self.image.html_format()
        if self.html_content == '':
            return formatted_img    
        else:
            return self.html_content.replace(f"</{self.tag}>", "") + formatted_img + f"</{self.tag}>"
        
            

class GoogleDoc:
    def __init__(self, document: dict) -> None:
        if document == {} or document == None:
            raise TypeError

        self.title = document.get('title') or ''
        self.content = document.get('body').get('content') or {}
        self.inline_obj = document.get('inlineObjects') or {}
        self.position_obj = document.get('positionedObjects') or {}
        self.doc_size = document.get('documentStyle').get('pageSize') or {}

        # List of GoogleContentObject
        self.data_list = []
    
    def get_obj_type():
        pass

    def extract(self) -> None:
        pass


    

