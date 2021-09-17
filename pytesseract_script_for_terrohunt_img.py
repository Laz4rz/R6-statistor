import pytesseract
import numpy as np

from fuzzywuzzy import fuzz

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


def get_total_fuzz(player_name: str, word_to_compare: str) -> int:
    ratio = fuzz.ratio(player_name, word_to_compare)
    partial_ratio = fuzz.partial_ratio(player_name, word_to_compare)
    tokensort_ratio = fuzz.token_sort_ratio(player_name, word_to_compare)
    total_ratio = ratio + partial_ratio + tokensort_ratio
    return total_ratio


result = pytesseract.image_to_string('results/terrohunt_thresh.jpg')
results = result.split(sep='\n')

players = [
    'Laz4rz',
    'Terrorysta'
]

ratios_dict = {}
results_dict = {}

for enum, row in enumerate(results):
    ratios_dict[enum] = {}

    for word in row.split(sep=' '):
        ratios_dict[enum][word] = {}
        for player in players:
            ratios_dict[enum][word][player] = get_total_fuzz(player_name=player, word_to_compare=word)

for row in ratios_dict:
    killer_killed = []
    for word in ratios_dict[row]:
        if np.any(np.fromiter(ratios_dict[row][word].values(), dtype=int) > 100):
            player_max_ratio = max(ratios_dict[row][word], key= lambda x: ratios_dict[row][word][x])
            killer_killed.append(player_max_ratio)
    if len(killer_killed) > 0: results_dict[row] = killer_killed

