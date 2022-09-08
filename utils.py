import pygame
import configuration as C


def load_image(filename, width=None, height=None):

	img = pygame.image.load(str(C.ASSET_DIR / filename))

	if width and height:
		return pygame.transform.scale(img, (width, height))
	else:
		return img
