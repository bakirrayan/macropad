import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers
from kmk.handlers.sequences import simple_key_sequence
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
# transparent key
_______ = KC.TRNS
# csgo keys
pistole = KC.N2
gun = KC.N1
knife = KC.N3
# VS Code keys
NEXT = simple_key_sequence( ( KC.LCTL(no_release=True), KC.LALT(no_release=True), KC.UP, ) )


keyboard.keymap = [
    # csgo
    [   _______,   _______,   _______,   _______,
        NEXT,   gun,   pistole,   knife,
        KC.LSFT,   KC.q,   KC.w,   KC.r,
        KC.LCTL,   KC.a,   KC.s,   KC.d
    ],
    # VS Code
    [   KC.TAB,     KC.F1,     KC.F2,     KC.F3,
        KC.y,     KC.F4,     KC.F5,     KC.F6,
        KC.w,     KC.F7,   KC.F8,     KC.F9,
        _______,    _______,    _______,    _______
    ]
]

encoder_handler.map = [ # Layer 1
                        ((KC.VOLD, KC.VOLU, KC.MUTE), (KC.BRID, KC.BRIU, KC.TO(1)),),
                        # Layer 2
                        ((KC.VOLD, KC.VOLU, KC.MUTE), (_______, _______, KC.TO(0)),)]

if __name__ == '__main__':
    keyboard.go()
