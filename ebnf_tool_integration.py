from sglang.utils import (
    execute_shell_command,
    wait_for_server,
    terminate_process,
    print_highlight,
)

# 定义一个示例函数，需要参数
def perform_search(query):
    print(f"Performing search with query: {query}")
    # 在这里添加搜索功能逻辑
    # 例如：
    # result = call_search_api(query)
    # print(f"Search result: {result}")

# 启动服务器
server_process = execute_shell_command(
    "python -m sglang.launch_server --model-path Qwen/Qwen2.5-1.5B-Instruct --port 30000 --host 0.0.0.0 --grammar-backend xgrammar"
)
wait_for_server("http://localhost:30000")

import openai

client = openai.Client(base_url="http://127.0.0.1:30000/v1", api_key="None")

# 定义 EBNF 语法规则
ebnf_grammar = r"""
        root ::= "search" query | "Hi" | "weather"
        query ::= " about AI" | " for Python tutorials" | " on latest technology trends"
        """

# 向模型发送请求
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

# 获取生成的答案
generated_answer = response.choices[0].message.content.strip()
print(f"Generated answer: {generated_answer}")

# 根据生成的答案调用函数
if generated_answer.startswith("search"):
    # 提取查询参数
    query = generated_answer.replace("search", "").strip()
    perform_search(query)
elif generated_answer == "Hi":
    print("The bot says: Hi!")
elif generated_answer == "weather":
    print("The bot says: Checking the weather...")

# 终止服务器
terminate_process(server_process)
