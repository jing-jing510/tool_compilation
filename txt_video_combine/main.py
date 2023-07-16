import csv
import errno
import io
import os.path
from openpyxl import Workbook
from flask import Flask, request, jsonify, render_template, send_from_directory, url_for
import json
from openpyxl import load_workbook
from werkzeug.utils import secure_filename
import pandas as pd

from openai_text import ai_fenjing, ai_prompt, translate_text_en2cn, rewriteText, translate_text_cn2en
import os

from txt_video_combine.step2_txt_to_image import run_program_with_args, run_program

df = pd.DataFrame()
app = Flask(__name__,static_folder='image')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def home():
    return render_template('index.html')
# 上传原文件
@app.route('/handle_file', methods=['POST'])
def handle_file():
    data = request.get_json()
    file_contents = data['data']

    # 你可能需要在这里处理文件内容
    # 例如，如果文件是.docx格式，你需要使用一个库如python-docx来读取它
    # 但在这个示例中，我们假设文件是纯文本，并直接返回它
    return jsonify({'text': file_contents})


# set_key 将新的GPT_KEY写入config.json当中
@app.route('/set_key', methods=['POST'])
def set_key():
    data = request.get_json()
    gpt_key = data['gpt_key']

    config = {}

    if os.path.exists('config.json'):
        # 如果 config.json 文件存在，读取现有的配置
        with open('config.json', 'rb') as f:
            config = json.load(f)

    # 不论'OPENAI_API_KEY'是否存在，都更新或设置 GPT key
    config['OPENAI_API_KEY'] = gpt_key

    # 将新的配置写入 config.json 文件
    with open('config.json', 'w') as f:
        json.dump(config, f,indent=4)

    return '', 204


# 创建小说文件夹
@app.route('/create_folder', methods=['POST'])
def create_folder():
    data = request.get_json()
    folder_name = data['folderName']
    directory = 'novel/' + folder_name
    print(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
        return jsonify({"status": "success", "message": "Folder created successfully"})
    else:
        return jsonify({"status": "failed", "message": "Folder already exists"})




@app.route('/rewrite', methods=['POST'])
def rewrite():
    text = request.get_json().get('text')
    # print(text)
    rewritten_text = rewriteText(text)
    print(rewritten_text)
    # Save the rewritten text to a file
    with open('novel/改文.txt', 'w') as f:
        f.write(rewritten_text)

    return jsonify({'rewritten_text': rewritten_text})


# 保存原文
@app.route('/save_text', methods=['POST'])
def save_text():
    data = request.get_json()
    folder_name = data['folderName']
    text = data['text']
    directory = 'novel/' + folder_name

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(directory + '/原文.txt', 'w', encoding='utf-8') as file:
        file.write(text)

    return 'Text saved successfully'


# 智能分镜导入
@app.route('/read_file', methods=['POST'])
def read_file():
    data = request.get_json()
    filename = 'novel/' + data['filename']

    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()

    return jsonify({'text': text})


# 调用openai_text.ai_fenjing()函数，将原文分镜后返回结果
@app.route('/ai_fenjing', methods=['POST'])
def handle_ai_fenjing():
    data = request.get_json()
    text = data['text']

    result = ai_fenjing(text)
    result = result.replace('镜头语言:', '')

    return jsonify({'result': result})


# 保存分镜设置excl
@app.route('/save_to_csv', methods=['POST'])
def save_to_excel():
    data = request.get_json()
    rows = data['rows']  # 这应该是一个包含所有行的列表，每一行也是一个列表，包含两个元素：“原文”和“AI分镜”
    # 打开文件，写入内容
    with open('novel/分镜设置.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # 添加标题行
        writer.writerow(["原文", "AI分镜"])
        # 添加数据行
        for row in rows:
            writer.writerow(row)

    return '', 204


# 读取分镜设置的excl
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    try:
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join('novel', filename)
            file.save(file_path)

            # 增加了encoding='utf-8-sig'，可以处理带有BOM的UTF-8文件
            data = pd.read_csv(file_path, encoding='utf-8-sig')

            # 将数据转换为列表
            rows = data.values.tolist()

            return jsonify({'rows': rows}), 200
        else:
            return '', 400
    except pd.errors.EmptyDataError:
        print("No columns to parse from file")
        return '', 500
    except Exception as e:
        print(e)
        return '', 500
# 人物设定中 中文转英文
@app.route('/translate_text_en2cn', methods=['POST'])
def translate_text_route():
    data = request.get_json()
    text = data['text']  # 英文文本
    translated_text = translate_text_en2cn(text)  # 调用你的翻译函数
    return {'translatedText': translated_text}

@app.route('/translate_text_cn2en', methods=['POST'])
def translate_text_cn2en_router():
    data = request.get_json()
    text = data['text']  # 中文文本
    translated_text_cn2en = translate_text_cn2en(text)  # 调用你的翻译函数
    return {'translatedText': translated_text_cn2en}

# 全面描述词 提交保存


@app.route('/save_to_config', methods=['POST'])
def save_to_config():
    data = request.get_json()
    globalHint = data['globalHint']
    characterSetting = data['characterSetting']
    # with open('config.json', 'w',encoding="utf-8") as json_file:
    #     json.dump(data, json_file,ensure_ascii=False,indent=4)
    # return '', 204
    if os.path.exists('config.json'):
        with open('config.json','rb',encoding="utf-8") as f:
            config = json.load(f)
    config['globalHint'] = globalHint
    config['characterSetting'] = characterSetting
    with open('config.json','w',encoding="utf-8") as json_file:
        json.dump(config, json_file,ensure_ascii=False,indent=4)
    return '', 204


# 生成关键词
@app.route('/ai_prompt', methods=['POST'])
def handle_ai_prompt():
    try:
        data = request.get_json()
        text = data['text']

        result = ai_prompt(text)
        # result = result.replace('镜头语言:', '')

        return jsonify({'result': result})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

# 生成翻译

# 保存关键词
@app.route('/save_csv', methods=['POST'])
def save_csv():
    data = request.get_json()['data']
    filename = 'novel/关键词.csv'

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['原文', 'AI分镜', '关键词'])
        writer.writeheader()
        writer.writerows(data)

    return '', 204  # return no content

@app.route('/get_image_urls', methods=['GET'])
def get_image_urls():
    image_folder = 'image'
    image_files = os.listdir(image_folder)
    image_urls = [url_for('static', filename=image_file, _external=True) for image_file in image_files]
    return jsonify(imageUrls=image_urls)
# 从文件夹里读取关键词
@app.route('/load_csv', methods=['POST'])
def load_csv():
    file = request.files['file']
    # filename = 'novel/' + secure_filename(file.filename)
    filename = 'novel/关键词.csv'
    print(filename)
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    # print(data)
    return jsonify({'data': data})


@app.route('/upload', methods=['POST'])
def upload_file():
    global data
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    text_file = io.TextIOWrapper(file, encoding='utf-8')
    reader = csv.reader(text_file)
    next(reader)  # 跳过标题行
    data = list(reader)  # 保存数据到全局变量 data

    # 我们假设 CSV 文件的列是按照 '原文', 'AI分镜', '关键词' 的顺序排列的
    result = {
        'yuanwen': [row[0] for row in data],
        'fenjing': [row[1] for row in data],
        'key': [row[2] for row in data]
    }
    return jsonify(result)

# 编辑更新
@app.route('/save', methods=['POST'])
def save():
    global data
    if not data:
        return jsonify({'status': 'error', 'message': 'No data to save. Please upload a file first.'}), 400
    request_data = request.get_json()
    # 这是要更新的行的索引
    index = int(request_data.get('yuanwen_n'))
    fenjing = request_data.get('fenjing')
    key = request_data.get('key')

    # 更新数据
    data[int(index)] = [data[int(index)][0], fenjing, key]
    # data[index][1] = fenjing
    # data[index][2] = key
    # 将更新后的数据写回 CSV 文件
    with open('novel/关键词.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['原文', 'AI分镜', '关键词'])  # Write the header row
        writer.writerows(data)

    return jsonify({'status': 'success'})

# @app.route('/images/<filename>')
# def get_image(filename):
#     return send_from_directory('image', filename)
# 生成图片
@app.route('/generate_images', methods=['POST'])
def generate_images():
    data = request.get_json()
    config_path = data.get('configPath')
    prompt_path = data.get('promptPath')
    image_urls = run_program_with_args(config_path, prompt_path)
    return jsonify(imageUrls=image_urls)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
