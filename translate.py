import json
import os
import re

from deep_translator import GoogleTranslator

cache_dict = {
    "STEM": "STEM",
    "ESL": "ESL",
    "GIS": "GIS",
    "BIM": "BIM",
    "CAD": "CAD",
    "CME": "CME",
    "edX": "edX"
}

language = str(input("tag's lenguage= "))

GT = GoogleTranslator(target=language)
# print(GT.translate('Class Central • Find the best courses, wherever they exist.'))

def my_strip(words):
    if '\n' in words:
            words = words.replace('\n', ' ')
    words = words.replace('      ', ' ')
    words = words.replace('     ', ' ')
    words = words.replace('    ', ' ')
    words = words.replace('   ', ' ')
    words = words.replace('  ', ' ')

    words = words.replace('&shy;', '')
    words = words.replace('&amp;', '&')
    words = words.replace('&#039;', '\'')
    words = words.replace('&#8217;', '\'')
    
    return words

def replace(match):
    words = match.group()[1:-1].strip()
    
    # print(words)
    if words == '':
        return match.group()
    
    # return cached result
    if words in cache_dict.keys():
        if cache_dict[words] == '-----':
            return match.group()
        return cache_dict[words]
    
    if '&&' not in words and len(words) != 0:
        # breakpoint()
        words = my_strip(words)
        print('-'*30)
        print(words, '->')
        try:
            trs = GT.translate(words)
            print(trs)
            trs = ">{0}<".format(trs)

            cache_dict[words] = trs
            return trs

        except:
            print(f'ERR: translating {words}')
            cache_dict[words] = '-----'
            return match.group()

    else:
        cache_dict[words] = '-----'
        return match.group()

if __name__ == "__main__":
    # read dict from file

    # translate for all subdirectory html
    for root, dirs, files in os.walk('.'):
        for file in files:
            path = os.path.join(root, file)
            if '.html' not in path:
                continue

            with open(path, "r", encoding='utf8') as fp:
                html = fp.read()
                print(path + ': ' + str(len(html)))
                pattern = re.compile('>([Ááéíóñúçãa-zA-Z0-9\-\+/~:\:=“”‘!’\(\)%#\?\.\$ \'\"\n,…—`®•●→_|&amp;|&shy;|&nbsp;]+?)<', re.S)
                html2 = re.sub(pattern, replace, html)
            with open(path, "w", encoding='utf8') as fp:
                fp.write(html2)
    
    # save dict to json file
    data = json.dumps(cache_dict)
    with open('dict.json', 'w') as f:
        f.write(data)