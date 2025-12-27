from pyladdersim.components import Contact, InvertedContact, Output, OnDelayTimer
from pyladdersim.ladder import Rung, Ladder
from pyladdersim.visualizer import LadderVisualizer

# Define components
input1 = Contact(name="Start")
input2 = InvertedContact(name="Stop")
output = Output(name="Lamp")

# Create a rung and add components
rung1 = Rung([input1, input2, output])

# Initialize the ladder and add rungs
ladder = Ladder()
ladder.add_rung(rung1)

# Run the ladder with visualization
ladder.run(visualize=True)