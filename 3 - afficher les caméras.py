# -*- coding: UTF-8 -*-

import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
print "src_dir : " + src_dir

arch_dir = 'lib/x64' if sys.maxsize > 2**32 else 'lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
print "arch_dir : " + arch_dir

sys.path.insert(0, "lib")

import Leap
from Leap import *

import numpy
import ctypes

from PIL import Image


#################################################################################################

# Extrait les données brutes de l’image depuis la frame pour retourner une image 
def image_to_pil(self, leap_image):
	
	# extraction dans un tampon
	address = int(leap_image.data_pointer)
	ctype_array_def = ctypes.c_ubyte * leap_image.width * leap_image.height
	as_ctype_array = ctype_array_def.from_address(address)
	as_numpy_array = numpy.ctypeslib.as_array(as_ctype_array)
	buffer = numpy.reshape(as_numpy_array, (leap_image.height, leap_image.width))
	
	# création de l’image depuis le tampon
	pil_image = Image.fromarray(buffer, "L")
	pil_image = pil_image.convert("RGB")
	
	return pil_image

#################################################################################################

class MonListener(Leap.Listener):

	def on_frame(self, controller):
		frame = controller.frame()
	
		leap_imageGauche = frame.images[0]
		leap_imageDroite = frame.images[1]
		
		# on sort si on n’a pas pu récupérer les 2 images
		if not ( leap_imageGauche.is_valid and leap_imageDroite.is_valid ):
			return
	
		# préparation des images
		imageGauche = image_to_pil(self, leap_imageGauche)
		imageDroite = image_to_pil(self, leap_imageDroite)
		
		# concaténation des images gauche et droite des caméras
		L, H = imageGauche.size
		l, h = imageDroite.size

		imageComposee = Image.new('RGB', (L+l, H))
		imageComposee.paste(imageGauche, (0, 0, L, H))
		imageComposee.paste(imageDroite, (L, 0, L+l, h))

		# affichage et enregistrement de l'image composée
		imageComposee.show()
		imageNom = "Image_"+str(frame.id)+".png"
		imageComposee.save(imageNom)


#### fin class MonListener

#################################################################################################

def main():

	# création du contrôleur
	controleur = Leap.Controller()
	# on traite les frames même si l'application n'a pas le focus (nécessaire pour IDE, débogueur , etc)
	controleur.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)

	# on demande à avoir les images des caméras
	controleur.set_policy_flags(Leap.Controller.POLICY_IMAGES)

	# mise en place du listeneur qui traitera les frames
	listeneur = MonListener()
	controleur.add_listener(listeneur)

	print "ENTRÉE pour quitter"		
	sys.stdin.readline()

	controleur.remove_listener(listeneur)  

if __name__ == "__main__":
	main()
