class Error(Exception):
    # base class for errors
    pass


class PaperContourError(Error):
    '''
    This error is raised when module detects
    only paper boundary as main contour.
    When to use?
    If no of contours detected after perspective transform is
    less than 4
    '''

    def __init__(self, message):
        self.message = message


class BubbleDetectionError(Error):
    '''
    This error is raised if after filtering out the countours
    the no of contours are < 240
    '''

    def __init__(self, message):
        self.message = message


class PaperDetectionError(Error):
    '''
    This error is detected when module fails to detect paper i.e. 
    the area with box.
    '''

    def __init__(self, message):
        self.message = message
