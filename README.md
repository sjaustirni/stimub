# Stimub

Script for connecting Brain-Computer Interface components with a stimulation hardware.

Possible Inputs:
 * `TCPInput`: String-based TCP packets (for instance, from OpenVibe or Unity)
 * `ConsoleInput`: Console input (Enter key) from user (useful for testing stimulation hardware)

Possible Stimulations:
 * `NiDAQTrigger`: NiDAQ hardware
 * `ConsoleTrigger`: useful for testing different inputs without access to NiDAQ hardware

## Examples
You can combine the inputs and stimulations as you wish:

```python
# Read events from OpenVibe and trigger console output
p = Proxy(TCPInput("127.0.0.1", 5679, "OVTK_GDF_Right"), ConsoleTrigger())
p.start()
```

```python
# Read events from console input and trigger NiDAQ
p = Proxy(ConsoleInput(), NiDAQTrigger(5, 0.002, 0.002, 3))
p.start()
```

```python
# Read events from Unity and trigger NiDAQ
p = Proxy(TCPInput("127.0.0.1", 5690, "MotorIntention"), NiDAQTrigger(5, 0.002, 0.002, 5))
p.start()
```

See `main.py` for more info.