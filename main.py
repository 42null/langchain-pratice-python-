import os
import json
import re

from langchain_community.llms import Ollama
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda


# Access to secrets
json_file_path = r".secrets/sqlAccess.json"
with open(json_file_path, "r") as f:
    sqlSecrets = json.load(f)

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

def print_debugging_variables():
    fields = [
        ("llm", llm_model_name),
        ("server path", sql_database_path),
        ("database", database_name),
        ("sql username", sql_username),
        ("sql password", sql_password),
    ]

    print("\nVariables for debugging")
    spacing_width = 20  # TODO: Make based on max field name length
    for field_name, field_value in fields:
        print(f"{field_name} {'.' * (spacing_width - len(field_name))} {field_value}")
    print("\n")

if __name__ == '__main__':
    # Setup Config
    llm_model_name    = "llama3"
    database_name     = "classicmodels"
    sql_database_path = sqlSecrets["server"]
    sql_username      = sqlSecrets["read_only_username"]
    sql_password      = sqlSecrets["read_only_password"]


    print_debugging_variables()

    # Setup
    llm = Ollama(model=llm_model_name)
    mysql_uri = f'mysql+mysqlconnector://{sql_username}:{sql_password}@{sql_database_path}/{database_name}'
    db = SQLDatabase.from_uri(mysql_uri)

    template = """Based on the table schema below, write a SQL query that would answer the user's question:
    {schema}

    Question: {question}
    SQL Query:"""
    prompt = ChatPromptTemplate.from_template(template)

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

    user_question = 'Which customer has spent the most money?'

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
    response_template = """Based on the table schema below, question, SQL query, and SQL response, write a natural language response:
    {schema}

    Question: {question}
    SQL Query: {query}
    SQL Response: {response}"""
    response_prompt = ChatPromptTemplate.from_template(response_template)

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

    final_response = full_chain.invoke({"question": user_question})
    print("Final Response: ", final_response)
