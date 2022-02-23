import requests

def convert_title_to_slug(title: str) -> str:
    lower_cased = title.lower().replace(' ','-')
    no_sp_char = ''.join(char for char in lower_cased if char.isalnum() or char == '-')
    return no_sp_char


def download(url, name) -> str:
    r = requests.get(url, allow_redirects=True)
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('Content-Type')
    if not content_type:
        raise TypeError
    file_name = name + content_type.replace('image/', '.')
    open(file_name, 'wb').write(r.content)
    return file_name

def html_font_class(font_name: str):
    font = "-".join(font_name.lower().strip().split(' '))
    return f"text-font-{font}"
