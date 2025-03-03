from flask import Flask, render_template, request, jsonify
from google import genai
import requests

app = Flask(__name__)

# Google Generative AI API 엔드포인트 및 API 키
API_KEY = "AIzaSyAdhxyDrqLe36vXLntLBnKTM195KZX6Jv0"  # 실제 API 키로 대체

@app.route('/')
def home():
    return render_template('index.html')  # index.html 파일 준비 필수

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    
    if not user_input:
        return jsonify({"error": "No input text received."}), 400
    
    try:
        # Google Generative AI 클라이언트 생성
        client = genai.Client(api_key=API_KEY)

        # 메시지를 AI 모델에 전달
        # response = client.models.generate_text(
        #     model="gemini-2.0-flash",  # 정확한 모델 버전 확인 필요
        #     prompt=user_input,
        #     parameters={
        #         "temperature": 0.7,
        #         "max_tokens": 150
        #     }
        # )
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            # gemini-1.5-flash
            contents=user_input,
            # parameters={
            #     "temperature": 0.7,
            #     "max_tokens": 150
            # }
        )
        # 응답 결과 출력 및 전달
        bot_reply = response.text
        
        print("Bot Reply:", bot_reply)
        
        return jsonify({"reply":bot_reply})
    
    except KeyError as e:
        # JSON 데이터를 예상 결과 형식으로 처리하지 못할 때
        print("KeyError:", e)
        return jsonify({"error": "Unexpected response format.", "details": str(e)}), 500

    except Exception as e:
        # 기타 예외 처리
        print("Error:", e)
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)  # Flask 디버그 모드 활성화
