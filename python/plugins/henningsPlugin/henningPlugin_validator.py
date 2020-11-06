from PyQt5.QtGui import QValidator
import os

class PathValidator(QValidator):

    def __init__(self, parent=None):
        super(PathValidator, self).__init__(parent)

    def validate(self, path, pos):
        if path:
            if os.path.exists(path):
                return (QValidator.Acceptable, path, pos)
            else:
                return (QValidator.Intermediate, path, pos)
        else:
            return (QValidator.Intermediate, path, pos)