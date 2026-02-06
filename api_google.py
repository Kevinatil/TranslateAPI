import os
import re
import json

from googletrans import Translator as GTranslator

from . import Translator

class Translator_google(Translator):
    def __init__(self, sleep_time = 5):
        self.sleep_time = sleep_time

        self.translator = GTranslator()

        self.support_languages = ['zh-cn', 'en', 'fr', 'ko', 'ja', 'auto']

    def _translate(self, text: str, source_lang: str = 'auto', target_lang: str = 'en') -> str:
        if target_lang in ['zh', 'ch']:
            target_lang = 'zh-cn'
        if not (source_lang in self.support_languages and target_lang in self.support_languages):
            raise RuntimeError('source_lang and target_lang must in [{}]'.format(', '.join(self.support_languages)))

        text = re.sub('\n', ' ', text)

        ret = self.translator.translate(text, src=source_lang, dest=target_lang)
        return ret.text

if __name__ == "__main__":
    # pip install googletrans==4.0.0rc1
    translator = Translator_google()
    print(translator._translate('hello', target_lang='zh-cn'))