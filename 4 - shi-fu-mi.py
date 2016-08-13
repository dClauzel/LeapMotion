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

import time

#################################################################################################


class FocusListener(Leap.Listener):

	# suivi du coup joué
	coup = "vide"

	# compteur pour durée à maintenir pour valider le coup
	compteur = 0
	compteurMax = 3

	def on_init(self, controller):
		print "*** on_init"

	def on_connect(self, controller):
		print "*** on_connect"

	def on_disconnect(self, controller):
		# Note: not dispatched when running in a debugger.
		print "*** on_disconnect"

	def on_exit(self, controller):
		print "*** on_exit"

	def on_frame(self, controller):
		frame = controller.frame()


		
		# on ne traite que si une main est détectée
		if frame.hands.is_empty:
			return

		doigtsEtendus = frame.fingers.extended()
		
		# comptons les doigts présents
		nombreDeDoigts = 0
		for finger in doigtsEtendus:
			nombreDeDoigts = nombreDeDoigts + 1

		# On n'a pas encore joué ? On enregistre le coup
		# sinon, on regarde si le joueur confirme son coup durant X secondes
		if (self.coup == "vide"):
			self.coup = typeDeCoup(nombreDeDoigts)
			compteur = 1
			print "nouvelle idée de coup : " + self.coup
		else:
				if (self.compteur <= self.compteurMax):
					if (self.coup) == typeDeCoup(nombreDeDoigts): # le coup a changé ?
						print " " +str(self.compteurMax-self.compteur) + " " + typeDeCoup(nombreDeDoigts)
						self.compteur = self.compteur + 1
					else:
						self.coup = "vide"
						print "Je change d'avis"
						self.compteur = 0
					time.sleep(1)
				else:
					print "Je joue : " + typeDeCoup(nombreDeDoigts)
					self.coup = "vide"
					self.compteur = 0


#### fin class FocusListener

#################################################################################################

# Retourne le type de coup en fonction du nombre de doigts
# - pierre : 0 doigt
# - ciseaux : 2 doigts
# - feuille : 5 doigts
def typeDeCoup(nombreDeDoigts):
	return {
		0: "pierre",
		1: "vide",
		2: "ciseaux",
		3: "vide",
		4: "vide",
		5: "feuille"
	}[nombreDeDoigts]

#################################################################################################

def main():
	# Create a sample listener and controller
	listener = FocusListener()
	controller = Leap.Controller()
	
	# To get frames while your app isn't focused, you need to set the "background frames" policy
	# https://developer.leapmotion.com/documentation/python/api/Leap.Controller.html#Leap.Controller.set_policy_flags
	controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)

	controller.add_listener(listener)

	print "Press Enter to exit.." 
	sys.stdin.readline()

	controller.remove_listener(listener) 

if __name__ == "__main__":
	main()
