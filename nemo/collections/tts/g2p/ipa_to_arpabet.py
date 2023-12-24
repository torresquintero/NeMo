def is_affricate(first_phone, second_phone):
    valid_affricates = ['tʃ', 'dʒ']
    return f'{first_phone}{second_phone}' in valid_affricates


def is_diphthong(first_phone, second_phone):
    valid_diphthongs = ['aʊ', 'aɪ', 'eɪ', 'oʊ', 'ɔɪ']
    return f'{first_phone}{second_phone}' in valid_diphthongs


def a_handler(current_phone, next_phone):
    if not is_diphthong(current_phone, next_phone):
        return 'AA'
    if next_phone == 'ʊ':
        return 'AW'
    if next_phone == 'ɪ':
        return 'AY'
    raise_parse_error('unk', current_phone, next_phone)


def raise_parse_error(previous_phone, current_phone, next_phone):
    raise ValueError(f"We don't know how to deal with {current_phone} in the context "
                     f"'{previous_phone}{current_phone}{next_phone}'")


def is_vowel(phone):
    vowels = ['æ', 'ʌ', 'ɛ', 'ɝ', 'i', 'u', 'ə', 'ɚ', 'ᵻ',
              'a', 'e', 'o', 'ɔ', 'ʊ', 'ɪ', 'ɑ', 'ɜ', 'ɐ']
    return phone in vowels


def stress(phone):
    if phone == "ˈ":
        return '1'
    if phone == 'ˌ':
        return '2'
    return '0'

    

def _ipa2arpabet(previous_phone, current_phone, next_phone):

    mapping = {
        # normal consonants
        'b': 'B',
        'ð': 'DH',
        'f': 'F',
        'ɡ': 'G',
        'h': 'HH',
        'k': 'K',
        'l': 'L',
        'm': 'M',
        'n': 'N',
        'ŋ': 'NG',
        'p': 'P',
        'ɹ': 'R',
        's': 'S',
        'θ': 'TH',
        'v': 'V',
        'w': 'W',
        'j': 'Y',
        'z': 'Z',
        'ɾ': 'T',

        # potential start of affricate
        't': 'CH' if is_affricate(current_phone, next_phone) else 'T',
        'd': 'JH' if is_affricate(current_phone, next_phone) else 'D',

        # potential end of affricate
        'ʃ': '' if is_affricate(previous_phone, current_phone) else 'SH',
        'ʒ': '' if is_affricate(previous_phone, current_phone) else 'ZH',

        # normal vowels
        'æ': 'AE',
        'ɛ': 'EH',
        'ɜ': 'EH',
        'ɝ': 'ER',
        'i': 'IY',
        'u': 'UW',
        'ɚ': 'ER',
        'ᵻ': 'IH',
        'ʌ': 'AH',
        'ə': 'AH',
        'ɑ': 'AA',
        "ɐ": 'AH', # maybe a mistake with espeak? not supposed to be in en-US according to https://github.com/espeak-ng/espeak-ng/blob/master/docs/languages/gmw/en.md

        # potential start of diphthong
        'a': a_handler(current_phone, next_phone),
        'o': 'OW' if is_diphthong(current_phone, next_phone) else 'AO',
        'e': 'EY' if is_diphthong(current_phone, next_phone) else 'UNK',
        'ɔ': 'OY' if is_diphthong(current_phone, next_phone) else 'AO',

        # potential end of diphthong
        'ʊ': '' if is_diphthong(previous_phone, current_phone) else 'UH',
        'ɪ': '' if is_diphthong(previous_phone, current_phone) else 'IH',

        # other chars
        "ˈ": '',
        "ˌ": '',
        " ": ' ',
        "ː": '',
    }

    result = mapping[current_phone]

    if result == 'UNK':
        raise_parse_error(previous_phone, current_phone, next_phone)

    if result and is_vowel(current_phone):
        result += stress(previous_phone)

    return result


def ipa2arpabet(string: str) -> list:
    full_arpabet = []

    previous_phone = None 
    for i, current_phone in enumerate(string):
        next_phone = None if i == len(string) - 1 else string[i + 1]
        arpabet = _ipa2arpabet(previous_phone, current_phone, next_phone)
        if arpabet:
            full_arpabet.append(arpabet)
        previous_phone = current_phone

    return full_arpabet
