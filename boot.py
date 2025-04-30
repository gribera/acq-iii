import board
import digitalio
import storage

# Para Metro M0/M4 Express, ItsyBitsy M0/M4 Express
switch = digitalio.DigitalInOut(board.D12)

switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# Si la entrada "switch" esta conectada a Gnd, el programa en CircuitPython
# puede escribir archivos en el FileSystem del board
storage.remount("/", readonly=switch.value)
