import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers
from kmk.extensions.media_keys import MediaKeys
from oled import Oled,OledDisplayMode,OledReactionType,OledData


print("Starting")

keyboard = KMKKeyboard()

encoder_handler = EncoderHandler()
media_keys = MediaKeys()
layers_ext = Layers()

keyboard.modules = [encoder_handler, media_keys, layers_ext]

oled_display_data=OledData(text={0:OledReactionType.LAYER,1:["Layer ==> 0","Layer ==> 1"]})

oled_ext = Oled(oled_display_data,toDisplay=OledDisplayMode.TXT,flip=False)

keyboard.extensions.append(oled_ext)

keyboard.col_pins = (board.GP8, board.GP9, board.GP10, board.GP11)
keyboard.row_pins = (board.GP12, board.GP13, board.GP14, board.GP15)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

encoder_handler.pins = ((board.GP6, board.GP7, board.GP5, False),
                        (board.GP3, board.GP4, board.GP2, False),)

_______ = KC.TRNS

keyboard.keymap = [
    # Layer 1
    [   KC.a,   KC.B,   KC.C,   KC.D,
        KC.e,   KC.f,   KC.g,   KC.h,
        KC.i,   KC.j,   KC.k,   KC.l,
        KC.m,   KC.n,   KC.o,   _______
    ],
    # Layer 2
    [   KC.z,     KC.F2,     KC.F18,     _______,
        KC.y,     KC.F17,     KC.F19,     _______,
        KC.w,     _______,   KC.F20,     _______,
        _______,    _______,    _______,    _______
    ]
]

encoder_handler.map = [ # Layer 1
                        ((KC.VOLD, KC.VOLU, KC.MUTE), (KC.BRID, KC.BRIU, KC.TO(1)),),
                        # Layer 2
                        ((KC.VOLD, KC.VOLU, KC.MUTE), (_______, _______, KC.TO(0)),)]

if __name__ == '__main__':
    keyboard.go()
