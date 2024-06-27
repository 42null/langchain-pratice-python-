"""
Credits:
This project was started out heavily using code form the below tutorials
- https://medium.com/@vchan444/get-started-with-llama-3-using-ollama-and-langchain-in-a-few-minutes-1e2b84c25f8b
- https://alejandro-ao.com/chat-with-mysql-using-python-and-langchain/
"""

import os
import json
import re

from helperFunctions import print_debugging_variables

from langchain_community.llms import Ollama
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda


# Access to secrets
secrets_json_file_path = r".secrets/sqlAccess.json"
with open(secrets_json_file_path, "r") as f:
    sqlSecrets = json.load(f)

# Get templates  # TODO: Access on demand instead of preloading all
with open(r"templates.json", "r") as f:
    templates = json.load(f)

def get_schema(db):
    schema = db.get_table_info()
    return schema

def run_query(db, query):
    return db.run(query)

def extract_sql_query(text):
    # pattern = r'```(.*?)```'
    pattern = r'```sql(.*?)```'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None

def get_and_sanitize_user_input(question):
    # TODO: Should I trim user input? Could be used to ask llm for formatting
    # TODO: Add more sanitization
    user_input = input(question)
    user_input = user_input.strip()
    return user_input



if __name__ == '__main__':
    # Setup Config
    llm_model_name    = "llama3"
    database_name     = "classicmodels"
    sql_database_path = sqlSecrets["server"]
    sql_username      = sqlSecrets["read_only_username"]
    sql_password      = sqlSecrets["read_only_password"]

    fields = [
            ("llm", llm_model_name),
            ("server path", sql_database_path),
            ("database", database_name),
            ("sql username", sql_username),
            ("sql password", sql_password),
        ]
    print_debugging_variables(fields)
    llm = None
    db = None


    # Setup
    llm = Ollama(model=llm_model_name)
    mysql_uri = f'mysql+mysqlconnector://{sql_username}:{sql_password}@{sql_database_path}/{database_name}'
    db = SQLDatabase.from_uri(mysql_uri)

    template = templates["database_info"][0]

    # template = """Based on the table schema below, write a SQL query that would answer the user's question:
    # {schema}
    #
    # Question: {question}
    # SQL Query:"""
    prompt = ChatPromptTemplate.from_template(template["prompt_template"])

    def add_schema(input_dict):
        input_dict['schema'] = get_schema(db)
        # print("GOT SCHEMA IS ...\n\n"+input_dict['schema']+"\n\n")
        return input_dict

    def extract_question(input_dict):
        return input_dict['question']

    sql_chain = (
            RunnableLambda(add_schema)
            | RunnablePassthrough.assign(question=extract_question)
            | prompt
            | llm.bind(stop=["\nSQLResult:"])
            | StrOutputParser()
    )

    user_question = get_and_sanitize_user_input(f"Please enter your question about the database \"{database_name}\": ")

    print("Invoking llm....")
    llmResponse = sql_chain.invoke({"question": user_question})
    print("LLM Response: ", llmResponse)

    # Extracting the SQL query from the LLM response
    query = extract_sql_query(llmResponse)
    print("Extracted SQL Query: ", query)

    # Running the SQL query and getting the response
    sql_response = run_query(db, query)
    print("SQL Response: ", sql_response)

    # Creating the full chain
    response_prompt = ChatPromptTemplate.from_template(template["response_template"])

    def add_response_context(input_dict):
        input_dict['query'] = query
        input_dict['response'] = sql_response
        return input_dict

    full_chain = (
            RunnableLambda(add_schema)
            | RunnableLambda(add_response_context)
            | response_prompt
            | llm
    )

    print("Invoking llm....")
    final_response = full_chain.invoke({"question": user_question})
    print("Final Response: ", final_response)
