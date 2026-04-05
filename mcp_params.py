playwright_params = {"command": "npx","args": [ "@playwright/mcp@latest"], "client_timeout": 30}
web_crawling_mcp_params = [playwright_params]
knowledge_graph_db_params = {"command": "npx","args": ["-y", "mcp-memory-libsql"],"env": {"LIBSQL_URL": "file:./memory/waiblingen.db"}} # npx is the node.js tool that runs npm packages without installing them globally
kb_db_params = [knowledge_graph_db_params]
