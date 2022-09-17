import imgToText


def pipeline(frame, coordinate):
    print('received frame of size', len(frame), 'and coordinates:', coordinate)

    # Extract the text at the target location
    print(imgToText.detect_text_swagger(frame))

    # Perform OCR

    # Perform translation

    # Perform text to speech

    # Profit
