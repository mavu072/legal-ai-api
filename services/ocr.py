from fastapi import UploadFile
from PIL import Image
from pdf2image import convert_from_bytes

import os
import io
import pytesseract
import threading


def ocr_image_to_text(images, filename: str):
    thread = threading.Thread(target=read_images_to_text, args=(images, filename,), name=f"Reading {filename}")

    print(f">>> Starting thread: {thread.getName()}")
    thread.start()


async def convert_pdf_to_image(file: UploadFile):
    if not file:
        raise Exception(f"{str(file)} is not a valid file.")

    contents = await file.read()

    if file.content_type == "application/pdf":
        images = convert_from_bytes(contents)
    else:
        images = [Image.open(io.BytesIO(contents))]

    return images


def read_images_to_text(images, filename: str):
    if not images:
        raise Exception(f"{str(images)} is not a valid input.")

    pages = []

    for image in images:
        page = pytesseract.image_to_string(image)
        pages.append(page)
        write_to_file(filename, page)

    print(f">>> Completed reading file: {filename}, pages: {len(pages)} ")
    return pages


def write_to_file(filename: str, content: str):
    mkdir_if_not_exists()

    fpath = f"{dir}/{filename}.txt"

    if (os.path.exists(fpath)):
        os.remove(fpath)

    file = open(fpath, "a")
    file.write(content)
    file.close()


def read_out_file(filename):
    mkdir_if_not_exists()

    fpath = f"{dir}/{filename}.txt"

    if (os.path.exists(fpath)):
        file = open(fpath)
        content = file.read()
    else:
        raise Exception(f"{filename} file does not exist")
        
    return content


def mkdir_if_not_exists():
    global dir
    dir = "__local__"

    if (os.path.exists(dir) == False):
        os.mkdir(dir)
