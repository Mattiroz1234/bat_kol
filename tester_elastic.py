from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch

# 1. טוענים מודל ליצירת embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. חיבור לאלסטיק
es = Elasticsearch("http://localhost:9200")  # שנה אם אתה רץ בדוקר או עם סיסמא

index_name = "people"

# 3. מיפוי לאינדקס (שדה טקסט ושדה dense_vector)
if not es.indices.exists(index=index_name):
    es.indices.create(
        index=index_name,
        mappings={
            "properties": {
                "offer": {"type": "text"},
                "search": {"type": "text"},
                "offer_vector": {"type": "dense_vector", "dims": 384},
                "search_vector": {"type": "dense_vector", "dims": 384},
            }
        }
    )

# 4. מוסיפים מסמכים לדוגמה
docs = [
    {"offer": "אני מתכנת פייתון", "search": "מחפש דאטה אנליסט"},
    {"offer": "אני דאטה אנליסט", "search": "מחפש מתכנת פייתון"},
    {"offer": "אני מעצב UX", "search": "מחפש שותף לפיתוח אתר"},
]

for i, doc in enumerate(docs):
    es.index(
        index=index_name,
        id=i + 1,
        document={
            **doc,
            "offer_vector": model.encode(doc["offer"]).tolist(),
            "search_vector": model.encode(doc["search"]).tolist(),
        },
    )

es.indices.refresh(index=index_name)

# 5. משפט שאתה רוצה לבדוק (מה אתה מחפש)
query_text = "מחפש מומחה נתונים"
query_vector = model.encode(query_text).tolist()

# 6. חיפוש kNN על שדה offer_vector (כי זה מה שאנשים מציעים)
resp = es.search(
    index=index_name,
    knn={
        "field": "offer_vector",
        "query_vector": query_vector,
        "k": 3,
        "num_candidates": 10
    }
)

print("תוצאות חיפוש ל:", query_text)
for hit in resp["hits"]["hits"]:
    print(f"{hit['_source']['offer']} (ציון: {hit['_score']:.3f})")