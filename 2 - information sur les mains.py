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

#################################################################################################

class MonListener(Leap.Listener):


	doigts_noms = ['pouce', 'index', 'majeur', 'annulaire', 'auriculaire']
	os_noms = ['métacarpe', 'proximale', 'intermédiaire', 'distale']
	etats_noms = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

	def on_init(self, controller):
		print "*** on_init"

	def on_connect(self, controller):
		print "*** on_connect"

		# activation du suivi des gestes
		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self, controller):
		# Note: not dispatched when running in a debugger.
		print "*** on_disconnect"

	def on_exit(self, controller):
		print "*** on_exit"

	def on_frame(self, controller):
		frame = controller.frame()

		print "Frame id: %d, timestamp : %d, mains : %d, doigts : %d" % (
			frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

		# Get hands
		for hand in frame.hands:

			handType = "Main gauche" if hand.is_left else "Main droite"

			print "\t%s, id %d, position: %s" % (
				handType, hand.id, hand.palm_position)

			# Get the hand's normal vector and direction
			normal = hand.palm_normal
			direction = hand.direction

			# Calculate the hand's pitch, roll, and yaw angles
			print "\tTangage : %f°, roulis : %f°, lacet : %f°" % (
				direction.pitch * Leap.RAD_TO_DEG,
				normal.roll * Leap.RAD_TO_DEG,
				direction.yaw * Leap.RAD_TO_DEG)

			# Get arm bone
			arm = hand.arm
			print "\tDirection du bras : %s, position du poignet : %s, position du coude : %s" % (
				arm.direction,
				arm.wrist_position,
				arm.elbow_position)

			# Get fingers
			for finger in hand.fingers:

				print "\t\tdoigt : %s, id : %d, longueur : %f mm, largeur : %f mm" % (
					self.doigts_noms[finger.type],
					finger.id,
					finger.length,
					finger.width)

				# Get bones
				for b in range(0, 4):
					bone = finger.bone(b)
					print "\t\t\tos : %s, début : %s, fin : %s, direction: %s" % (
						self.os_noms[bone.type],
						bone.prev_joint,
						bone.next_joint,
						bone.direction)

		# Get tools
		for tool in frame.tools:

			print "\tOutil id : %d, position : %s, direction : %s" % (
				tool.id, tool.tip_position, tool.direction)

		# Get gestures
		for gesture in frame.gestures():
			if gesture.type == Leap.Gesture.TYPE_CIRCLE:
				circle = CircleGesture(gesture)

				# Determine clock direction using the angle between the pointable and the circle normal
				if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
					clockwiseness = "horaire"
				else:
					clockwiseness = "trigonométrique"

				# Calculate the angle swept since the last frame
				swept_angle = 0
				if circle.state != Leap.Gesture.STATE_START:
					previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
					swept_angle = (circle.progress - previous_update.progress) * 2 * Leap.PI

				print "\tCercle id : %d, %s, progression: %f, rayon : %f, changement d'angle : %f°, sens %s" % (
						gesture.id, self.etats_noms[gesture.state],
						circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

			if gesture.type == Leap.Gesture.TYPE_SWIPE:
				swipe = SwipeGesture(gesture)
				print "\tBalayage id : %d, état : %s, position : %s, direction : %s, vitesse : %f" % (
						gesture.id, self.etats_noms[gesture.state],
						swipe.position, swipe.direction, swipe.speed)

			if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
				keytap = KeyTapGesture(gesture)
				print "\tFrappe doigt id : %d, %s, position : %s, direction : %s" % (
						gesture.id, self.etats_noms[gesture.state],
						keytap.position, keytap.direction )

			if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
				screentap = ScreenTapGesture(gesture)
				print "\tFrappe écran id : %d, %s, position : %s, direction : %s" % (
						gesture.id, self.etats_noms[gesture.state],
						screentap.position, screentap.direction )

		if not (frame.hands.is_empty and frame.gestures().is_empty):
			print ""

	def state_string(self, state):
		if state == Leap.Gesture.STATE_START:
			return "STATE_START"

		if state == Leap.Gesture.STATE_UPDATE:
			return "STATE_UPDATE"

		if state == Leap.Gesture.STATE_STOP:
			return "STATE_STOP"

		if state == Leap.Gesture.STATE_INVALID:
			return "STATE_INVALID"

#### fin class MonListener

#################################################################################################

def main():

    # création du contrôleur
    controller = Leap.Controller()
    # on traite les frames même si l'application n'a pas le focus (nécessaire pour IDE, débogueur , etc)
    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    # mise en place du listeneur qui traitera les frames
    listeneur = MonListener()
    controller.add_listener(listeneur)

    while (1):
        listeneur.on_frame(controller)

if __name__ == "__main__":
	main()
