import led

class sign(object):
    def __init__(self):
        self.full = led(11)
        self.high = led(13)
        self.nomask =  led(15)
        self.immask = led(16)
        self.okay = led(18)

    def fullErrorOn(self):
        self.full.light()

    def fullErrorOff():
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
        self.immask,.putout()

    def okayOn(self):
        self.okay.light()

    def okayOff(self):
        self.okay.putout()
