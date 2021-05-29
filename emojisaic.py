from lib.emoji_scanner import EmojiScanner
from lib.image_generator import EmojiMosaicGenerator
from lib.gifmaker import GifMaker
import json
import glob
import shutil
import os
import click

@click.command()
@click.option('-g', '--gif', help='gif filename')
@click.option('-i', '--image', help='still image filename')
@click.option('-s', '--size', type=int, default=8, help='emoji height in pixels (default: 8)', )
@click.option('-z', '--zoom', type=int, default=1, help='multiply size of original image by this (default: 1)')
@click.option('-o', '--offset', type=int, default=0, help='random offset for emoji placement, in pixels (default: 0)')
@click.option('-c', '--coverage', type=int, default=None, help='emoji offset for pixel coverage (see docs, it is complicated)')
@click.option('-q', '--quiet', is_flag=True, help='be quiet! no output in this mode')
@click.option('-t', '--tmp', is_flag=True, help='remove all temp files (use by itself)')
@click.option('-m', '--mapping', is_flag=True, help='generate new emoji color map (use by itself)')
def cmd(gif, image, size, zoom, offset, coverage, quiet, tmp, mapping):
	options_hash = dict(
		filename=get_filename(gif, image),
		size=size, 
		zoom=zoom,
		offset=offset,
		coverage=coverage,
		quiet=quiet	
		)
	if tmp:
		clear_temp_files()
	elif mapping:
		generate_emoji_map()
	elif gif:		
		generate_emoji_gif(options_hash)
	elif image:
		generate_still_image(options_hash)
	else:
		print("Error:")
		print("at least one of these are mandatory:")
		print("    -g, --gif TEXT      gif filename")
		print("    -i, --image TEXT    still image filename")
		print("    -t, --tmp           remove all temp files (use by itself)")
		print("    -m, --mapping       generate new emoji color map (use by itself)")

def generate_emoji_map():
	with open('lib/map.json', 'w') as f:		
		json.dump(dict(), f, indent=4)

	image_files = sorted(glob.glob("emojis/*.png"))
	for file in image_files:	
		emoji_scanner = EmojiScanner(file)
		emoji_scanner.write()

def clear_temp_files():
	print("Removing all files in tmp folder...")
	shutil.rmtree('tmp')
	os.mkdir('tmp')

def generate_emoji_gif(options):
	gif_maker = GifMaker(options)
	gif_maker.make_emoji_gif()

def generate_still_image(options):
	generator = EmojiMosaicGenerator(options)
	generator.create_image(options["filename"])

def get_filename(gif, image):
	if gif:
		return gif 
	elif image:
		return image
	else:
		return None

def main():	
	cmd()

if __name__ == "__main__":
	main()