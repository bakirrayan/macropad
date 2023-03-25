import busio, terminalio, displayio, gc, board
import adafruit_displayio_ssd1306
from adafruit_display_text import label
from kmk.extensions import Extension


class OledDisplayMode:
    TXT = 0
    IMG = 1


class OledReactionType:
    STATIC = 0
    LAYER = 1


class OledData:
    def __init__(
        self,
        image=None,
        text=None,
    ):
        if image:
            self.data = [image]
        elif text:
            self.data = [text]


class Oled(Extension):
    def __init__(
        self,
        views,
        toDisplay=OledDisplayMode.TXT,
        oWidth=128,
        oHeight=64,
        flip: bool = False,
    ):
        displayio.release_displays()
        self.rotation = 180 if flip else 0
        self._views = views.data
        self._toDisplay = toDisplay
        self._width = oWidth
        self._height = oHeight
        self._prevLayers = 0
        gc.collect()

    def returnCurrectRenderText(self, layer, singleView):
        # for now we only have static things and react to layers. But when we react to battery % and wpm we can handle the logic here
        if singleView[0] == OledReactionType.STATIC:
            return singleView[1][0]
        if singleView[0] == OledReactionType.LAYER:
            return singleView[1][layer]

    def renderOledTextLayer(self, layer):
        splash = displayio.Group()
        splash.append(
            label.Label(
                terminalio.FONT,
                text=self.returnCurrectRenderText(layer, self._views[0]),
                color=0xFFFFFF,
                x=0,
                y=10,
            )
        )
        self._display.show(splash)
        gc.collect()

    def renderOledImgLayer(self, layer):
        splash = displayio.Group()
        odb = displayio.OnDiskBitmap(
            '/' + self.returnCurrectRenderText(layer, self._views[0])
        )
        image = displayio.TileGrid(odb, pixel_shader=odb.pixel_shader)
        splash.append(image)
        self._display.show(splash)
        gc.collect()

    def updateOLED(self, sandbox):
        if self._toDisplay == OledDisplayMode.TXT:
            self.renderOledTextLayer(sandbox.active_layers[0])
        if self._toDisplay == OledDisplayMode.IMG:
            self.renderOledImgLayer(sandbox.active_layers[0])
        gc.collect()

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, keyboard):
        displayio.release_displays()
        sda, scl = board.GP16, board.GP17
        i2c = busio.I2C(scl, sda)
        self._display = adafruit_displayio_ssd1306.SSD1306(
            displayio.I2CDisplay(i2c, device_address=0x3C),
            width=self._width,
            height=self._height,
            rotation=self.rotation,
        )
        if self._toDisplay == OledDisplayMode.TXT:
            self.renderOledTextLayer(0)
        if self._toDisplay == OledDisplayMode.IMG:
            self.renderOledImgLayer(0)
        return

    def before_matrix_scan(self, sandbox):
        if sandbox.active_layers[0] != self._prevLayers:
            self._prevLayers = sandbox.active_layers[0]
            self.updateOLED(sandbox)
        return

    def after_matrix_scan(self, sandbox):

        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return