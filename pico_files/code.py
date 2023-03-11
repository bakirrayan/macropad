import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys

print("Starting")

keyboard = KMKKeyboard()

encoder_handler = EncoderHandler()
media_keys = MediaKeys()
keyboard.modules = [encoder_handler, media_keys]

keyboard.col_pins = (board.GP8, board.GP9, board.GP10, board.GP11)
keyboard.row_pins = (board.GP12, board.GP13, board.GP14, board.GP15)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

encoder_handler.pins = ((board.GP6, board.GP7, board.GP5, False),
                        (board.GP3, board.GP4, board.GP2, False),)

keyboard.keymap = [
    [   KC.a,   KC.B,   KC.C,   KC.D,
        KC.e,   KC.f,   KC.g,   KC.h,
        KC.i,   KC.j,   KC.k,   KC.l,
        KC.m,   KC.n,   KC.o,   KC.p]
]

encoder_handler.map = [((KC.VOLU, KC.VOLD, KC.MUTE), (KC.VOLU, KC.VOLD, KC.MUTE),)]

if __name__ == '__main__':
    keyboard.go()
