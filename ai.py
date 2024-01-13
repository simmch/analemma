import os
import sys
import bs4
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
import nest_asyncio
from langchain.document_loaders.mongodb import MongodbLoader
nest_asyncio.apply() 
from dotenv import load_dotenv
from typing import Dict, Optional 
from motor.motor_asyncio import AsyncIOMotorClient
import certifi

class CustomMongodbLoader(MongodbLoader):
    def __init__(self, connection_string: str, db_name: str, collection_name: str, *, filter_criteria: Optional[Dict] = None):
        # Call the original constructor
        super().__init__(connection_string, db_name, collection_name, filter_criteria=filter_criteria)

        # Add your SSL certificate handling
        self.client = AsyncIOMotorClient(connection_string, tlsCAFile=certifi.where())
        self.db = self.client.get_database(db_name)
        self.collection = self.db.get_collection(collection_name)



load_dotenv()

async def run_search(question):
    if os.environ["env"] == "production":
        use_database = "Lore"
    else:
        use_database = "LoreTest"

    loader = CustomMongodbLoader(
        connection_string=os.environ["MONGO_KEY"],
        db_name=use_database,
        collection_name="lore",
        )
    
    if loader:
        docs = await loader.aload()
        # print(len(docs))

        template = """The context given is from our Dungeons & Dragons campaign, which is set in a world called Tungra. All of the context is important to the story and development of the characters, the locations, the world, and the plot. You will answer like the Dungeon Master.
        If you don't know the answer, say that the answer has not been added to the campaign lore, don't try to make up an answer.
        Use three sentences maximum and keep the answer as concise as possible.
        Always say "thanks for asking!" at the end of the answer.

        {context}

        Question: {question}

        Helpful Answer:"""
        custom_rag_prompt = PromptTemplate.from_template(template)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=500)
        splits = text_splitter.split_documents(docs)
        vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

        # Retrieve and generate using the relevant snippets of the blog.
        retriever = vectorstore.as_retriever()
        # prompt = hub.pull("rlm/rag-prompt")
        llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0)


        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)


        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | custom_rag_prompt
            | llm
            | StrOutputParser()
        )
        message = rag_chain.invoke(question)

        return message
    else:
        return "There is nothing even remotely close to this in the campaign lore, dummy."