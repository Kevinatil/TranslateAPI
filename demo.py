import pysrt
import time
from tqdm import tqdm

from . import TranslatorAll

## google demo
type = 'google'

name = 'demo.srt'
out_name = name + '_translated_{}.srt'.format(type)
subs = pysrt.open(name, encoding='utf-8')
translator = TranslatorAll(type=type)

for i, sub in tqdm(enumerate(subs)):
    translated = translator.translate(sub.text, source_lang='ko', target_lang='zh', post_process = True)
    print(translated)
    # sub.text += '\n{}'.format(translated)
    sub.text = translated
    time.sleep(translator.sleep_time)

    if i % 100 == 0:
        subs.save(out_name, encoding='utf-8')

subs.save(out_name, encoding='utf-8')




## zhipu demo
type = 'zhipu'

name = 'demo.srt'
out_name = name + '_translated_{}.srt'.format(type)
subs = pysrt.open(name, encoding='utf-8')
translator = TranslatorAll(type=type)

keywords = {
    'TT': 'TikTok'
}
translator.add_key_words(keywords)

for i, sub in tqdm(enumerate(subs)):
    translated = translator.translate(sub.text, source_lang='ko', target_lang='zh', post_process = True)
    print(translated)
    # sub.text += '\n{}'.format(translated)
    sub.text = translated
    time.sleep(translator.sleep_time)

    if i % 100 == 0:
        subs.save(out_name, encoding='utf-8')

subs.save(out_name, encoding='utf-8')