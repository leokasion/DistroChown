# DistroChown 🛡️

**DistroChown** is a lightweight, cross-distro Python utility designed to standardize **Apache** web root permissions. It automatically identifies the underlying Linux distribution to apply the correct user, group, and permission modes (755/644) required for stable web server operations.

## 🚀 The Problem
Permission drift is a common issue during server migrations, CMS updates, or manual file uploads. Different distributions use different default users (`www-data` vs `apache` vs `wwwrun`) and different web roots (`/var/www/` vs `/srv/www/`). Manual fixing is prone to human error.

## ✨ Features
* **Automated Distro Sensing:** Parses `/etc/os-release` to detect **Debian**, **Rocky**, **RHEL**, or **openSUSE**.
* **Intelligent Mapping:** Automatically switches between `apache`, `www-data`, and `wwwrun` based on the environment.
* **Modern Path Handling:** Built with `pathlib` for robust recursive walking and error handling.
* **Security Focused:** Standardizes directories to `755` and files to `644`.
* **Root Shield:** Built-in UID check to ensure the script has the necessary privileges to execute `chown`.

## 🛠️ Installation & Usage

1. **📥 Clone the repository:**
   ```bash
   git clone https://github.com/leokasion/DistroChown.git
   cd DistroChown
   ```
2. **⚡ Run with Sudo:**
   Since changing file ownership requires superuser privileges:
   ```Bash
    sudo python3 main.py
   ```

3. **📊 Logic Mapping**
    ```
    Distribution	    Web Root	  Default User	    Default Group
    Debian/Ubuntu	    /var/www/	  www-data	        www-data
    Rocky/RHEL	        /var/www/	  apache	        apache
    SUSE/openSUSE	    /srv/www/	  wwwrun	        www
    ```

4. **🖥️ Example**
    ```
    $ sudo python3 main.py 
    [sudo] password for user:           
    [*] Starting permission fix on /var/www for www-data:www-data
    [SET] 755 www-data:www-data -> /var/www/html
    [SET] 755 www-data:www-data -> /var/www/html/settings
    [SET] 644 www-data:www-data -> /var/www/html/index.html
    [SET] 644 www-data:www-data -> /var/www/html/settings/index.html
    ```
