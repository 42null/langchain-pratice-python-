This is just a minor starter project where I had been experimenting with tutorials on LangChain. Credits are involved at the top of each respective file. As of writing it just uses a local Ollama3 instance to interact with a SQL database. 

Not shown here but also a great resource I encountered: Langchain-Full-Course-main: https://github.com/Coding-Crashkurse/Langchain-Full-Course / https://www.youtube.com/watch?v=a89vqgK-Qcs

If trying this code, replace secret keys with strings directly or create ".secrets/sqlAccess.json" with the structre
```
{
  "read_only_username" : "<username>",
  "read_only_password": "<password>"
  "server": "<server address: Eg. example.net or #.#.#.#>"
}
```
