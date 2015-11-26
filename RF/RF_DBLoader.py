from entities import *
from components.entityInterfaces import *

interface = EntityInterfaces()

# Button 1
button = interface.addButton("Staircase Light");
button.addCommand("On", style = "success", codes = [5248307])
command_off = button.addCommand("Off", style = "danger", codes = [5248316])
button.save()
command_off.setAsAutoLightDisable()
button.save()

# Button 2
button = interface.addButton("Couch Light");
command_on = button.addCommand("On", style = "success", codes = [5248451])
command_off = button.addCommand("Off", style = "danger", codes = [5248460])
button.save()
command_on.setAsAutoLightEnable()
command_off.setAsAutoLightDisable()
button.save()

# Button 3
button = interface.addButton("Button 3", visible = False);
button.addCommand("On", style = "success", codes = [5248731])
button.addCommand("Off", style = "danger", codes = [5248780])
button.save()