DEPENDENCIES_INSTALLED = False

try:
    import wand
    import clr
    DEPENDENCIES_INSTALLED = True
except ImportError:
    pass