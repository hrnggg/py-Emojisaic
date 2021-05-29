from lib.progress import ProgressBar

class ImageScanner:
	def __init__(self, options):		
		self.options = options
		self.bar = None

	def generate_pixel_map(self, image, emoji_size):
		self.image = image 
		self.emoji_size = emoji_size
		self.pixels = []
		self.x = 0
		self.y = 0
		self.scan_image()	
		return self.pixels	

	def average_colors_for_area(self):
		colors = {'r': 0, 'g': 0, 'b': 0}
		total = 0
		for dy in range(self.emoji_size):
			ny = self.y + dy
			for dx in range(self.emoji_size):
				nx = self.x + dx		
				if not self.is_valid_pixel(nx, ny):
					continue
				total += 1
				results = self.get_pixel_colors(nx, ny)
				colors = self.add_results_to_tally(results, colors)
		return self.create_pixel_struct(colors, total)

	def is_valid_pixel(self, x, y):
		width, height = self.image.size
		return x < width and y < height

	def create_pixel_struct(self, colors, total):
		div = self.divide_pixels(colors, total)
		return {'x': self.x, 'y': self.y, 'r': div['r'], 'g': div['g'], 'b': div['b']}

	def add_results_to_tally(self, results, colors):
		colors['r'] += results['r']
		colors['g'] += results['g']
		colors['b'] += results['b']		
		return colors

	def scan_image(self):
		width, height = self.image.size
		while self.y < height:			
			while self.x < width:
				self.pixels.append(self.average_colors_for_area())
				self.x += self.emoji_size 
			self.x = 0
			self.y += self.emoji_size
			if not self.options["quiet"]:
				self.update()

	def divide_pixels(self, colors, total):
		return {
			'r': colors['r'] // total,		
			'g': colors['g'] // total,		
			'b': colors['b'] // total,
		}

	def get_pixel_colors(self, x, y):
		pixel = self.image.getpixel((x, y))
		return {'r': pixel[0], 'g': pixel[1], 'b': pixel[2]}

	def update(self):
		if self.bar is None:
			self.bar = ProgressBar(self.image.size[1], 'image scanning')
		self.bar.set(self.y)		