import google.generativeai as genai

genai.configure(api_key="AIzaSyDloTU8alHp2JLXWFkQzPuNFK_4-8q6ckg")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works")
print(response.text)