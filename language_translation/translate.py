from language_translation.settings import *
import openai

# Set up your OpenAI GPT-3 API key
openai.api_key = OPEN_AI_KEY

# prompt settings
SYSTEM_CONTENT = """
                I want you to act as an English translator, spelling corrector and improver. 
                I will send you texts taken from Optical Camera Recognition (OCR) and you will detect the language, translate it, consider potential OCR errors, and answer in the corrected and improved version of my text, in English. 
                I want you to replace my simplified A0-level words and sentences with more beautiful and elegant, upper level English words and sentences. 
                Keep the meaning same, but make them more literary. 
                I want you to only reply the correction, the improvements and nothing else, do not write explanations. 
                """
SYSTEM_CONTENT = """
                I want you to act as a translator, spelling corrector and improver. 
                I will send you texts taken from Optical Camera Recognition (OCR) and you will detect the language, translate it, consider potential OCR errors, and answer in the corrected and improved version of my text, in the language asked. 
                I want you to replace my simplified A0-level words and sentences with more beautiful and elegant, upper level words and sentences. 
                Keep the meaning same, but make them more literary. 
                I want you to only reply the correction, the improvements and nothing else, do not write explanations. 
                """
# Remove \n and extra spaces from the prompt
SYSTEM_CONTENT = ' '.join(SYSTEM_CONTENT.split())

# Define a function that maps language codes to their corresponding names
def get_language_name(language_code: str) -> str:
    language_mapping = {
        "en": "English",
        "ja": "Japanese",
        "zh": "Chinese",
        "th": "Thai",
        "fr": "French",
        "de": "German",
        "es": "Spanish",
        "it": "Italian",
        "pt": "Portuguese",
        # Add more language codes and names as needed
    }
    return language_mapping.get(language_code, "Unknown")



def translate_language(text, language: str="en", still_in_development=False):
    if still_in_development:
        return "test 420"
    # Define the prompt for translation
    prompt = f"Translate this sentence into {language}: {text}."

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

    return translated_text


if __name__ == "__main__":
    # Example usage
    text = "Helo, my neme is J0hn"
    translated_text = translate_language(text, "Chinese")
    print(translated_text)  # Output: "Hello, my name is Taro."

# For FYP
# "こんにちは、私の名前は太郎です。" -> 你好，我叫太郎。/ สวัสดีครับ/ค่ะ ฉันชื่อโทโระครับ/ค่ะ. / Hello, my name is Taro.
# "Helo, my neme is J0hn" -> 你好，我的名字是约翰。/ สวัสดีครับ/ค่ะ ฉันชื่อจอห์นครับ/ค่ะ. / Hello, my name is John.
# "Helo, m neme is J0hn" -> 你好，我的名字是约翰。/ สวัสดีครับ/ค่ะ ฉันชื่อจอห์นครับ/ค่ะ. / Hello, my name is John.
# "Helo, m nam is Jhn" -> 你好，我的名字是约翰。/ สวัสดีครับ/ค่ะ ฉันชื่อจอห์นครับ/ค่ะ. / Hello, my name is John.

