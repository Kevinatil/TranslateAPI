import os
import re
import json

from zai import ZhipuAiClient
from . import Translator

def get_api_key():
    with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as f:
        data = json.load(f)['zhipu']
    return data['APIKEY']

APIKEY = get_api_key()


class Chatter:
    def __init__(self, model_name = "glm-4.7"):
        self.model_name_all = ["glm-4.5", "glm-4.6", "glm-4.7"]

        assert model_name in self.model_name_all
        self.model_name = model_name

        self.client = ZhipuAiClient(api_key=APIKEY)

    def chat_no_rag(self, user_input, messages = None):
        if messages is None:
            messages = []
        messages.append({"role": "user", "content": user_input})

        r = self.client.chat.completions.create(model=self.model_name, messages=messages, thinking={'type': 'disabled'})
        reply = r.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})

        return reply, messages



class Translator_zhipu(Translator):
    def __init__(self, sleep_time = 5):
        self.sleep_time = sleep_time
        self.chatter = Chatter(model_name='glm-4.7')
        self.lang_map = {
            'zh': '中文',
            'ch': '中文',
            'en': '英文',
            'fr': '法文',
            'ko': '韩文',
        }
        self.default_translation_prompt = '请你将给定的字幕翻译成{}，{}翻译结果以如下格式输出：{{"result": <翻译结果>}}，不要输出其他无关内容。请确保翻译结果语句通顺合理，最好口语化一点。需要翻译的内容为：{}'

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

