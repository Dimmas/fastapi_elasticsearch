from fastapi import FastAPI
from elasticsearch import Elasticsearch

app = FastAPI()
es = Elasticsearch(cloud_id='CLOUD_ID', basic_auth=("elastic", 'ELASTIC_PASSWORD'))


@app.post("/faq")
async def add_question(question: str, answer: str):
    # Добавление вопроса и ответа в базу данных ElasticSearch
    try:
        es.index(index="faq", body={"question": question, "answer": answer})
        return {"status": "success"}
    except:
        return {"status": "error"}


@app.get("/faq")
async def search_question(query: str, page: int = 1, size: int = 10):
    # Полнотекстовый поиск вопросов в базе данных ElasticSearch с пагинацией результатов
    search_body = {
        "query": {
            "match": {
                "question": query
            }
        },
        "from": (page - 1) * size,
        "size": size
    }
    result = es.search(index="faq", body=search_body)
    return result["hits"]["hits"]


@app.put("/faq/{question_id}")
async def update_question(question_id: str, question: str, answer: str):
    # Обновление вопроса и ответа в базе данных ElasticSearch
    try:
        es.update(index="faq", id=question_id, body={"doc": {"question": question, "answer": answer}})
        return {"status": "success"}
    except:
        return {"status": "error"}


@app.delete("/faq/{question_id}")
async def delete_question(question_id: str):
    # Удаление вопроса и ответа из базы данных ElasticSearch
    try:
        es.delete(index="faq", id=question_id)
        return {"status": "success"}
    except:
        return {"status": "error"}

