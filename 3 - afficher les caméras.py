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

from PIL import Image

#################################################################################################

class MonListener(Leap.Listener):

	def on_frame(self, controller):
		frame = controller.frame()
	
		leap_imageGauche = frame.images[0]
		leap_imageDroite = frame.images[1]

		# collecte des données de la caméra gauche
		bImage = bytearray(leap_imageGauche.width * leap_imageGauche.height)
		for d in range(0, leap_imageGauche.width * leap_imageGauche.height - 1):
			bImage[d] = leap_imageGauche.data[d]

		# transformation en image
		imageGauche = Image.frombytes("L", (leap_imageGauche.width,  leap_imageGauche.height), buffer(bImage))

		# collecte des données de la caméra droite
		bImage = bytearray(leap_imageDroite.width * leap_imageDroite.height)
		for d in range(0, leap_imageDroite.width * leap_imageDroite.height - 1):
			bImage[d] = leap_imageDroite.data[d]
	
		# transformation en image
		imageDroite = Image.frombytes("L", (leap_imageGauche.width,  leap_imageGauche.height), buffer(bImage))
		
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
	controller = Leap.Controller()

	# on traite les frames même si l'application n'a pas le focus (nécessaire pour IDE, débogueur , etc)
	controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)

	# on demande à avoir les images des caméras
	controller.set_policy_flags(Leap.Controller.POLICY_IMAGES)

	# mise en place du listeneur qui traitera les frames
	listeneur = MonListener()
	controller.add_listener(listeneur)

	print "ENTRÉE pour quitter"        
	sys.stdin.readline()

	controller.remove_listener(listener)  

if __name__ == "__main__":
	main()
