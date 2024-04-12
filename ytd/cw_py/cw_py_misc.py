from pathlib import Path


def get_folder_list_from_dir(dir: str):
    return [str(p) for p in Path(dir).rglob('*') if p.is_dir()]


def get_non_dds(path: str) -> list[str]:
    supported_formats = ['.png', '.jpg', '.jpeg', '.tga', '.bmp', 'tif', 'tiff']
    return [str(p) for p in Path(path).rglob('*') if p.suffix in supported_formats]


def get_dds(path: str) -> list[str]:
    return [str(p) for p in Path(path).rglob('*.dds')]


def calculate_mipmaps(width: int, height: int) -> int:
    mipLevels = 1
    while width > 4 or height > 4:
        width = max(width // 2, 1)
        height = max(height // 2, 1)
        mipLevels += 1
    return mipLevels