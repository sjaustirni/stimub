from proxy import Proxy, TCPInput, ConsoleInput, ConsoleTrigger, NiDAQTrigger

if __name__ == "__main__":
    # Choose and/or adjust the wanted scenario.
    # For OpenVibe and Unity scenarios, make sure the corresponding software is running.
    # For NiDAQ scenarios, make sure the hardware is connected.

    # Read events from OpenVibe and trigger console output
    #p = Proxy(TCPInput("127.0.0.1", 5679, "OVTK_GDF_Right"), ConsoleTrigger())

    # Read events from console input and trigger NiDAQ
    #p = Proxy(ConsoleInput(), NiDAQTrigger(5, 0.002, 0.002, 3))

    # Read events from Unity and trigger NiDAQ
    p = Proxy(TCPInput("127.0.0.1", 5690, "MotorIntention"), NiDAQTrigger(5, 0.002, 0.002, 5))

    p.start()
