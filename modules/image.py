from helper import download

class Image:
    def __init__(self, type, doc_width) -> None:
        self.type = type
        self.doc_width = doc_width
        self.w_1_2 = doc_width / 2
        self.w_1_3 = doc_width / 3
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
        embedded_obj = img.get(f'{self.type}ObjectProperties').get('embeddedObject')
        self.id = img.get('objectId')
        name = f"{self.type}-{self.id}"
        img_name = download(embedded_obj.get("imageProperties").get("contentUri"), name)

        self.src= f"./assets/{file_slug}/{img_name}"
        
        # position
        if self.type == "positioned":
            left_offset = embedded_obj.get('positioning').get('leftOffset')
            width = img.get('size').get('width')
            self.pos = self.get_img_pos(left_offset, width)

        self.slug = file_slug
        # download img?


    def html_format(self, is_target: bool = True) -> str:
        target = ''
        if is_target:
            target = "target = 'blank'"
        return f"<img src='{self.src}' alt='{self.slug}' class='float-{self.pos}' {target}>"
        