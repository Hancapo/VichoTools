def depen_installed():
    try:
        import clr
        pythonnet_installed = True
        return pythonnet_installed
    except ImportError:
        return False
