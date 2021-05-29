import json
from PIL import Image

class EmojiFinder:
    def __init__(self, options={}):
        self.options = options
        self.emoji_map = json.load(open('lib/map.json', 'r'))
        self.done_pixels = {}

    def closest_emoji(self, pixel):
        self.r = pixel['r']
        self.g = pixel['g']
        self.b = pixel['b']
        match_filename = self.look_up_or_find_emoji(pixel)
        match_image = Image.open(match_filename).convert('RGBA')
        return match_image

    def look_up_or_find_emoji(self, pixel):
        key = f"{pixel['r']}{pixel['g']}{pixel['b']}"
        if self.done_pixels.get(key) is None:
            self.done_pixels[key] = self.find_emoji()
        return self.done_pixels[key]

    def find_emoji(self):
        if self.options["coverage"] is not None:
            coverage = self.options["coverage"]
            top_scores = sorted(self.emoji_map.items(), key=lambda x: self.score_emoji(x[1]))[:coverage]
            best_emoji = self.emoji_with_max_coverage(top_scores)
            return best_emoji
        else:
            best_emoji = sorted(self.emoji_map.items(), key=lambda x: self.score_emoji(x[1]))[0][0]
            return best_emoji        

    def score_emoji(self, rgb):
        score = abs(rgb['red'] - self.r) + abs(rgb['green'] - self.g) + abs(rgb['blue'] - self.b)
        return score

    def emoji_with_max_coverage(self, scores):
        return sorted(scores, key=lambda x: x[1]['coverage'], reverse=True)[0][0]