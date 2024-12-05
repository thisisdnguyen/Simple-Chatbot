from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = [{
        "role": "user",
        "content": "Hello!"
    }]

class ChatResponse(BaseModel):
    message: str

genai.configure(api_key=os.getenv("GENAI_API_KEY"))

@app.post('/api/v1/chat', response_model=ChatResponse)
def chat(inputs: ChatRequest):
    try:
        # Tạo lịch sử hội thoại thành một chuỗi văn bản
        conversation_history = "\n".join([f"{entry['role']}: {entry['content']}" for entry in inputs.history])

        # Kết hợp lịch sử hội thoại và tin nhắn hiện tại thành một đầu vào duy nhất
        full_input = f"{conversation_history}\nuser: {inputs.message}"

        model = genai.GenerativeModel("gemini-1.5-flash")
        
        response = model.generate_content(full_input)  # Chỉ truyền một đối số duy nhất

        # Kiểm tra nếu phản hồi không có nội dung hợp lệ
        if not response or not hasattr(response, 'text'):
            raise HTTPException(status_code=400, detail="Failed to generate a valid response.")
        
        # Trả về phản hồi được tạo
        return {"message": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
