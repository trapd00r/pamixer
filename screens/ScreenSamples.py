
class ScreenSamples():

    def __init__(self):

        self.win = None
        self.windex = None
        self.wpreview = None

        return

    def layout(self, win):
        self.win = win

        win.refresh()

        # initial redraw
        self.redraw()

    def redraw(self, recurse = False):
        if self.win is None:
            return

        win = self.win

        win.erase()
        win.move(0, 0)

        samples = par.pa_samples
        for i in samples:
            win.addstr(samples[i].name + "\n")

        win.refresh()

        return

from ParCur import par