from PIL import Image
import os

source_dir = "Pola_att"
output_dir = "Pola_jpg"
max_size = 299

if __name__ == '__main__':

	for prod in os.listdir(source_dir):
		if prod.startswith('.'):
			continue

		print prod

		for pic in os.listdir(os.path.join(source_dir,prod)):
			if pic.startswith('.'):
				continue

			print pic

			im = Image.open(os.path.join(source_dir, prod, pic))
			if im.height > im.width:
				height = max_size
				width = max_size * im.width/im.height
			else:
				width = max_size
				height = max_size * im.height/im.width
			jpg = im.resize((width, height))
			if jpg.mode != 'RGB':
				jpg = jpg.convert('RGB')

			pic = os.path.splitext(pic)[0] + '.jpg'

			dir = os.path.join(output_dir,prod)
			if not os.path.exists(dir):
				os.makedirs(dir)

			jpg.save(os.path.join(output_dir,prod,pic))