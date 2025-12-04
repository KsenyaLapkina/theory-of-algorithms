class MemeGeneratorError(Exception):
    """Базовое исключение для генератора мемов."""
    pass

class ImageNotLoadedError(MemeGeneratorError):
    """Исключение при работе с незагруженным изображением."""
    pass

class InvalidImageError(MemeGeneratorError):
    """Исключение при работе с некорректным изображением."""
    pass