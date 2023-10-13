checking_status = 'Waiting for ImageMagick installation...'
loading_index = 0  # Nuevo índice
import bpy


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

def check_magick_installation():
    global loading_index  # Acceso a loading_index
    loading_icons = ["◐", "◓", "◑", "◒"]
    if is_imagemagick_installed():
        bpy.app.timers.unregister(check_magick_installation)
        bpy.context.scene.magick_install_status = "ImageMagick is already installed."
        loading_index = 0  # Resetear el índice
        return None
    loading_index = (loading_index + 1) % 4  # Incrementar el índice, pero reiniciarlo después de 3
    bpy.context.scene.magick_install_status = f"Checking ImageMagick installation {loading_icons[loading_index]}"
    return 0.5  # Reducir el intervalo a 0.5 segundos para una animación más fluida
