'''
Display a gaze marker on the camera/scene video. Demonstrates how to receive frames from the camera, map gaze data onto
a camera frame, and draw a gaze marker.

Courtesy of: https://github.com/adhawkmicrosystems/python-sdk-examples/tree/master/camera_gaze
'''

import math
import sys

import adhawkapi
import adhawkapi.frontend
from adhawkapi import MarkerSequenceMode, PacketType


class EyeTracker:
    ''' Frontend communicating with the backend '''

    def __init__(self):

        self.current_frame = None
        self.handle_external_video_stream = None

        # Instantiate and start a video receiver with self._handle_video_stream as the handler for new frames
        # Stores the video receiver's address
        self._video_receiver = adhawkapi.frontend.VideoReceiver()
        self._video_receiver.frame_received_event.add_callback(self.handle_video_stream)
        self._video_receiver.start()
        self._video_receiver_address = self._video_receiver.address

        # Instantiate an API object
        self._api = adhawkapi.frontend.FrontendApi()

        # Tell the api that we wish to tap into the GAZE_IN_IMAGE data stream with the given callback as the handler
        self._api.register_stream_handler(PacketType.GAZE_IN_IMAGE, self.handle_gaze_in_image_stream)

        # Start the api and set its connection callback to self._handle_connect. When the api detects a connection to a
        # tracker, this function will be run.
        self._api.start(connect_cb=self._handle_connect_response)

        # Flags the frontend as not connected yet
        self.connected = False

        self._gaze_coordinates = None

    def handle_video_stream(self, _gaze_timestamp, _frame_index, image_buf, _frame_timestamp):
        self.current_frame = image_buf

        # Update the UI
        self.handle_external_video_stream(image_buf, self.gaze_coordinates)

    def handle_gaze_in_image_stream(self, _timestamp, gaze_img_x, gaze_img_y, *_args):
        # Updates the gaze marker coordinates with new gaze data. It is possible to receive NaN from the api, so we
        # filter the input accordingly.
        self.gaze_coordinates = [gaze_img_x, gaze_img_y]

    def shutdown(self):
        ''' Shuts down the backend connection '''

        # Stops the video stream
        self._api.stop_video_stream(*self._video_receiver_address, lambda *_args: None)

        # Stops api camera capture
        self._api.stop_camera_capture(lambda *_args: None)

        # Stop the log session
        self._api.stop_log_session(lambda *_args: None)

        # Shuts down the api
        self._api.shutdown()

    def quickstart(self):
        ''' Runs a Quick Start using AdHawk Backend's GUI '''

        # The tracker's camera will need to be running to detect the marker that the Quick Start procedure will display
        self._api.quick_start_gui(mode=MarkerSequenceMode.FIXED_GAZE, marker_size_mm=35,
                                  callback=(lambda *_args: None))

    def calibrate(self):
        ''' Runs a Calibration using AdHawk Backend's GUI '''

        # Two calibration modes are supported: FIXED_HEAD and FIXED_GAZE
        # With fixed head mode you look at calibration markers without moving your head
        # With fixed gaze mode you keep looking at a central point and move your head as instructed during calibration.
        self._api.start_calibration_gui(mode=MarkerSequenceMode.FIXED_HEAD, n_points=9, marker_size_mm=35,
                                        randomize=False, callback=(lambda *_args: None))

    def _handle_connect_response(self, error):

        # Starts the camera and sets the stream rate
        if not error:
            # Sets the GAZE_IN_IMAGE data stream rate to 125Hz
            self._api.set_stream_control(PacketType.GAZE_IN_IMAGE, 125, callback=(lambda *args: None))

            # Starts the tracker's camera so that video can be captured and sets self._handle_camera_start_response as
            # the callback. This function will be called once the api has finished starting the camera.
            self._api.start_camera_capture(camera_index=0, resolution_index=adhawkapi.CameraResolution.MEDIUM,
                                           correct_distortion=False, callback=self._handle_camera_start_response)

            # Starts a logging session which saves eye tracking signals. This can be very useful for troubleshooting
            self._api.start_log_session(log_mode=adhawkapi.LogMode.BASIC, callback=lambda *args: None)

            # Flags the frontend as connected
            self.connected = True

    def _handle_camera_start_response(self, error):

        # Handles the response after starting the tracker's camera
        if error:
            # End the program if there is a camera error
            print(f'Camera start error: {error}')
            self.shutdown()
            sys.exit()
        else:
            # Otherwise, starts the video stream, streaming to the address of the video receiver
            self._api.start_video_stream(*self._video_receiver_address, lambda *_args: None)
