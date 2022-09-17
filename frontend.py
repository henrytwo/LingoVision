# This example requires the PySide2 library for displaying windows and video. Other such libraries are avaliable, and
# you are free to use whatever you'd like for your projects.
from PySide2 import QtCore, QtGui, QtWidgets
import adhawkapi
import eye_tracker
import math

MARKER_SIZE = 20  # Diameter in pixels of the gaze marker
MARKER_COLOR = (0, 250, 50)  # Colour of the gaze marker

class Interface(QtWidgets.QWidget):
    ''' Class for receiving and displaying the video stream '''

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('LingoVision')

        vbox = QtWidgets.QVBoxLayout()

        self.text_label = QtWidgets.QLabel('Q: run a Quick Start,  C: run a Calibration, SPACE: Capture text')
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)
        vbox.addWidget(self.text_label)

        # Qt code to create a label that can hold an image. We will use this label to hold successive images from the
        # video stream.
        self.live_text_label = QtWidgets.QLabel('Live Feed:')
        self.live_text_label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(self.live_text_label)
        self.image_label = QtWidgets.QLabel(self)
        vbox.addWidget(self.image_label)

        # Full frame that we're analyzing
        self.full_frame_text_label = QtWidgets.QLabel('Captured Frame:')
        self.full_frame_text_label.setAlignment(QtCore.Qt.AlignLeft)
        vbox.addWidget(self.full_frame_text_label)
        self.full_frame_label = QtWidgets.QLabel(self)
        vbox.addWidget(self.full_frame_label)

        self.setLayout(vbox)

        # A Quick Start tunes the scan range and frequency to best suit the user's eye and face shape, resulting in
        # better tracking data. For the best quality results in your application, you should also perform a calibration
        # before using gaze data.
        self.quickstart_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('q'), self)
        self.quickstart_shortcut.activated.connect(self.quickstart)

        # A calibration allows us to relate the measured gaze with the real world using a series of markers displayed
        # in known positions
        self.calibration_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('c'), self)
        self.calibration_shortcut.activated.connect(self.calibrate)

        # Initialize the gaze coordinates to dummy values for now
        self._gaze_coordinates = (0, 0)

        # Set this later
        self.tracker = None

    def set_capture_image(self, capture_image):
        # Start capture image and start translation sequence
        self.calibration_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('space'), self)
        self.calibration_shortcut.activated.connect(capture_image)

    def set_current_frame(self, frame, coordinates):
        # Create a new Qt pixmap and load the frame's data into it
        qt_img = QtGui.QPixmap()
        qt_img.loadFromData(frame, 'JPEG')

        # Draws the gaze marker on the new frame
        self._draw_gaze_marker(qt_img)

        # Sets the new image
        self.full_frame_label.setPixmap(qt_img)

    def closeEvent(self, event):
        '''
        Override of the window's close event. When the window closes, we want to ensure that we shut down the api
        properly.
        '''

        self.tracker.shutdown()
        super().closeEvent(event)

    @property
    def connected(self):
        ''' Property to allow the main loop to check whether the api is connected to a tracker '''
        return self.tracker.connected

    def quickstart(self):
        ''' Function to allow the main loop to invoke a Quick Start '''
        self.tracker.quickstart()

    def calibrate(self):
        ''' Function to allow the main loop to invoke a Calibration '''
        self.tracker.calibrate()

    def handle_video_stream(self, image_buf, coordinates):
        # Create a new Qt pixmap and load the frame's data into it
        qt_img = QtGui.QPixmap()
        qt_img.loadFromData(image_buf, 'JPEG')

        # Get the image's size. If self._frame_size has not yet been initialized, we set its values to the frame size.
        size = qt_img.size().toTuple()
        if size[0] != self.image_label.width() or size[1] != self.image_label.height():
            # Set the image label's size to the frame's size
            self.image_label.resize(size[0], size[1])

        self._gaze_coordinates = coordinates

        # Draws the gaze marker on the new frame
        self._draw_gaze_marker(qt_img)

        # Sets the new image
        self.image_label.setPixmap(qt_img)

    def _draw_gaze_marker(self, qt_img):
        if math.isnan(self._gaze_coordinates[0]) or math.isnan(self._gaze_coordinates[1]):
            return

        # Draws the gaze marker on the given frame image
        painter = QtGui.QPainter(qt_img)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(*MARKER_COLOR), QtCore.Qt.SolidPattern))
        painter.drawEllipse(QtCore.QRectF(self._gaze_coordinates[0] - MARKER_SIZE / 2,
                                          self._gaze_coordinates[1] - MARKER_SIZE / 2,
                                          MARKER_SIZE, MARKER_SIZE))
        painter.end()
