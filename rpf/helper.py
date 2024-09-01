from ..vicho_dependencies import dependencies_manager as d
from pathlib import Path
import hashlib

def generate_path_hash(path: str) -> str:
    hash_function = hashlib.new('md5')
    hash_function.update(path.encode('utf-8'))
    return hash_function.hexdigest()

def update_status():
    return d.Action[str](lambda x: print(x))


def load_gta_cache(path: str) -> bool:
    try:
        d.GTA5Keys.LoadFromPath(path)
        d.gamecache = d.GameFileCache(2147483648, 10, path, "mp2024_01_g9ec", False, "Installers;_CommonRedist")
        d.gamecache.LoadAudio = False
        d.gamecache.LoadVehicles = False
        d.gamecache.LoadPeds = False
        d.gamecache.Init(update_status(), update_status())
        return True
    except Exception as e:
        print(f"Error detail: {e}")
        import traceback 
        traceback.print_exc()
        return False
    
def get_file_folder_list(filefolder_list, path):
    for entry in Path(path).iterdir():
        if entry.suffix in ['.exe', '.dll', '.rpf', '.asi', '.txt', '.dat'] or entry.is_dir():
            filefolder = filefolder_list.add()
            filefolder.id = generate_path_hash(str(entry))
            filefolder.name = entry.name
            filefolder.path = str(entry)
            #filefolder.rpf_entry_type = 'NONE'
            filefolder.rpf_path = ''
            if entry.is_file():
                match entry.suffix:
                    case '.exe':
                        filefolder.file_type = 'EXE'
                    case '.dll':
                        filefolder.file_type = 'DLL'
                    case '.rpf':
                        filefolder.file_type = 'RPF'
                    case '.asi':
                        filefolder.file_type = 'ASI'
                    case '.txt':
                        filefolder.file_type = 'TXT'
                    case '.dat':
                        filefolder.file_type = 'DAT'
                    case _:
                        filefolder.file_type = 'TXT'
            if entry.is_dir():
                filefolder.file_type = 'FOLDER'
        
        

def get_folder_file_icon(filefolder):
    match filefolder:
        case 'EXE':
            return 'TOPBAR'
        case 'DLL':
            return 'LIBRARY_DATA_DIRECT'
        case 'RPF':
            return 'PACKAGE'
        case 'ASI':
            return 'GHOST_ENABLED'
        case 'TXT':
            return 'FILE_TEXT'
        case 'DAT':
            return 'TEXT'
        case 'FOLDER':
            return 'FILE_FOLDER'
        case _:
            return 'FILE'