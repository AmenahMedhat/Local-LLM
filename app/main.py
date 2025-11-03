# app/main.py

import requests
import gradio as gr
import json

# Local Ollama API
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "hala-1.2b-arabic"  # The name you created with your Modelfile

def chat_with_model(prompt):
    """Send the user prompt to the local Ollama model and return its response."""
    try:
        # Request streaming response
        response = requests.post(OLLAMA_API_URL, json={
            "model": MODEL_NAME,
            "prompt": prompt
        }, stream=True)

        # Collect partial responses
        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    if "response" in data:
                        full_response += data["response"]
                except Exception:
                    continue  # Ignore malformed partial lines

        return full_response or "لم يتم الحصول على رد من النموذج."
    except Exception as e:
        return f"حدث خطأ أثناء الاتصال بالنموذج: {e}"


# Gradio interface
iface = gr.Interface(
    fn=chat_with_model,
    inputs=gr.Textbox(lines=5, placeholder="اكتب استفسارك المالي هنا..."),
    outputs="text",
    title="المساعد الاقتصادي المحلي 🤖",
    description="يستخدم نموذج Hala-1.2B المحلي عبر Ollama لتحليل البيانات المالية وكتابة تقارير بالعربية."
)

if __name__ == "__main__":
    iface.launch()
