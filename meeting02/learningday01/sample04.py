from google import genai

client = genai.Client(api_key="AIzaSyBJFaGaBp9t3pLGSavCSTuaCP48Fj5LdrA")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)