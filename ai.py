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
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema.document import Document
import nest_asyncio
from langchain.document_loaders.mongodb import MongodbLoader
nest_asyncio.apply() 
from dotenv import load_dotenv
from typing import Dict, Optional, Sequence
from motor.motor_asyncio import AsyncIOMotorClient
import certifi
import vectorsearch

class CustomMongodbLoader(MongodbLoader):
    # Adjust your __init__ method to accept additional parameters that might help in filtering
    def __init__(self, connection_string: str, db_name: str, collection_name: str, *, filter_criteria: Optional[Dict] = None, field_names: Optional[Sequence[str]] = None, additional_params: Dict = None):
        super().__init__(connection_string, db_name, collection_name, filter_criteria=filter_criteria)
        self.client = AsyncIOMotorClient(connection_string, tlsCAFile=certifi.where())
        self.db = self.client.get_database(db_name)
        self.collection = self.db.get_collection(collection_name)
        
        # Let's say you want to dynamically adjust your filter based on some external parameters
        # if additional_params:
        #     self.filter_criteria.update(additional_params)  # Make sure to handle None scenarios for filter_criteria and additional_params
        #     self.collection = self.db.get_collection(collection_name)



load_dotenv()

async def run_search(question):
    # if os.environ["env"] == "production":
    #     use_database = "Lore"
    # else:
    #     use_database = "Lore"

    # loader = CustomMongodbLoader(
    #     connection_string=os.environ["MONGO_KEY"],
    #     db_name=use_database,
    #     collection_name="lore",
    #     field_names=["original_title", "original_description"],
    #     )

    text = vectorsearch.answer_question(question)

    if text:
        print("Got Text from vector search!")
        def get_text_chunks_langchain(text):
            text_splitter = CharacterTextSplitter(chunk_size=3000, chunk_overlap=500)
            docs = [Document(page_content=x) for x in text_splitter.split_text(text)]
            return docs
        
        docs = get_text_chunks_langchain(text)
        if docs:
            print("Got Docs!")
            # docs = await loader.aload()
            # print(len(docs))

            template = """You are the Lore Archive for Dungeon and Dragons campaigns.
            If you don't know the answer, say that the answer has not been added to the campaign lore, don't try to make up an answer. Break up paragraphs with blank lines for readability. Make it clear when you are quoting from the campaign lore. Make the response discord formatted text with bolds, italics, and underlines, without ```yaml. 

            {context}

            Question: {question}

            Helpful Answer:"""
            custom_rag_prompt = PromptTemplate.from_template(template)

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=500)
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
    else:
        print("Error in vectorsearch.py function.")
        return False