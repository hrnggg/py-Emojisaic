from lib.image_generator import EmojiMosaicGenerator
import os
from PIL import Image

class GifMaker:
    def __init__(self, options={}):
        self.options = options
        self.filename = options["filename"]    
        self.generator = EmojiMosaicGenerator(options)

    def make_filenames(self):
        self.name = os.path.splitext(os.path.basename(self.filename))[0]
        self.new_files = []

    def make_emoji_gif(self):
        self.make_filenames()
        self.image = Image.open(self.filename)
        self.write_frames()
        for i, filename in enumerate(self.files):
            if not self.options["quiet"]:
                print("\nDoing frame {:3d}/{}".format(i + 1, len(self.files)))            
            self.new_files.append(self.generator.create_image(filename))
        self.write_gif()

    def write_gif(self):
        gif = []
        for i, filename in enumerate(self.new_files):
            new_frame = Image.open(filename)
            gif.append(new_frame)

        option_string = self.generator.get_option_string()
        new_filename = self.filename.replace(self.name, f'{self.name}-mosaic{option_string}')
        if not self.options["quiet"]:
            print(f"\nWriting to {new_filename}...")
        gif[0].save(new_filename, save_all=True, append_images=gif[1:], duration=self.image.info["duration"], loop=0)

    def write_frames(self):
        if not self.options["quiet"]:
            print("splitting gif into frames...\n")
        self.files = []
        for i in range(self.image.n_frames):
            self.image.seek(i)
            number = str(i).zfill(2)
            filename = f"tmp/{self.name}-{number}.png"
            self.image.save(filename)
            self.files.append(filename)
        print("splitting done.")



