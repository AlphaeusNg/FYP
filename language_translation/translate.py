from language_translation.settings import *
import openai

# Set up your OpenAI GPT-3 API key
openai.api_key = OPEN_AI_KEY

# prompt settings
SYSTEM_CONTENT = """
Task Description:
I need your assistance as a translator, spelling corrector, and text improver. 
I will provide texts in {original_language} extracted from Optical Character Recognition (OCR), and I need them translated into {translated_language}. 
Please consider potential OCR errors and provide the corrected and improved translation. 
If the input is unclear or nonsensical, make a contextual guess to produce a meaningful output. 
ONLY provide the corrected and improved translated text as the output, you MUST NOT have any additional explanations.
"""

def clean_prompt(prompt: str) -> str:
    """Remove extra spaces and newline characters from the prompt."""
    return ' '.join(prompt.split())


def translate_language(text, original_language: str="English", translated_language: str="Chinese"):

    # Define the prompt for translation
    system_prompt = clean_prompt(SYSTEM_CONTENT.format(original_language=original_language, translated_language=translated_language))

    # Call the OpenAI API to get the translation
    response = openai.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        max_tokens=4096,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract and return the translated text from the response
    return response.choices[0].message.content


if __name__ == "__main__":
    # Example usage
    text = "Helo, my neme is J0hn"
    translated_text = translate_language(text=text, original_language="English", translated_language="Chinese")
    print(translated_text)  # Output: "Hello, my name is Taro."

