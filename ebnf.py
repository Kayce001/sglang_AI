from sglang.utils import (
    execute_shell_command,
    wait_for_server,
    terminate_process,
    print_highlight,
)

server_process = execute_shell_command(
    "python -m sglang.launch_server --model-path Qwen/Qwen2.5-1.5B-Instruct --port 30000 --host 0.0.0.0 --grammar-backend xgrammar"
)

wait_for_server("http://localhost:30000")

import openai

client = openai.Client(base_url="http://127.0.0.1:30000/v1", api_key="None")

# EBNF example
ebnf_grammar = r"""
        root ::= "search" | "Hi" | "weather"
        """
response = client.chat.completions.create(
    model="Qwen/Qwen2.5-1.5B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful EBNF test bot."},
        {"role": "user", "content": "i want some result from internet."},
    ],
    temperature=0,
    max_tokens=32,
    extra_body={"ebnf": ebnf_grammar},
)
print(response.choices[0].message.content)




#print_highlight(response.choices[0].message.content)
terminate_process(server_process)

