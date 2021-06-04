from dataiku import pandasutils as pdu
import re
import neologdn
import emoji

def clean_text(text):
    text = neologdn.normalize(text) # 全角・半角の統一と重ね表現の除去
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE) # URLの除去
    text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', text)
    text = ''.join(['' if c in emoji.UNICODE_EMOJI else c for c in text]) # emojiの除去
    text = re.sub(r'(\d)([,.])(\d+)', r'\1\3', text) # 桁区切りの除去
    text = re.sub(r'\d+', '0', text) # 数字の置換。意味的な分析ででは、数字の具体的な値を使えないことが多く、いたずらにボキャブラリを増やすだけで、後のタスクでは役に立たないことが多いため
    text = re.sub(r'[!-/:-@[-`{-~]', r' ', text) # 半角記号の置換
    text = re.sub(u'[■-♯【】]', '', text) # 全角記号の置換 (ここでは0x25A0 - 0x266Fのブロックのみを除去)
    text = text.replace(u' ', '').replace(u'　', '').replace(u'「', '').replace(u'」', '').replace('・', "").replace('、', "")
    return text