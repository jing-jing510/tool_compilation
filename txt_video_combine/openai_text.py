# auth ： xiaokou
# date ： 2023/6/28 15:14
import time

import openai

#接入openai接口
openai.api_key = "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"
with open('prompt/prompt.txt', 'r',encoding="utf-8") as file:
    prompt_content = file.read()
    file.close()
with open('prompt/fenjing.txt', 'r',encoding="utf-8") as file:
    fenjing_content = file.read()
    file.close()
# print(sys_content)
#设置要问的问题
# text = "你好"
# text2 = "在一个阴暗而悲伤的房间里，我们看到一位年轻女孩蜷缩在角落里，她的脸庞苍白无力，眼神无比疲惫。阳光透过陈旧的窗帘洒在她瘦弱的身躯上，勾勒出她无助的轮廓。她的双手紧紧攥着一张纸，似乎是她最后的寄托和倚靠。房间内弥漫着浓重的沉默和绝望，仿佛时间也停滞在这一刻，只有她孤独的呼吸声陪伴着她。我们心生同情，不禁想知道她的故事，以及她所经历的苦难。"
# text3 = "看着眼前奄奄一息的女孩"
#批量处理 改文的分镜
def ai_fenjing_array():
    lines = []
    #将input中的文案.txt
    #按照每一行切分到可修改的数组当中
    with open("input/改文.txt", 'r', encoding='utf-8') as file:
        for line in file:
            lines.append(line.strip())
    # print(lines)
    return lines
def request_with_retry(messages, max_tokens=1000, max_requests=90, cooldown_seconds=60):
    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=max_tokens,
                n=1,
                stop=None
            )
            return response['choices'][0]['message']['content'].strip()
        except openai.error.RateLimitError:
            print("超过速率限制。正在等待冷却时间...")
            time.sleep(cooldown_seconds)
        except Exception as e:
            print(f"发生错误：{str(e)}")
            time.sleep(10)


def translate_text(text):
    messages = [
        {"role": "system", "content": "你是一个有帮助的助手。"},
        {"role": "user", "content": f"将以下中文文本翻译为英文：{text}"},
    ]
    return request_with_retry(messages)
def ai_prompt(text):
    messages = [
        {"role": "system", "content": prompt_content},
        {"role": "user", "content": text},
    ]
    return request_with_retry(messages)
def ai_fenjing(text):
    messages = [
        {"role": "system", "content": fenjing_content},
        {"role": "user", "content": text},
    ]
    return request_with_retry(messages)
# 批量处理ai_prompt
def ai_prompt_batch(fenjing):
    prompt = []
    # 将ai_fenjing(text)将参数使用
    for line in fenjing:
        # print(ai_prompt(line))
        prompt.append(ai_prompt(line))
    # print(prompt)
    return prompt
# 批量处理ai_fenjing
def ai_fenjing_batch(lines):
    fenjing = []
    # 循环lines中的每一行,将其放到ai_fenjing(text)当参数使用
    for line in lines:
        # print(ai_fenjing(line))
        fenjing.append(ai_fenjing(line))
    # print(fenjing)
    return fenjing

if __name__ == '__main__':
    # print(ai_prompt(text2))
    # print(ai_fenjing(text3))
    ai_fenjing_batch()
    # pass