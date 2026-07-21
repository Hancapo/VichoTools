
ENV_TEXTURES: list[str] = [
    "env_bark",
    "env_cloth",
    "env_crusty",
    "env_noise_concrete",
    "env_noise_heavy",
    "env_smooth_concrete2",
    "env_stucco",
    "env_woodgrain",
    "env_woodgrain_2",
]

SUPPORTED_FORMATS: list[str] = [
    ".png",
    ".jpg",
    ".bmp",
    ".tiff",
    ".tif",
    ".tga",
    ".jpeg",
    ".dds",
    ".psd",
    ".gif",
    ".webp",
]

ITD_MENU_ENUM = [
    ("SETTINGS", "Settings", "Settings", "SETTINGS", 0),
    ("EXPORT", "Export", "Export", "FILE_TICK", 2)
]

PROCESS_TYPE = [
    ("ALL", "All", "ALL"),
    ("CHECKED", "Checked item(s)", "Checked item(s)"),
    ("ACTIVE", "Active item", "Active item"),
]

GAME_TYPES = [
    ("GTA5_GEN8", "GTA 5 Legacy", "Grand Theft Auto V YTD"),
    ("GTA5_GEN9", "GTA 5 Enhanced", "Grand Theft Auto V YTD"),
    ("RDR3", "Red Dead Redemption 2", "Red Dead Redemption 2 YTD"),
    ("GTA4", "GTA IV", "Grand Theft Auto IV WTD")
]

DDS_QUALITY_ITEMS = [
    ("0.5", "Preview", "Fast conversion for quick previews"),
    ("0.7", "Standard", "Recommended quality for most DDS textures"),
    ("0.85", "Production", "Higher quality for final assets"),
    ("1.0", "Highest", "Highest quality DDS output"),
]