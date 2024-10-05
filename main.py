from fastapi import FastAPI, UploadFile

from services.ocr import convert_pdf_to_image, ocr_image_to_text
from services.ner import find_named_entities
from services.vectordb import init_chromadb, query_chromadb
from utils.ner_validator import censor_named_entities


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello world"}


@app.post("/ocr/files/upload/")
async def upload_file(file: UploadFile):
    images = await convert_pdf_to_image(file)

    fname, fsize = file.filename, file.size
    pages = len(images)

    ocr_image_to_text(images, fname)

    return {"uploaded": True, "filename": fname, "size": fsize, "pages": pages}


@app.post("/ner/entity/recognition/")
def identify_named_entities(text: str):
    entity_list = find_named_entities(text)
    total = len(entity_list)

    return {"total": total, "entities": entity_list}


@app.get("/vectordb/init")
def initialize_vector_database():
    init_chromadb();

    return {"message": "Vector DB initialized"}


@app.post("/vectordb/query")
def query_vector_database(query: str):
    results = query_chromadb(query)
    total = len(results)

    return {"total": total, "result": results}

@app.post("/llm/query")
def query_llm_assistant(query: str):
    entity_list = find_named_entities(query)
    censored_query = censor_named_entities(entity_list, query)

    return {"result": censored_query}