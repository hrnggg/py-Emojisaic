from PIL import Image
import json

class EmojiScanner:
    def __init__(self, filepath):
        self.filepath = filepath
        self.image = Image.open(filepath)
        self.init_colors()
        self.init_total()
        self.scan_emoji()
        self.divide_result()

    def init_total(self):
        self.total_pixels = self.image.size[0] * self.image.size[1]

    def init_colors(self):
        self.red = 0
        self.blue = 0
        self.green = 0
        self.counted_pixels = 0

    def divide_result(self):
        self.red //= self.counted_pixels
        self.blue //= self.counted_pixels
        self.green //= self.counted_pixels
    
    def write(self):
        filename = self.filepath.split('/')[1]
        number = int(filename.split('.')[0])
        print("\rdoing {:3d}.png".format(number), end="")
        full_list = json.load(open('lib/map.json'))
        full_list[self.filepath] = self.emoji_score()        
        with open('lib/map.json', 'w') as f:
            json.dump(full_list, f, indent=4)

    def emoji_score(self):
        return dict(
            red=self.red,
            green=self.green,
            blue=self.blue,
            coverage=int(self.coverage_percentage())
        )

    def coverage_percentage(self):
        return self.counted_pixels / 4096 * 100

    def scan_emoji(self):
        if self.image.mode == 'P' or self.image.mode == 'LA':
            self.image = self.image.convert('RGBA')
        width, height = self.image.size
        for x in range(width):
            for y in range(height):
                pixel = self.image.getpixel((x, y))
                if self.image.mode[-1] == 'A':
                    opacity = 255 - pixel[-1]
                    if opacity > 245:
                        continue
                self.scan_pixel(pixel)

    def scan_pixel(self, pixel):
        self.counted_pixels += 1                
        self.red += pixel[0]
        self.green += pixel[1]
        self.blue += pixel[2]

