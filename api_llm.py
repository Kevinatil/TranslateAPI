import re
import json
from openai import OpenAI

from . import Translator

class Chatter:
    def __init__(self, model_name = 'deepseek-r1:8b'):
        self.model_name_all = ['deepseek-r1:8b']

        assert model_name in self.model_name_all
        self.model_name = model_name

        self.client = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

    def chat_no_rag(self, user_input, messages = None):
        if messages is None:
            messages = []
        messages.append({"role": "user", "content": user_input})

        r = self.client.chat.completions.create(model=self.model_name, messages=messages)
        reply = r.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})

        return reply, messages



class Translator_llm(Translator):
    def __init__(self, sleep_time = 0):
        self.sleep_time = sleep_time
        self.chatter = Chatter(model_name='deepseek-r1:8b')
        self.lang_map = {
            'zh': '中文',
            'ch': '中文',
            'en': '英文',
            'fr': '法文',
            'ko': '韩文',
        }
        self.default_translation_prompt = '请你将给定的字幕翻译成{}，{}翻译结果以如下格式输出：{{"result": <翻译结果>}}，不要输出其他无关内容。请确保翻译结果语句通顺合理。需要翻译的内容为：{}'

    def _parse_json(self, s):
        s = re.sub(r'\n', ' ', s)
        find = re.findall(r'\{.+\}', s)[0]
        return json.loads(find)

    def _translate(self, text: str, source_lang: str = 'auto', target_lang: str = 'en') -> str:
        text = re.sub('\n', ' ', text)

        source_prompt = '字幕所用语言为{}，'.format(self.lang_map[source_lang]) if source_lang != 'auto' else ''
        prompt = self.default_translation_prompt.format(self.lang_map[target_lang], source_prompt, text)

        output = self.chatter.chat_no_rag(prompt)[0]
        output = self._parse_json(output)['result']

        return output


