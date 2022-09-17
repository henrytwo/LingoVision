import locate_text


def pipeline(frame, coordinate):
    print('received frame of size', len(frame), 'and coordinates:', coordinate)

    # Extract the text at the target location
    extracted_image = locate_text.locate_text(frame, coordinate)

    # Perform OCR

    # Perform translation

    # Perform text to speech

    # Profit