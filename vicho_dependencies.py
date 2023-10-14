def depen_installed():
    try:
        import wand
        wand_installed = True
        import clr
        pythonnet_installed = True
        return wand_installed and pythonnet_installed
    except ImportError:
        return False
    

def is_imagemagick_installed():
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\ImageMagick\\Current") as key:
            lib_path = winreg.QueryValueEx(key, "LibPath")[0]
            if lib_path:
                return True

    except:
        return False