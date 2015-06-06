import os
import sys
import inspect
import platform

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap

MY_SYSTEM = platform.system()


class FunctionsHelper:
    def __init__(self):
        if MY_SYSTEM == 'Windows':
            self.lock_screen = self.lock_screen_windows
        elif MY_SYSTEM == 'Linux':
            self.lock_screen = self.lock_screen_linux
        else:
            self.lock_screen = self.unimplemented

    def unimplemented(self):
        raise NotImplementedError()

    def lock_screen_windows(self):
        import ctypes
        ctypes.windll.user32.LockWorkStation()

    def lock_screen_linux(self):
        raise NotImplementedError('Function lock_screen_linux is not implemented yet')


class GestureListener(Leap.Listener):
    last_swipe_id = 0

    def __init__(self, *args, **kwargs):
        super(GestureListener, self).__init__(*args, **kwargs)
        self.helper = FunctionsHelper()

    def on_connect(self, controller):
        print 'Connected'
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    def on_frame(self, controller):
        frame = controller.frame()
        swipe_count = 0
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = Leap.SwipeGesture(gesture)
                swipe_count += 1
                print 'SWIPE: %d' % swipe.id
                self.helper.lock_screen()


def main():
    controller = Leap.Controller()
    gesture_listener = GestureListener()
    controller.add_listener(gesture_listener)

    print 'Press Enter to quit...'
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(gesture_listener)

if __name__ == '__main__':
    main()
