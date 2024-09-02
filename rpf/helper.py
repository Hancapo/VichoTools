from ..vicho_dependencies import dependencies_manager as d
from pathlib import Path as p
import hashlib

def generate_hash(path: str) -> str:
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
    for entry in p(path).iterdir():
        if entry.suffix in ['.exe', '.dll', '.rpf', '.asi', '.txt', '.dat'] or entry.is_dir():
            filefolder = filefolder_list.add()
            filefolder.id = generate_hash(str(entry))
            filefolder.name = entry.name
            filefolder.path = str(entry)
            filefolder.is_rpf = False
            if entry.is_file():
                match entry.suffix:
                    case '.exe':
                        filefolder.file_type = 'EXE'
                    case '.dll':
                        filefolder.file_type = 'DLL'
                    case '.rpf':
                        filefolder.file_type = 'RPF'
                        filefolder.is_rpf = True
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

def get_rpf_file_folder_list(filefolder_list, rpf_path: str):
    found_rpf = None
    for rpf in d.gamecache.AllRpfs:
        if rpf.FilePath == rpf_path:
            found_rpf = rpf
            break
    print(f"Found RPF: {found_rpf} in {rpf_path}")
    if found_rpf:
        for rpf_entry in found_rpf.AllEntries:
            actual_path = str(rpf_entry.Path).replace(rpf_path.lower(), '')
            print(f"Checking entry: {actual_path}")
            slash_count = actual_path.count('\\')
            if slash_count == 1:
                print(f"Adding entry: {actual_path}")
                entry = filefolder_list.add()
                entry.id = generate_hash(actual_path)
                entry.name = rpf_entry.Name
                entry.path = rpf_path
                entry.rpf_path = actual_path
                entry.is_rpf = True
                
                if '.' in rpf_entry.Name:
                    match rpf_entry.Name.split('.')[-1]:
                        case 'ydr':
                            entry.file_type = 'YDR'
                        case 'ydd':
                            entry.file_type = 'YDD'
                        case 'ybn':
                            entry.file_type = 'YBN'
                        case 'xml':
                            entry.file_type = 'XML'
                        case 'ymt':
                            entry.file_type = 'YMT'
                        case 'ytyp':
                            entry.file_type = 'YTYP'
                        case 'dds':
                            entry.file_type = 'DDS'
                        case 'meta':
                            entry.file_type = 'META'
                        case 'fxc':
                            entry.file_type = 'FXC'
                        case 'sps':
                            entry.file_type = 'SPS'
                        case 'ide':
                            entry.file_type = 'IDE'
                        case 'dat':
                            entry.file_type = 'DAT'
                        case 'ycd':
                            entry.file_type = 'YCD'
                        case 'ipl':
                            entry.file_type = 'IPL'
                        case 'pso':
                            entry.file_type = 'PSO'
                        case 'txt':
                            entry.file_type = 'TXT'
                        case 'bmp':
                            entry.file_type = 'BMP'
                        case _:
                            entry.file_type = 'NONE'
                else:
                    entry.file_type = 'FOLDER'
                
            
        

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