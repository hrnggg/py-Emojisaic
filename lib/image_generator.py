from lib.image_scanner import ImageScanner
from lib.emoji_finder import EmojiFinder
from lib.progress import ProgressBar
import os
from PIL import Image
import random 

class EmojiMosaicGenerator:
    def __init__(self, options={}):
        self.options = options
        self.__create_helpers()
        self.__set_quality()

    def create_image(self, filename):        
        self.name = os.path.splitext(os.path.basename(filename))[0]
        self.assign_images_and_pixel_map(filename)
        if not self.options["quiet"]:
            self.bar = ProgressBar(len(self.pixel_map), 'image generation')
        self.add_emojis_to_new_image()
        option_string = self.get_option_string()
        new_filename = filename.replace(self.name, f'{self.name}-mosaic{option_string}')
        if new_filename[-3:] != 'png': 
            self.new_image = self.new_image.convert("RGB")
        self.new_image.save(new_filename)
        return new_filename

    def assign_images_and_pixel_map(self, filename):
        self.image = Image.open(filename) 
        if self.image.mode == 'P' or self.image.mode == 'LA':
            self.image = self.image.convert('RGBA')
        width, height = self.image.size
        self.new_image = Image.new('RGBA', (width * self.zoom, height * self.zoom))            
        self.pixel_map = self.scanner.generate_pixel_map(self.image, self.emoji_size)

    def add_emojis_to_new_image(self):
        for pixel in self.pixel_map:
            pixel = self.__adjust_coordinates(pixel)            
            emoji = self.finder.closest_emoji(pixel)
            emoji = emoji.resize((self.emoji_size * self.zoom, self.emoji_size * self.zoom))
            self.put_pixels(emoji, pixel['x'], pixel['y'])
            if not self.options["quiet"]:
                self.bar.add(1)
    
    def put_pixels(self, emoji, x, y):
        for dy in range(emoji.size[1]):
            for dx in range(emoji.size[0]):  
                pixel = emoji.getpixel((dx, dy))              
                if self.is_valid_pixel(x + dx, y + dy):
                    self.new_image.putpixel((x + dx, y + dy), pixel)

    def is_valid_pixel(self, x, y):
        width, height = self.new_image.size
        return x < width and y < height
        
    def __adjust_coordinates(self, pixel):
        pixel['x'] *= self.zoom
        pixel['y'] *= self.zoom
        pixel = self.__randomize_offset(pixel)
        return pixel

    def __randomize_offset(self, pixel):
        offset = self.offset
        pixel['x'] += random.randint(-offset, offset)
        pixel['y'] += random.randint(-offset, offset)
        return pixel 

    def __create_helpers(self):
        self.scanner = ImageScanner(self.options)
        self.finder = EmojiFinder(self.options)

    def __set_quality(self):
        self.emoji_size = self.options["size"]
        self.zoom = self.options["zoom"]
        self.offset = self.options["offset"]
        self.coverage = self.options["coverage"]

    def get_option_string(self):
        s = ""
        if self.emoji_size != 8:
            s += f"_size-{self.emoji_size}"
        if self.zoom != 1:
            s += f"_zoom-{self.zoom}"
        if self.offset != 0:
            s += f"_offset-{self.offset}"
        if self.coverage != None:
            s += f"_coverage-{self.coverage}"
        return s
