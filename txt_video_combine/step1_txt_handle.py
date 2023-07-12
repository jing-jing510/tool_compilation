# from flask import Flask,request
#
# app = Flask(__name__)
#
#
# @app.route('/upload',methods=['POST'])
# def upload_file():
#     file = request.files['file']
#     file.save(file.filename)

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/handle_file', methods=['POST'])
def handle_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        file_contents = file.read().decode('utf-8')
        return jsonify({'file_contents': file_contents})
    return jsonify({'error': 'Invalid file'})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'docx'}

if __name__ == '__main__':
    app.run()