import os
import sys
import shutil
from pathlib import Path

# --- Configuration Mapping ---
DISTRO_MAP = {
    "debian": {"root": "/var/www/", "user": "www-data", "group": "www-data"},
    "rocky":   {"root": "/var/www/", "user": "apache",   "group": "apache"},
    "rhel":    {"root": "/var/www/", "user": "apache",   "group": "apache"},
    "suse":    {"root": "/srv/www/", "user": "wwwrun",   "group": "www"},
}

def get_distro_info():
    """Parses /etc/os-release to identify the environment."""
    try:
        with open("/etc/os-release", "r") as f:
            content = f.read().lower()
            for distro, config in DISTRO_MAP.items():
                if distro in content:
                    return config
    except FileNotFoundError:
        sys.exit("[!] Error: /etc/os-release not found. Is this a Linux system?")
    return None

def fix_permissions():
    # 1. Root Check
    if os.getuid() != 0:
        sys.exit("[!] This script must be run as root/sudo to change ownership.")

    # 2. Distro Identification
    config = get_distro_info()
    if not config:
        sys.exit("[!] Linux distribution not recognized. Exiting.")

    target_root = Path(config["root"])
    user = config["user"]
    group = config["group"]

    if not target_root.exists():
        sys.exit(f"[!] Target path {target_root} does not exist.")

    print(f"[*] Starting permission fix on {target_root} for {user}:{group}")

    # 3. Recursive Walk
    for path in target_root.rglob("*"):
        try:
            # Set mode: 755 for directories, 644 for files
            mode = 0o755 if path.is_dir() else 0o644
            path.chmod(mode)
            
            # Set ownership
            shutil.chown(str(path), user=user, group=group)
            
            print(f"[SET] {mode:o} {user}:{group} -> {path}")
        except PermissionError:
            print(f"[SKIP] Permission Denied: {path}")
        except Exception as e:
            print(f"[ERROR] Failed to process {path}: {e}")

if __name__ == "__main__":
    fix_permissions()