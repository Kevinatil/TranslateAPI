import pysrt
import time
from tqdm import tqdm

from videocr.translate import TranslatorAll

# 不要直接在文件夹里执行


# translator = TranslatorAll(type='zhipu')
# text = '저녁엔 식사 약속이 있었습니다' # "다 같이 에펠탑 보러 가는 것으로 하루를 마무리했어요" # '저녁엔 식사 약속이 있었습니다'
# print(translator.translate(text, source_lang='ko', target_lang='zh'))



name = 'full1.srt'
out_name = name + '_translated.srt'
subs = pysrt.open(name, encoding='utf-8')
translator = TranslatorAll(type='zhipu')

for sub in tqdm(subs):
    translated = translator.translate(sub.text, source_lang='ko', target_lang='zh', post_process = True)
    sub.text = translated
    time.sleep(translator.sleep_time)

subs.save(out_name, encoding='utf-8')




# for sub in tqdm(subs):
#     translated = translator.post_process(sub.text)
#     sub.text = translated