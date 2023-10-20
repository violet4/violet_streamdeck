import subprocess
import threading
import time

#import alsaaudio

from vsdlib.widgets import Widget
from vsdlib.buttons import Button
from vsdlib.button_style import ButtonStyle
from vsdlib.board import Board

from utils import get_asset_path


# class VolumeWidget(Widget):
#     increase_volume_button: Button
#     decrease_volume_button: Button
#     display_volume_button: Button
#     muted: bool
#     volume: str
#     mixer: alsaaudio.Mixer
#     _thread: threading.Thread
#     def __init__(self, board:Board, style:ButtonStyle=ButtonStyle()):
#         super().__init__(board, style)
#         self.mixer = alsaaudio.Mixer()
#         self.volume = self.get_current_volume()
#         self.muted = self.getmute()
#         self.display_volume_button = Button(self.create_mute_fn(), style=style)
#         self.set_volume_str()
#         self.increase_volume_button = Button(
#             self.create_change_volume_fn(self.display_volume_button),
#             text="Vol+", style=style
#         )
#         self.decrease_volume_button = Button(
#             self.create_change_volume_fn(self.display_volume_button, decrease=True),
#             text="Vol-", style=style
#         )
#         self._thread = threading.Thread(target=self.watch_volume, daemon=True)
#         self._thread.start()

#     def watch_volume(self):
#         pactl = subprocess.Popen(['pactl', 'subscribe'], stdout=subprocess.PIPE)
#         sink_events = subprocess.Popen(['grep', '--line-buffered', 'sink'], stdin=pactl.stdout, stdout=subprocess.PIPE)
#         last_volume = 0
#         last_muted = 0
#         while True:
#             line = None
#             if sink_events.stdout is not None:
#                 line = sink_events.stdout.readline()
#             if not line:
#                 time.sleep(0.1)
#                 continue
#             volume = self.get_current_volume()
#             muted = self.getmute()
#             if volume == last_volume and muted == last_muted:
#                 continue
#             last_volume = volume
#             last_muted = muted
#             self.set_volume_str(volume, muted)


#     def set_volume_str(self, volume=None, muted=None):
#         if volume is None:
#             volume = self.get_current_volume()
#         volume = f'{volume}%'

#         if muted is None:
#             muted = self.getmute()

#         text = f'muted\n({volume})' if muted else volume
#         self.display_volume_button.set(text=text)

#     def create_mute_fn(self):
#         def toggle_mute(pressed):
#             if not pressed:
#                 return
#             self.muted = not self.muted
#             self.mixer.setmute(1 if self.muted else 0)
#             self.set_volume_str(muted=self.muted)
#         return toggle_mute


#     def create_change_volume_fn(self, display_volume_button:Button, decrease:bool=False):
#         def change_volume(pressed):
#             if not pressed:
#                 return
#             char = '-' if decrease else '+'
#             subprocess.check_output(
#                 f"amixer set 'Master' 5%{char} | grep Right --color=never | tail -1|cut -d'[' -f2|cut -d']' -f1",
#                 shell=True,
#             ).decode().strip()
#             self.set_volume_str()
#         return change_volume

#     @staticmethod
#     def is_muted():
#         value = subprocess.check_output(
#             f"amixer set 'Master' 0%- | grep Right --color=never | tail -1",
#             shell=True,
#         ).decode().strip()
#         return '[off]' in value

#     def get_current_volume(self):
#         while self.mixer.handleevents():
#             pass
#         return self.mixer.getvolume()[0]

#     def getmute(self):
#         return self.is_muted()
#         # while self.mixer.handleevents():
#         #     pass
#         # mute = bool(self.mixer.getmute()[0])
#         # print("mute", mute)
#         # return mute


class BrightnessWidget(Widget):
    brightness_display_button: Button
    brightness_up_button: Button
    brightness_down_button: Button

    _min_brightness:int = 10
    _max_brightness:int = 100

    def __init__(self, board:Board, style:ButtonStyle=ButtonStyle()):
        super().__init__(board, style)
        self.brightness_display_button = Button(style=style)
        self.set_brightness_str()
        self.brightness_up_button = Button(
            self.make_change_brightness_up_callback(),
            text='Lite+', style=ButtonStyle(image_path=get_asset_path('lightbulb_on.jpg')),
        )
        self.brightness_down_button = Button(
            self.make_change_brightness_down_callback(),
            text='Lite-', style=ButtonStyle(image_path=get_asset_path('lightbulb_off.jpg')),
        )

    def set_brightness_str(self):
        self.brightness_display_button.set(text=f'{self.board.brightness}\nTODO\nsleep\nmode')

    def get_brightness(self):
        return self.board.brightness

    def make_change_brightness_callback(self, diff:int):
        def change_brightness(pressed:bool):
            if pressed:
                self.change_brightness(diff)
                self.set_brightness_str()
        return change_brightness

    def change_brightness(self, diff: int):

        self.board.brightness += diff
        if self.board.brightness < self._min_brightness:
            self.board.brightness = self._min_brightness
        elif self.board.brightness > self._max_brightness:
            self.board.brightness = self._max_brightness
        self.board.sd.set_brightness(self.board.brightness)
        return self.board.brightness

    def make_change_brightness_up_callback(self):
        return self.make_change_brightness_callback(10)

    def make_change_brightness_down_callback(self):
        return self.make_change_brightness_callback(-10)
