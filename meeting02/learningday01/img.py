from google import genai
import base64

client = genai.Client(api_key="AIzaSyBJFaGaBp9t3pLGSavCSTuaCP48Fj5LdrA")

# Correct image generation call
response = client.models.generate_images(
    model="gemini-1.5-flash",   # free model
    prompt="A cute robot studying in a library, high quality"
)

# Extract base64 for the first image
image_base64 = response.generated_images[0].inline_data.data

# Decode
image_bytes = base64.b64decode(image_base64)

with open("generated_image.png", "wb") as f:
    f.write(image_bytes)

print("✅ Image saved successfully as generated_image.png")
