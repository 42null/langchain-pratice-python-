This is just a minor starter project where I had been experimenting with tutorials on LangChain. Credits are involved at the top of each respective file.

Current abilities of this repository.
- Using a local Ollama3 instance to interact with a SQL database (remoteSqlQueryUsingLangchain.py)
- Picking options and generating a vectorstore from documents (vectorstoreCreatorTool.py)


If trying this code, replace secret keys with strings directly or create ".secrets/sqlAccess.json" with the structure.
```
{
  "read_only_username" : "<username>",
  "read_only_password": "<password>"
  "server": "<server address: Eg. example.net or #.#.#.#>"
}
```
