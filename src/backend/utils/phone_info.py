from src.backend.utils.run import run


def get_phone_info():
    device_model = run("adb shell getprop ro.product.model")[0].replace("\n", "")

    wifi_status = True if "enabled" in run("adb shell dumpsys wifi | sed -n '1p'")[0] else False

    charging_status = {
        "AC": True if "true" in run('adb shell dumpsys battery | grep "AC powered"')[0] else False,
        "USB": True if "true" in run('adb shell dumpsys battery | grep "USB powered"')[0] else False
    }
    charging_status = charging_status["AC"] or charging_status["USB"]

    battery_level = int(run('adb shell dumpsys battery | grep "level"')[0].replace("  level: ", ""))

    phone_info = {
        "device_model": device_model,
        "wifi_status": wifi_status,
        "charging_status": charging_status,
        "battery_level": battery_level,
    }

    return phone_info
