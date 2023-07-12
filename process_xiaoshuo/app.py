from flask import Flask, request, jsonify
import openai

openai.api_key = 'your-api-key'

app = Flask(__name__)

@app.route('/get_answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    question = data['question']
    engine = data['engine']
    response = openai.Completion.create(
        engine=engine,
        prompt=question,
        max_tokens=150
    )
    return jsonify({'answer': response.choices[0].text.strip()})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
