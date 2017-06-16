import sys
import os
import tempfile
from string import Template
from pathlib import Path
import zipfile
import webbrowser
from tkinter import Tk
from tkinter import messagebox
import re

import templates
from excepts import ImagesNotFound


# todo: take list of explicit image paths, which are passed in from listdir or the unzip
def render_from_template(paths,
                         doc_template, page_template, img_types,
                         outfile=os.path.join(tempfile.gettempdir(), 'html-mangareader', 'render.html')):
    if not paths:
        raise ImagesNotFound
    imagepaths = [Path(p).as_uri() for p in paths]
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    with open(outfile, 'w', encoding='utf-8', newline='\r\n') as renderfd:
        html_template = Template(doc_template)
        img_template = Template(page_template)
        img_list = [img_template.substitute(img=imagepaths[i], id=i, previd=(i - 1), nextid=(i + 1))
                    for i in range(0, len(imagepaths))]
        doc_string = html_template.substitute(body=''.join(img_list))
        renderfd.write(doc_string)
    print("view saved to " + outfile)
    return outfile

def scan_directory(path, img_types):
    files = filter(lambda f: f.is_file(), Path(path).iterdir())
    files = filter(lambda f: os.path.isfile(os.path.join(path, f)), os.listdir(path))
    imagefiles = filter(lambda f: f.split('.')[-1].lower() in img_types, files)
    if not imagefiles:
        raise ImagesNotFound('No image files were found in directory: {}'.format(path))
    return [os.path.join(path, p) for p in sorted(imagefiles, key=filename_comparator)]

def extract_zip(path, img_types, outpath=os.path.join(tempfile.gettempdir(), 'html-mangareader')):
    with zipfile.ZipFile(path, mode='r') as zip_file:
        imagefiles = list(filter(lambda f: f.split('.')[-1].lower() in img_types, zip_file.namelist()))
        if not imagefiles:
            raise ImagesNotFound('No image files were found in archive: {}'.format(path))
        zip_file.extractall(outpath, imagefiles)
        return [os.path.join(outpath, image) for image in sorted(imagefiles, key=filename_comparator)]


def extract_render(path, doc_template, page_template, img_types, outpath):
    start = 0
    try:
        if os.path.isfile(path):
            if path.split('.')[-1].lower() in img_types:
                imgpath = scan_directory(os.path.dirname(path), img_types)
                start = filter(lambda p: os.path.basename(path))
            else:
                try:
                    imgpath = extract_zip(path, img_types)
                except zipfile.BadZipFile:
                    print('{} does not appear to be a valid zip/cbz file.'.format(path))
                    return
        else:
            imgpath = scan_directory(path, img_types)
        renderfile = render_from_template(imgpath, doc_template, page_template, img_types)
        webbrowser.open(renderfile)
    except ImagesNotFound as e:
        print(e)
        return
    return


def filename_comparator(filename):
    """Natural sort comparison key function. Thanks to <https://stackoverflow.com/a/16090640> for this bit of genius"""
    return [int(s) if s.isdigit() else s.lower()
            for s in re.split(r'(\d+)', filename)]


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        Tk().withdraw()
        messagebox.showinfo('HTML MangaReader - simply the fastest comic book reader',
                            'Start reading your favorite comics by doing one of the following:\n'
                            '- Drag an image folder or file onto the MangaReader icon, or\n'
                            '- Drag a ZIP or CBZ archive onto the MangaReader icon')
        exit(0)
    path = '.' if len(sys.argv) <= 1 else sys.argv[1]
    # render_from_template(path, templates.DOC_TEMPLATE, templates.IMG_TEMPLATE, templates.DEFAULT_IMAGETYPES, os.path.join(path, 'render.html'))
    # render_from_template(path, templates.DOC_TEMPLATE, templates.IMG_TEMPLATE, templates.DEFAULT_IMAGETYPES)
    # outpath = extract_zip('testar.zip', templates.DEFAULT_IMAGETYPES)
    # print(outpath)
    extract_render(path, templates.DOC_TEMPLATE, templates.IMG_TEMPLATE, templates.DEFAULT_IMAGETYPES, None)
