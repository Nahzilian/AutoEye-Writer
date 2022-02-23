from modules.image import Image
from .helper import html_font_class, convert_title_to_slug

class GoogleContentObject:
    """
    Type:
    inline object
    paragraph
        - With bold/italic
        - With image
        - With 
    """
    def __init__(self, obj: dict, slug: str, main_font: str) -> None:
        self.obj = obj.get('paragraph')
        self.style = obj.get('paragraphStyle')
        self.html_content = ''
        self.slug = slug or ''
        self.main_font = main_font
        self.tag = 'p'

    def bold_text_html(self,content: str) -> str:
        """Apply bold"""
        return f"<b>{content}</b>"

    def italic_text_html(self, content: str) -> str:
        """Apply Italic"""
        return f"<em>{content}</em>"

    def style_content(self, obj: dict, content: str) -> str:
        """
        Check style object to add certain text decor
        Also add specific font family if not match with the original
        """
        formatted = ''
        font = obj.get("weightedFontFamily")
        if obj != {}:
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
        """
        Convert data to HTML format content
        """
        elements = self.obj.get('elements')
        main_content = ''

        for e in elements:
            text_run = e.get('textRun')
            if text_run:
                content = self.style_content(text_run.get("textStyle"), text_run.get("content"))
                main_content += content
        
        self.html_content = f"<{self.tag} class='{html_font_class(self.main_font)}'>{main_content}</{self.tag}>"


class GoogleContentWithImage(GoogleContentObject):
    """
    ie: img_data = ""kix.od0i30v76o2p": {...}"
    """
    def __init__(self, obj: dict, slug: str, img_data: dict, img_type: str, main_font: str, page_size) -> None:
        super().__init__(obj, slug, main_font)
        if not img_data:
            raise TypeError
        self.img_data = img_data
        
        # self.size = img_data.get(f"{img_type}ObjectProperties").get("embeddedObject").get("size")

        self.img_type = img_type
        # File slug should be path to product folder
        self.image = Image(img_type=img_type, doc_width=page_size)
        self.image.get_image_atr(img_data, self.slug)

        

    def build_content(self):
        # This will become overall format
        super().build_content()
        formatted_img = self.image.html_format()
        self.html_content = self.html_content.replace(f"</{self.tag}>", "") + formatted_img + f"</{self.tag}>"    
        
            

class GoogleDoc:
    def __init__(self, document: dict) -> None:
        if document == {} or document == None:
            raise TypeError

        self.title = document.get('title') or ''
        self.content = document.get('body').get('content') or {}
        self.inline_obj = document.get('inlineObjects') or {}
        self.position_obj = document.get('positionedObjects') or {}
        self.doc_size = document.get('documentStyle').get('pageSize') or {}

        self.slug = convert_title_to_slug(self.title)
        # List of GoogleContentObject
        
        # self.data_list = {"title": "", "dek": "", "by-lines": "", "main_content":"", "main_img": ""}
        self.data_list = ''
        self.extracted_data = []
    
    def get_obj_type(self, obj: dict):
        if "positionedObjectIds" in obj:
            id = obj.get("positionedObjectIds")
            img_obj = self.position_obj.get(id)
            return GoogleContentWithImage(obj, self.slug, img_obj, 'positioned', self.doc_size)
        elif "sectionBreak" in obj:
            return None
        else:
            ps = obj.get("paragraph").get("elements")
            inline_exist = False
            inline_ref = {}

            # This might not ref to inline_ref
            for p in ps:
                if "inlineObjectElement" in p:
                    inline_exist = True
                    inline_ref = p
                    break
            
            if inline_exist:
                id = inline_ref.get("inlineObjectElement").get("inlineObjectId")
                img_obj = self.inline_obj.get(id)
                return GoogleContentWithImage(obj, self.slug, img_obj, 'inline', 'Need to filled in', self.doc_size)
        
            else:
                return GoogleContentObject(obj, self.slug, 'Need to filled in')

    def extract(self) -> None:
        data = []
        for section in self.content:
            temp = self.get_obj_type(section)
            if temp != None:
                data.append(temp)
        self.extracted_data = data
    
    
    def write_to_html(self, path: str = ''):
        for item in self.extracted_data:
            item.build_content()
            print(item.html_content)
        # f = open("assets/output.html", "w")
        # f.write("FWERWERWERWER")
        # f.close()

