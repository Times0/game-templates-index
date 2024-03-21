from . import chdefs
from . import pimodules
from . import glvars

pyv = pimodules.pyved_engine

# - alias
pygame = pyv.pygame
EngineEvTypes = pyv.EngineEvTypes
Button = pyv.gui.Button2

# - contsants
BGCOLOR = 'antiquewhite3'


def proc_start():
    pyv.get_ev_manager().post(EngineEvTypes.StatePush, state_ident=glvars.MyGameStates.Chessmatch)


class IntroCompo(pyv.EvListener):
    """
    main component for this game state
    """

    def _update_playertypes(self):
        chdefs.pltype1 = chdefs.OMEGA_PL_TYPES[self.idx_pl1]
        chdefs.pltype2 = chdefs.OMEGA_PL_TYPES[self.idx_pl2]
        self.pltypes_labels[0].text = chdefs.pltype1
        self.pltypes_labels[1].text = chdefs.pltype2

    def __init__(self):
        super().__init__()
        self.sent = False  # to avoid nasty bug in web ctx -> push event is triggered twice!

        # model
        self.idx_pl1 = 0
        self.idx_pl2 = 0

        # - v: labels
        # current sig is:
        # (position, text, txtsize=35, color=None, anchoring=ANCHOR_LEFT, debugmode=False)
        sw = pyv.get_surface().get_width()
        self.title = pyv.gui.Label(
            (-150 + (sw // 2), 100), 'The game of chess', txt_size=41, anchoring=pyv.gui.ANCHOR_CENTER
        )
        self.title.textsize = 122
        self.title.color = 'brown'

        self.pltypes_labels = [
            pyv.gui.Label((115, 145), 'unkno type p1', color='darkblue', txt_size=24),
            pyv.gui.Label((115, 205), 'unkno type p2', color='darkblue', txt_size=24),
        ]
        self._update_playertypes()

        # - v: buttons
        def rotatepl1():
            self.idx_pl1 = (self.idx_pl1 + 1) % len(chdefs.OMEGA_PL_TYPES)
            self._update_playertypes()

        def rotatepl2():
            self.idx_pl2 = (self.idx_pl2 + 1) % len(chdefs.OMEGA_PL_TYPES)
            self._update_playertypes()

        def rotleft_pl1():
            self.idx_pl1 = (self.idx_pl1 - 1)
            if self.idx_pl1 < 0:
                self.idx_pl1 = -1 + len(chdefs.OMEGA_PL_TYPES)
            self._update_playertypes()

        def rotleft_pl2():
            self.idx_pl2 = (self.idx_pl2 - 1)
            if self.idx_pl2 < 0:
                self.idx_pl2 = -1 + len(chdefs.OMEGA_PL_TYPES)
            self._update_playertypes()

        self.buttons = [
            Button(None, 'Start Chessmatch', (128, 256), callback=proc_start),
            Button(None, ' > ', (128 + 200 + 25, 140), callback=rotatepl1),
            Button(None, ' < ', (128 - 25 - 60, 140), callback=rotleft_pl1),
            Button(None, ' > ', (128 + 200 + 25, 200), callback=rotatepl2),
            Button(None, ' < ', (128 - 25 - 60, 200), callback=rotleft_pl2),
        ]

        for b in self.buttons:
            b.set_debug_flag()

    def turn_on(self):
        super().turn_on()
        for b in self.buttons:
            b.set_active()

    def turn_off(self):
        super().turn_off()
        for b in self.buttons:
            b.set_active(False)

    def on_paint(self, ev):
        ev.screen.fill('orange')

        # self.title.draw()
        # for lab in self.pltypes_labels:
        #     lab.draw()
        # for b in self.buttons:
        #     b.draw()

    def on_keydown(self, ev):
        if ev.key == pygame.K_ESCAPE:
            pyv.vars.gameover = True

    def on_mousedown(self, ev):
        if not self.sent:
            self.sent = True
            pyv.get_ev_manager().post(EngineEvTypes.StatePush, state_ident=glvars.MyGameStates.CompeteNow)


class ChessintroState(pyv.BaseGameState):
    """
    Goal : that game state will show 1 out of 3 infos:
    - user not auth, you need to auth
    - user auth + CR balance + your best score so far <+> You cannot try again
    - user auth + CR balance + your best score so far <+> Trying will cost you xx CR, click to continue
    """

    def __init__(self, ident):
        super().__init__(ident)
        self.icompo = None

    def enter(self):
        self.icompo = IntroCompo()
        self.icompo.turn_on()

    def resume(self):
        self.icompo.turn_on()

    def release(self):
        self.icompo.turn_off()

    def pause(self):
        self.icompo.turn_off()
