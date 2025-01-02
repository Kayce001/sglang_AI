from sglang import function, system, user, assistant, gen, set_default_backend, RuntimeEndpoint

# 初始化一个空的对话状态
conversation_history = []
answer_counter = 1  # 初始化答案计数器，用于动态生成 answer_i
first_turn = True  # 标记是否是第一次对话

@function
def multi_turn_question(s, question):
    global answer_counter,first_turn  # 使用全局变量保持答案计数
    
    if first_turn:
        s += system("You are a helpful assistant.")
        first_turn = False  # 标记第一次对话结束

    # 将历史对话加入到当前对话状态
    for msg in conversation_history:
        s += msg
    
    # 用户提问
    s += user(question)
    
    # 动态生成答案变量名称
    answer_name = f"answer_{answer_counter}"
    
    # 获取助手回答，并保存到动态生成的变量中
    s += assistant(gen(answer_name, max_tokens=256))
    
    # 保存本轮对话的用户提问和助手回答到历史中
    conversation_history.append(user(question))
    conversation_history.append(assistant(gen(answer_name, max_tokens=256)))  # 保存答案

    # 增加答案计数器
    answer_counter += 1
    
    return s

# 设置后端连接
set_default_backend(RuntimeEndpoint("http://localhost:30000"))

# 无限轮次对话示例
while True:
    # 获取用户输入的问题
    user_input = input("User: ")
    
    # 退出条件
    if user_input.lower() == "exit":
        print("Exiting the conversation...")
        break

    # 获取助手的回答
    state = multi_turn_question.run(user_input)
    
    # 打印出整个 state 对象，看看其包含了哪些变量
    print("State contents:", state)
    
    # 根据动态命名的方式打印助手的答案
    answer_key = f"answer_{answer_counter - 1}"  # 获取当前答案的键名
    print(f"Assistant: {state[answer_key]}")
