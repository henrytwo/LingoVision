# This example requires the PySide2 library for displaying windows and video. Other such libraries are avaliable, and
# you are free to use whatever you'd like for your projects.
from PySide2 import QtCore, QtGui, QtWidgets
import sys
import frontend
import adhawkapi
import eye_tracker

def main():
    '''Main function'''

    tracker = eye_tracker.EyeTracker()

    app = QtWidgets.QApplication(sys.argv)

    # Instantiate a Frontend object. We give it the address of the video receiver, so the api's video stream will
    # be sent to it.
    ui = frontend.Interface()

    # Okay this is so sketchy but it's literally 5:21 am okay
    def capture_image():
        print(tracker.current_frame, tracker.gaze_coordinates)

        ui.set_current_frame(tracker.current_frame, tracker.gaze_coordinates)

    ui.set_capture_image(capture_image)

    ui.tracker = tracker
    ui.capture_image = capture_image
    tracker.handle_external_video_stream = ui.handle_video_stream

    try:
        print('Plug in your tracker and ensure AdHawk Backend is running.')
        while not ui.connected:
            pass  # Waits for the frontend to be connected before proceeding
    except (KeyboardInterrupt, SystemExit):
        ui.close()
        # Allows the frontend to be shut down robustly on a keyboard interrupt

    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
