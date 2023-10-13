depen_installed = False

try:
    import wand
    import pythonnet
    depen_installed = True
except ImportError:
    pass