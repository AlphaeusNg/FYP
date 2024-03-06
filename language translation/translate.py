from settings import *
import openai

# Set up your OpenAI GPT-3 API key
openai.api_key = OPEN_AI_KEY


def translate_japanese_to_english(japanese_text):
    # Define the prompt for translation
    prompt = f"Manga sentence: {japanese_text}."

    # Call the OpenAI API to get the translation
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": SYSTEM_CONTENT},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2048,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract and return the translated text from the response
    translated_text = response.choices[0].message.content

    # First interaction with the model: translate this text
    # Second interaction: refine the text to achieve the natural flow of a native speaker’s writing
    return translated_text


if __name__ == "__main__":
    # Example usage
    japanese_text = "こんにちは、私の名前は太郎です。"
    translated_text = translate_japanese_to_english(japanese_text)
    print(translated_text)  # Output: "Hello, my name is Taro."

