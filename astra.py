import os
import requests
from dotenv import load_dotenv
from langchain_astradb.vectorstores import AstraDBVectorStore
from langchain_openai.embeddings import OpenAIEmbeddings

load_dotenv()

# Cargar variables de entorno
endpoint = os.getenv('ASTRA_DB_API_ENDPOINT')
token = os.getenv('ASTRA_DB_APPLICATION_TOKEN')
collection = "web2"
namespace = "default_keyspace"

# Crear la instancia de embeddings
embeddings = OpenAIEmbeddings()

# Crear la instancia de AstraDBVectorStore
vectorstore = AstraDBVectorStore(
    collection_name=collection,
    embedding=embeddings,
    token=token,
    api_endpoint=endpoint,
    namespace=namespace  # Asegúrate de especificar el namespace
    #metric="cosine"       # Opcional, especifica la métrica si es necesario
)

# Obtener el contenido de la URL
url = "https://es.wikipedia.org/wiki/Copa_Am%C3%A9rica"  # Reemplaza con tu URL
response = requests.get(url)
content = response.text

# Función para dividir el texto en fragmentos
def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    chunks = []
    start = 0
    text_length = len(text)
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - chunk_overlap
    return chunks

# Dividir el contenido en fragmentos
chunks = chunk_text(content, chunk_size=1000, chunk_overlap=200)

# Añadir los fragmentos al vector store
vectorstore.add_texts(chunks)

# Realizar una búsqueda de similitud
results = vectorstore.similarity_search("revisar", k=1)
print(results)