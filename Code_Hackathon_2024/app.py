import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS  # Thêm thư viện Flask-CORS


app = Flask(__name__)
CORS(app)  # Kích hoạt CORS

API_KEY = 'AIzaSyAeRwbaE9PZtvmjqBv2mKwYfIW0rcKcwUw'  # Thay thế bằng API key hợp lệ của bạn
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

@app.route('/chat', methods=['POST', 'OPTIONS'])  # Thêm phương thức OPTIONS
def chat_endpoint():
    if request.method == 'OPTIONS':  # Xử lý yêu cầu OPTIONS cho CORS
        return '', 200

    data = request.get_json()
    if 'message' not in data:
        return jsonify({"error": "Missing 'message' parameter"}), 400

    user_message = data['message']

    try:
        bot_response = interact_with_chatbot(user_message)
        return jsonify({"response": bot_response})
    except Exception as e:  # Xử lý các lỗi chung
        return jsonify({"error": f"Internal Server Error: {e}"}), 500


def interact_with_chatbot(question):
    response = chat.send_message(question)
    cleaned_response = response.text.replace('*', '')
    return cleaned_response

if __name__ == '__main__':
    app.run(debug=True)
