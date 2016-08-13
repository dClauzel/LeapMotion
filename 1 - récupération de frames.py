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

    def on_init(self, controller):
        print "*** on_init"

    def on_connect(self, controller):
        print "*** on_connect"

    def on_disconnect(self, controller): # N'est pas appelé depuis le débogueur
        print "*** on_disconnect"

    def on_exit(self, controller):
        print "*** on_exit"

    # traitement de la frame
    def on_frame(self, controller):
        frame = controller.frame()
        print "Frame id : " + str(frame.id)

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