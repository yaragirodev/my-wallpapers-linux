import requests
import os
import subprocess 

api = requests.get("https://my-wallpapers.cat8753.ru/api/get-wallpapers")
rJson = api.json()
linkIMG = rJson["url"]
imgpath = "wallpaper.png"

# download photo from api
def download_photo(url, filename="wallpaper.png"):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"photo saved to {filename}")
    except requests.exceptions.RequestException as e:
        print(f"photo save error: {e}")

# set wallpaper (KDE, GNOME)
def setbg(path):
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    abs_path = os.path.abspath(path)

    try:
        if "gnome" in desktop or "unity" in desktop or "cinnamon" in desktop:
            # GNOME (and others)
            subprocess.run([
                "gsettings", "set",
                "org.gnome.desktop.background",
                "picture-uri", f"file://{abs_path}"
            ], check=True)

            # if has dark theme
            subprocess.run([
                "gsettings", "set",
                "org.gnome.desktop.background",
                "picture-uri-dark", f"file://{abs_path}"
            ], check=False)

            print("sucess! (GNOME)")
            print(f"Wallpaper url - {linkIMG}")

        elif "kde" in desktop:
            # KDE Plasma
            script = f"""
            var Desktops = desktops();
            for (i=0;i<Desktops.length;i++) {{
                d = Desktops[i];
                d.wallpaperPlugin = "org.kde.image";
                d.currentConfigGroup = Array("Wallpaper","org.kde.image","General");
                d.writeConfig("Image", "file://{abs_path}");
            }}
            """
            subprocess.run([
                "qdbus-qt5", "org.kde.plasmashell", "/PlasmaShell",
                "org.kde.PlasmaShell.evaluateScript", script
            ], check=True)

            print("sucess! (KDE Plasma)")
            print(f"Wallpaper url - {linkIMG}")

        else:
            print("ERROR: NO DE FOUND! (THIS UTILITY SUPPORTS: KDE, GNOME)")

    except Exception as e:
        print(f"ERROR: {e}")



setbg(imgpath)
download_photo(linkIMG)

