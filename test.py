from groq import Groq

client = Groq(
    api_key="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"
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Hello",
        }
    ],
    model="llama-3.3-70b-versatile"
)

print(chat_completion.choices[0].message.content)