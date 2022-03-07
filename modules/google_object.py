from .template import Template
from modules.image import Image
from .helper import html_font_class, convert_title_to_slug, html_change_wrapper_tag, sanitize_html_content, extract_content_from_tag

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
            
            if text_run and text_run['content'] != '\n' and text_run['content'] != '':
                # print(text_run)
                sanitized = sanitize_html_content(text_run.get("content"))
                content = self.style_content(text_run.get("textStyle"), sanitized)
                main_content += content
            else:
                continue
        if main_content != '':
            self.html_content = f"<{self.tag} class='{html_font_class(self.main_font)} gs_reveal'>{main_content}</{self.tag}>"
        else: 
            self.html_content = None


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
        if self.html_content == None:
            self.html_content = ''
        self.html_content = self.html_content.replace(f"</{self.tag}>", "") + formatted_img + f"</{self.tag}>"
        if self.img_type == 'inline' and self.tag != 'div':            
            self.html_content = html_change_wrapper_tag(self.tag, "div", self.html_content)
            # self.html_content.replace(f"<{self.tag}", "<div")
            # self.html_content = self.html_content.replace(f"</{self.tag}>", "</div>")


        
            

class GoogleDoc:
    def __init__(self, document: dict, host: str) -> None:
        if document == {} or document == None:
            raise TypeError

        self.title = document.get('title') or ''
        self.content = document.get('body').get('content') or {}
        self.inline_obj = document.get('inlineObjects') or {}
        self.position_obj = document.get('positionedObjects') or {}
        self.doc_size = document.get('documentStyle').get('pageSize') or {}

        self.slug = convert_title_to_slug(self.title)
        # List of GoogleContentObject
        
        self.data_obj = {"title": "", "dek": "", "by_lines": [], "main_content":"", "main_img": ""}
        # self.data_obj = ''
        self.extracted_data = []
        self.template = ''
        self.formatted_content = ''
        self.host = host
    
    def get_obj_type(self, obj: dict):
        if "sectionBreak" in obj:
            # Remove section break from the list
            return None
        else:
            # Extract data from object
            paragraph: dict = obj.get("paragraph")
            elements: list = paragraph.get("elements")
            
            # Inline flags
            inline_exist = False
            inline_ref = {}
            
            # Positioned flag
            position_exist = "positionedObjectIds" in paragraph

            # Check if inlineObjectElement in p
            # No fancy search algorithm!!! => List size is too small for that
            for p in elements:
                if "inlineObjectElement" in p:
                    inline_exist = True
                    inline_ref = p
                    break
                    
            
            if inline_exist:
                id = inline_ref.get("inlineObjectElement").get("inlineObjectId")
                img_obj = self.inline_obj.get(id)
                return GoogleContentWithImage(obj, self.slug, img_obj, 'inline', 'Need to filled in', self.doc_size)
            elif position_exist:
                # Each paragraph should only be attached with 1 image only, hence the 0th index of the list 
                id = paragraph.get("positionedObjectIds")[0]
                img_obj = self.position_obj.get(id)

                return GoogleContentWithImage(obj, self.slug, img_obj, 'positioned', 'Need to filled in', self.doc_size)

            else:
                return GoogleContentObject(obj, self.slug, 'Need to filled in')

    def extract(self) -> None:
        data = []
        for section in self.content:
            temp = self.get_obj_type(section)

            if temp:
                temp.build_content()
                if temp.html_content != None:
                    data.append(temp)

        self.extracted_data = data
        if len(data) < 7:
            raise IndexError("Data is too short to be extracted")
        
        self.data_obj['main_img'] = data[0].html_content
        self.data_obj['title'] = html_change_wrapper_tag("p","h1",data[1].html_content) 
        self.data_obj['dek'] = html_change_wrapper_tag("p","h2",data[2].html_content) 
        self.data_obj['by_lines'] = [ html_change_wrapper_tag("p","h4",x.html_content) for x in data[3:5]]
        self.data_obj['main_content'] = data[5:]

    
    def load_template(self, path: str, template: Template = None) -> None:
        if template != None:
            self.template = template
        elif path != None or path != "": 
            self.template = Template(path)
                

    def format_with_template(self) -> None:
        dek = extract_content_from_tag(self.data_obj['dek'], 'span')
        
        self.template.replace_content('<---TITLE--->', self.data_obj['title'])

        self.template.replace_content('<---DEK--->', dek)

        inline_img_src = extract_content_from_tag( self.data_obj['main_img'], 'img')
        self.template.replace_content('<---OGIMG--->', f"{self.host}/assets/{self.slug}/{inline_img_src[2:]}")
        
        print(self.data_obj["by_lines"])
        for i in range(2):
            self.template.replace_content(f'<---BY_LINE_{i + 1}--->', self.data_obj["by_lines"][i])

        main_contents = "\n".join(x.html_content for x in self.data_obj['main_content'])

        self.template.replace_content('<---CONTENT--->', main_contents)

        self.template.replace_content('<---INLINE_IMG--->', f"./assets/{self.slug}/{inline_img_src}")


    def write_to_file(self):
        self.template.write_to_file(self.slug)

