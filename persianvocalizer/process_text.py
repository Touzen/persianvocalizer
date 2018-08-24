import string

d = { 'а': 'a',
      'б': 'b',
      'в': 'v',
      'г': 'g',
      'ғ': 'q',
      'д': 'd',
      'е': 'e',
      'ё': 'yā',
      'ж': 'ž',
      'з': 'z',
      'и': 'i',
      'ӣ': 'ī',
      'й': 'y',
      'к': 'k',
      'қ': 'q',
      'л': 'l',
      'м': 'm',
      'н': 'n',
      'о': 'ā',
      'п': 'p',
      'р': 'r',
      'с': 's',
      'т': 't',
      'у': 'o',
      'ӯ': 'u',
      'ф': 'f',
      'х': 'x',
      'ҳ': 'h',
      'ч': 'č',
      'ҷ': 'j',
      'ш': 'š',
      'ъ': '\'',
      'э': 'e',
      'ю': 'yu',
      'я': 'ya'}

allowed_chars = list(d.keys()) + [' ', '\n', '1', '2', '3', '4', '5', '6', '7', '8', '9']
translator = str.maketrans('', '', string.punctuation)

with open('tgk.txt', 'r') as original:
    with open('transcribed.txt', 'w') as transcribed:
        for l_number, line in enumerate(original):
            if l_number % 10**4 == 0:
                print('Processing line #%d...'%(l_number,))

            line = line.lower().strip()
            transcribed_line = []
            processed_line = ''
            for character in line:
                if character not in allowed_chars and character not in string.punctuation + '«' + '»':
                    print(character, end='')
                    # We skip lines that contain unknown special characters
                    processed_line = None
                    break
                else:
                    if character in d:
                        processed_line += d[character]
                    elif character in '!.?':
                        processed_line += character + '\n'
                    else:
                        processed_line += character
            if processed_line and len(processed_line) > 2:
                transcribed.write(processed_line)
                transcribed.write('\n')

