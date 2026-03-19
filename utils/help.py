from config import (EQUIPO, VERSION, FECHA)
from core.acq import get_acq

acq = get_acq()

async def show_help(transport):
    text = (
        "┏┓┏┓┏┓  ┳┳┳  |==========================================================\r\n"
        "┣┫┃ ┃┃━━┃┃┃  |================== Comandos disponibles ==================\r\n"
        "┛┗┗┛┗┻  ┻┻┻  |==========================================================\r\n"
        "--- General ---\r\n"
        "ESC ?\t\t\t\tAyuda\r\n"
        "ESC e\t\t\t\tDatos y versión del equipo\r\n"
        "--- Startup ---\r\n"
        "ESC s\t\t\t\tServicios en startup\r\n"
        "ESC S [w]\t\t\tHabilita/deshabilita servicios en startup\r\n"
        "ESC W s [SSID]\t\t\tSetea SSID\r\n"
        "--- RTC ---\r\n"
        "ESC H [yyyy,mm,dd,hh,mm,ss]\tSetea fecha y hora en el RTC\r\n"
        "ESC h\t\t\t\tLee fecha y hora desde el RTC\r\n"
        "--- WIFI ---\r\n"
        "ESC w\t\t\t\tInformación sbre WiFi\r\n"
        "ESC W s [SSID]\t\t\tSetea SSID\r\n"
        "ESC W p [password]\t\tSetea password del WiFi\r\n"
        "ESC W c\t\t\t\tConecta a la red WiFi\r\n"
        "ESC W d\t\t\t\tDesconecta de la red WiFi\r\n"
        "--- ACQ ---\r\n"
        "ESC E\t\t\t\tSetea modo de trabajo\r\n"
        "ESC A\t\t\t\tSetea cantidad de canales analógicos\r\n"
        "ESC L s [tiempo]\t\tTransmite lectura de canales analógicos\r\n"
        "ESC L p\t\t\t\tDetiene transmisión de canales analógicos\r\n"
        "ESC L u\t\t\t\tTransmite lectura de canales digitales\r\n"
        "ESC R s [tiempo]\t\tInicia registro en EEPROM\r\n"
        "ESC R p\t\t\t\tDetiene registro en EEPROM\r\n"
        "ESC R d\t\t\t\tDescarga datos de la EEPROM\r\n"
    )
    transport.write(text.encode("utf-8"))

async def show_version(transport):
    text = (
      " $$$$$$\   $$$$$$\   $$$$$$\        $$$$$$\ $$$$$$\ $$$$$$\ \r\n"
      "$$  __$$\ $$  __$$\ $$  __$$\       \_$$  _|\_$$  _|\_$$  _|\r\n"
      "$$ /  $$ |$$ /  \__|$$ /  $$ |        $$ |    $$ |    $$ |  \r\n"
      "$$$$$$$$ |$$ |      $$ |  $$ |$$$$$$\ $$ |    $$ |    $$ |  \r\n"
      "$$  __$$ |$$ |      $$ |  $$ |\______|$$ |    $$ |    $$ |  \r\n"
      "$$ |  $$ |$$ |  $$\ $$ $$\$$ |        $$ |    $$ |    $$ |  \r\n"
      "$$ |  $$ |\$$$$$$  |\$$$$$$ /       $$$$$$\ $$$$$$\ $$$$$$\ \r\n"
      "\__|  \__| \______/  \___$$$\       \______|\______|\______|\r\n"
      "                         \___|                              \r\n"
      f"Equipo: {EQUIPO}\r\n"
      f"Versión: {VERSION}\r\n"
      f"Fecha: {FECHA}\r\n"
      f"Modo: {acq.modo}\r\n"
      f"Canales analógicos: {acq.cant_analog1}\r\n"
    )
    transport.write(text.encode("utf-8"))