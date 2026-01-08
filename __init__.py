import re
import time
from warnings import warn

class Translator:
    sleep_time: int = 1

    def _translate(self, text: str, source_lang: str = 'auto', target_lang: str = 'auto') -> str:
        pass

    def post_process(self, text, conduct=True):
        if conduct:
            text = re.sub(r'\s', '', text)
            text = re.sub(r'[。，]', ' ', text)
            return text
        else:
            return text

    def translate(self, text: str, source_lang: str = 'auto', target_lang: str = 'auto', post_process: bool = True, retry: int = 5) -> str:
        for i in range(retry):
            try:
                return self.post_process(self._translate(text, source_lang, target_lang))
            except Exception as e:
                print(e)
                warn('translate err, sleep {}s, retry time {}'.format(self.sleep_time, i), Warning)
                time.sleep(self.sleep_time)
        return text



class TransFactory:
    
    @classmethod
    def create_translator(cls, type: int, **kwargs) -> Translator:
        # if type not in cls._translators:
        #     raise ValueError(f"不支持的翻译器类型: {type}. 支持的类型: {list(cls._translators.keys())}")
        if type == 'tc':
            from .api_tencent import Translator_tencent
            translator_class = Translator_tencent # cls._translators[type]
        elif type == 'llm':
            from .api_llm import Translator_llm
            translator_class = Translator_llm
        elif type == 'zhipu':
            from .api_zhipu import Translator_zhipu
            translator_class = Translator_zhipu
        elif type == 'baidu':
            from .api_baidu import Translator_baidu
            translator_class = Translator_baidu
        return translator_class(**kwargs)

def TranslatorAll(type: str = 'tc', **kwargs) -> Translator:
    return TransFactory.create_translator(type, **kwargs)

if __name__ == "__main__":
    translator = TranslatorAll(type='tc')
    
    text = "다 같이 에펠탑 보러 가는 것으로 하루를 마무리했어요"

    print(translator.translate('저녁엔 식사 약속이 있었습니다', source_lang='ko', target_lang='zh'))