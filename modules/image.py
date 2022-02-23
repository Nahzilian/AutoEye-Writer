from .helper import download

class Image:
    def __init__(self, img_type, doc_width) -> None:
        self.img_type = img_type
        self.doc_width = doc_width.get("width").get("magnitude")
        self.w_1_2 = self.doc_width / 2
        self.w_1_3 = self.doc_width / 3
        self.W_2_3 = self.w_1_3 * 2
        self.id = ''
        self.src = ''
        self.pos = ''
        self.slug = ''


    def get_img_pos(self, left_offset: dict, size: dict) -> str:
        """
        Determine if the image need to be float left, right or center
        """
        width = size.get('magnitude')
        start_pos = left_offset.get('magnitude')
        end_pos = width + start_pos

        # Handle left hand side
        if start_pos < self.w_1_3:
            if end_pos < self.w_1_2:
                return 'left'
            else:
                return 'center'
        else:
            if end_pos <= self.W_2_3:
                return'center'
        
        # Handle right hand side

        if start_pos >= self.w_1_2:
            return 'right'
        else:
            return 'center'

    def get_image_atr(self, img:dict, file_slug: str):
        """
        This should be able to differentiate between 2 types of image
        """
        obj_props: dict = img.get(f'{self.img_type}ObjectProperties')
        embedded_obj = obj_props.get('embeddedObject')
        self.id = img.get('objectId')
        name = f"{self.img_type}-{self.id}"
        img_name = download(embedded_obj.get("imageProperties").get("contentUri"), name)

        self.src= f"./assets/{file_slug}/{img_name}"
        
        # position
        if self.img_type == "positioned":
            left_offset = obj_props.get('positioning').get('leftOffset')
            width = embedded_obj.get('size').get('width')
            self.pos = self.get_img_pos(left_offset, width)
        else: 
            self.pos = 'center'

        self.slug = file_slug
        


    def html_format(self, is_target: bool = True) -> str:
        target = ''
        if is_target:
            target = "target='blank'"
        return f"<img src='{self.src}' alt='{self.slug}' class='float-{self.pos}' {target}>"
        