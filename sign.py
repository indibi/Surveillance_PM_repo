import led

class sign(object):
    def __init__(self):
        self.full = led.led(11)
        self.high = led.led(13)
        self.nomask =  led.led(15)
        self.immask = led.led(16)
        self.okay = led.led(19)

    def fullErrorOn(self):
        self.full.light()

    def fullErrorOff(self):
        self.full.putout()

    def highErrorOn(self):
        self.high.light()

    def highErrorOff(self):
        self.high.putout()

    def noMaskErrorOn(self):
        self.nomask.light()

    def noMaskErrorOff(self):
        self.nomask.putout()

    def imMaskErrorOn(self):
        self.immask.light()

    def imMaskErrorOff(self):
        self.immask.putout()

    def okayOn(self):
        self.okay.light()

    def okayOff(self):
        self.okay.putout()
