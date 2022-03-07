import requests
import os
from bs4 import BeautifulSoup

special_char = {
    "&": "&amp;",
    "'": "&apos;",
    "’": "&apos;",
    '"': "&quot;",
    ">":"&gt;",
    "<":"&lt;"
}

def convert_title_to_slug(title: str) -> str:
    lower_cased = title.lower().replace(' ','-')
    no_sp_char = ''.join(char for char in lower_cased if char.isalnum() or char == '-')
    return no_sp_char


def download(url, name, slug = '') -> str:
    r = requests.get(url, allow_redirects=True)
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('Content-Type')
    if not content_type:
        raise TypeError
    file_path = f'assets/prod/assets/{slug}'
    is_exist = os.path.exists(file_path)
    if not is_exist:
        print("File path not exist. Creating new")
        os.makedirs(file_path)

    file_name = file_path + f'/{name}.'+ content_type.replace('image/', '')
    open(file_name, 'wb').write(r.content)
    return file_name

def html_font_class(font_name: str):
    font = "-".join(font_name.lower().strip().split(' '))
    return f"text-font-{font}"

def sanitize_html_content(content: str):
    sanitized = content
    for key, value in special_char.items():
        sanitized = sanitized.replace(key, value)
    return sanitized


def html_change_wrapper_tag(target: str, new_tag: str, line: str):
    new_line = line.replace(f"<{target}", f"<{new_tag}")
    new_line = new_line.replace(f"</{target}>", f"</{new_tag}>")
    return new_line

def extract_content_from_tag(content: str, tag):
    soup = BeautifulSoup(content, 'html.parser')
    if tag == "img":
        imgs = soup.find_all(tag)
        return imgs[0]['src']
    else:
        tags = soup.find_all(tag)
        return tags[0].text.strip()