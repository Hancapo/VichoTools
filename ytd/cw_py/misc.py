from pathlib import Path

SUPPORTED_FORMATS = [".png", ".jpg", ".bmp", ".tiff", ".tif", ".jpeg", ".dds", ".psd", ".gif", ".webp"]


def get_folder_list_from_dir(dir: str):
    return [str(p) for p in Path(dir).rglob("*") if p.is_dir()]


def get_non_dds(path: str) -> list[str]:
    return [str(p) for p in Path(path).rglob("*") if p.suffix in SUPPORTED_FORMATS]


def get_dds(path: str) -> list[str]:
    return [str(p) for p in Path(path).rglob("*.dds")]


def calculate_mipmaps_lvls(width: int, height: int) -> int:
    if width <= 4 or height <= 4:
        return 1
    levels = 1
    while width > 4 and height > 4:
        width = max(1, width // 2)
        height = max(1, height // 2)
        levels += 1
    return levels
