def depen_installed():
    try:
        import wand
        wand_installed = True
        import clr
        pythonnet_installed = True
        return wand_installed and pythonnet_installed
    except ImportError:
        return False