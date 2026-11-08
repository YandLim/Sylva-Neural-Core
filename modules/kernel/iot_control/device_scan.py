from config import in_config, ex_config
from utils import logger
import tinytuya
import json

system_log = logger.get_logger(__name__, True)
iot_device_path = in_config.IOT_DEVICE_PATH

def get_device_data(json_data: dict, device_name: str, device_id: str) -> dict:
    system_log.info("Running self scan")
    try:
        c = tinytuya.Cloud(
            apiRegion=ex_config.tuya_region,
            apiKey=ex_config.tuya_api,
            apiSecret=ex_config.tuya_secret,
            apiDeviceID=ex_config.tuya_device_id
        )

        devices = c.getdevices()
        for device in devices:
            # Find match ID with user target device
            if device.get("id") == device_id:
                system_log.info("Found match ID")
                local_devices = tinytuya.deviceScan(False, 18, byID=True)

                if device_id in local_devices:
                    device_data = local_devices.get(device_id)
                    ip_address = device_data["ip"]
                    version =  device_data["version"]

                    data = {
                        "device_id": device_id,
                        "ip_address": ip_address,
                        "local_key": device.get("key"),
                        "version": version
                    }

                    json_data[device_name] = data

                    # Update iot device list json file 
                    with open(iot_device_path, "w") as f:
                        json.dump(json_data, f, indent=2)

                    return True, data

                system_log.error("Device is not in same wifi/network")
                return False, None
            
        system_log.error("Can't find the device")
        return False, None
    
    except Exception as e: 
        system_log.error(f"Error occured while scanning device: {e}")
        return False, None
