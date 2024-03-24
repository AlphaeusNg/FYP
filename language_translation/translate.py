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
# 2nd iteration
#  want you to act as a translator, spelling corrector and improver. 
# I will send you {original_language} texts taken from Optical Camera Recognition (OCR) and I want you translate them into {translated_language}.
# Consider potential OCR errors, and answer in the corrected and improved version of my text. Make a contextual guess if the input is rubbish.
# I want you to only reply the corrected, improved translated text, and nothing else, do not write explanations. 

# 3rd iteration
# I want you to act as a translator, spelling corrector and improver. 
# I will send you {original_language} texts taken from Optical Camera Recognition (OCR) and I want you translate them into {translated_language}.
# Each text detection will be separated by |. You must add | after each translated segment.
# Consider potential OCR errors, and answer in the corrected and improved version of my text. Make a contextual guess if the input is rubbish.
# I want you to only reply the corrected, improved translated text, and nothing else.
# You must not write explanations. 

# 4th iteration
# """
#                 Task Description:
# I need your assistance as a translator, spelling corrector, and text improver. I will provide texts in {original_language} extracted from Optical Character Recognition (OCR), and I need them translated into {translated_language}. Each segment of text will be separated by a '|'. Please consider potential OCR errors and provide the corrected and improved translation. If the input is unclear or nonsensical, make a contextual guess to produce a meaningful output. Only provide the corrected and improved translated text as the output, without any additional explanations.

# Input Format:

# Texts in {original_language} extracted from OCR, separated by '|'
# Example: '暮 磯|馨 売|で娘町働 \'也や 』 ?ザ 曹|サ洲いや旧|二 つか つにつ え小『 " や ?|荒あ 盤ンんと|形紫 ; やッ6|る|や: ゆゅ|当をる あで 生 亀|\' 農|やの ラな 慧 や) 相や加口_~ね? 藍|夢 喜|1 也や〔山にやこ|ゼ 園 8 四卯 念|鷺 』|登|葉」る 3 櫛前 を 露 お 惣二 糸 そえ 帽) 〔 篤プ 」ハワ ? 八一 1 ふ 課 ・ー 馨 峯 らにか 1 1 ら ゃなる _ メハリザ 』 ‥「くの八ノ・ト \' ? ~ 』 レ メ こ か 葉 ろち」 ぜ小いあ 変 劇 駒三 86 ま $ す 地川る (ふ にあ 長 5ゃ ギ子 \' 蘭 3 ゆ へんな 深 白 な 川太た「ん さと 競三 呂~ト ベ^ド ゆ5ん」 び- お い * あ \'やん地; い子ね. ! #~~_ 豊 ノ節 上) 議芸 こ 台|! $ ふりけ》な :'
# Output Format: 'Living by the coast|Fragrant sale|Working in the town|And so|General Cao|Old state|Two, connected|Small|And?|Rough disc|Purple shape|And 6|To do|And: Softly|To live with turtles|Farming|And wisdom|Mutual addition|Indigo|Dream joy|Also in the mountains|Garden, Eight, April, Memorial|Heron|Climbing|Leaves, Before dawn, Dew, Sown with threads|Diligently, Hawaii?|Eight, Lesson, Fragrant peak|Becoming gentle|Mysterious|And the small leaves|Dramatic change, Komasa, $86, Flowing river|Long, Orchid child|Towards the deep, Shirota|Competition, Bed|And the rich season|Art discussion, Platform|Waving!'

# Ensure translations are accurate, fluent, and error-free, taking into account any potential OCR inaccuracies.
# Maintain appropriate tone and style consistent with the context of the texts.
# If the input is ambiguous or nonsensical, produce a contextually relevant translation."""

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



def translate_language(text, original_language: str="English", translated_language: str="Chinese", development_mode=False):
    if development_mode:
        return "test 420"
    
    SYSTEM_CONTENT = f"""Task Description:
I need your assistance as a translator, spelling corrector, and text improver. 
I will provide texts in {original_language} extracted from Optical Character Recognition (OCR), and I need them translated into {translated_language}. 
Please consider potential OCR errors and provide the corrected and improved translation. 
If the input is unclear or nonsensical, make a contextual guess to produce a meaningful output. 
Only provide the corrected and improved translated text as the output, without any additional explanations.
"""
    # Remove \n and extra spaces from the prompt
    SYSTEM_CONTENT = ' '.join(SYSTEM_CONTENT.split())
    # Define the prompt for translation
    prompt = f"{text}"

    # Call the OpenAI API to get the translation
    response = openai.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": SYSTEM_CONTENT},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4096,
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

