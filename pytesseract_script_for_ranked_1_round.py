import os

import cv2
import pytesseract
import numpy as np

from tqdm import tqdm
from typing import List
from thefuzz import fuzz

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


def get_total_fuzz(player_name: str, word_to_compare: str) -> int:
    ratio = fuzz.ratio(player_name, word_to_compare)
    partial_ratio = fuzz.partial_ratio(player_name, word_to_compare)
    token_sort_ratio = fuzz.token_sort_ratio(player_name, word_to_compare)
    # token_set_ratio = fuzz.token_set_ratio(player_name, word_to_compare)
    total_ratio = ratio + partial_ratio + token_sort_ratio
    return total_ratio


def get_image_list(directory_path: str) -> List:
    all_files = os.listdir('ranked_1_round')
    all_files.sort(key = lambda x: int(x.split(sep='_')[0]))
    for file in all_files:
        extension = file.split(sep='.')[1]
        if extension != 'jpg':
            raise Exception(f'Encountered file with with wrong extension: {file}, expected .jpg')
        image_type = file.split(sep='_')[2]
        if image_type == 'original':
            yield file


team1 = [
    'Laz4rz',
    'happijessie',
    'Vanity.-.',
    'Huzzah_Nugg',
    'Shamoocow'
]

team2 = [
    'PeterPane',
    'Big_Belly_Billy',
    'Batts.InVi',
    'Abum.InVi',
    'ysixzi'
]

players = team1 + team2

images = get_image_list(directory_path='ranked_1_round')
detection = []

for image in tqdm(images):
    img = cv2.imread(f'ranked_1_round/{image}', cv2.IMREAD_GRAYSCALE)
    thresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)[1]
    result = pytesseract.image_to_string(thresh)
    results = result.split(sep='\n')

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
            if np.any(np.fromiter(ratios_dict[row][word].values(), dtype=int) > 190):
                player_max_ratio = max(ratios_dict[row][word], key= lambda x: ratios_dict[row][word][x])
                killer_killed.append(player_max_ratio)
        if len(killer_killed) > 1:
            results_dict[row] = killer_killed
            if killer_killed[0] in team1 and killer_killed[1] in team2\
                    or killer_killed[1] in team1 and killer_killed[0] in team2:
                detection.append([killer_killed[0], killer_killed[1], image.split('_')[0]])

killfeed = []
for entry in detection:
    if [entry[0], entry[1]] in killfeed:
        continue
    else:
        killfeed.append([entry[0], entry[1]])

stats = {}
for player in players:
    stats[player] = {
        'kills': 0,
        'deaths': 0
    }

for entry in killfeed:
    print(entry[0]+' killed '+entry[1])
    stats[entry[0]]['kills'] += 1
    stats[entry[1]]['deaths'] += 1

team2_stats = []
for player in team2:
    team2_stats.append(player + ' Kills: ' + str(stats[player]['kills']) + ' Deaths: ' + str(stats[player]['deaths']))

for entry in team2_stats:
    print(str(entry))

team1_stats = []
for player in team1:
    team1_stats.append(player + ' Kills: ' + str(stats[player]['kills']) + ' Deaths: ' + str(stats[player]['deaths']))

for entry in team1_stats:
    print(str(entry))
