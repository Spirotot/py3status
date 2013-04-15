from datetime import timedelta
from gi.repository import Notify
from time import time

POMO       = 1500  # 60 * 25
SHORT_REST = 300   # 60 * 5
LONG_REST  = 1800  # 60 * 30
NB_REST    = 4


class Py3status:
    """
    Pomodoro method
    """
    pomo = POMO
    rest = SHORT_REST
    nb_rest = NB_REST

    def pomodoro(self, json, i3status_config):
        """
        This function will update a timer in the i3status bar for 25 minutes,
        then print a red "Break time" message for 5 minutes.
        """
        if not self.pomo:
            self.rest -= 1
            timer = self.rest
            self.full_text = 'Break time'
            color = 'color_bad'
        else:
            self.pomo -= 1
            timer = self.pomo
            self.full_text = 'Pomodoro'
            color = 'color_degraded'

        if not timer:
            # Pomodoro or Rest is finished, send notification
            self.send_notification()

        response = {
            'cached_until' : time(),
            'color': i3status_config[color],
            'self.full_text': '{}: {}'.format(
                self.full_text, str(timedelta(seconds=timer))[2:]),
            'name': 'pomodoro',
        }

        return (0, response)

    def send_notification(self):
        """
        :Requirements: libnotify, python-gobject
        """

        Notify.init('Pomodoro')
        notification = Notify.Notification.new (
            '<b>Attention:</b>',
            '{} is finished'.format(self.full_text),
            'dialog-information',
        )
        notification.show()

        if not self.rest:
            # Rest is finished, reinitialize data
            self.nb_rest -= 1
            self.pomo = POMO
            self.rest = SHORT_REST

        if not self.nb_rest:
            # Number of small rest reached, go for long rest
            self.rest = LONG_REST
            self.nb_rest = NB_REST
