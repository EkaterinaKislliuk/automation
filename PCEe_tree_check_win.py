import wmi
import subprocess

class PCIeDiagnostics:
    def __init__(self):
        """
        Initialize the PCIeDiagnostics class.
        """
        self.wmi_client = wmi.WMI()
        self.pcie_devices = self.get_pci_devices()

    def get_pci_devices(self):
        """
        Get information about all PCIe devices on the system using WMI.
        """
        try:
            pci_devices = self.wmi_client.Win32_PnPEntity()
            devices = []

            for device in pci_devices:
                if "PCI" in (device.PNPDeviceID or ""):  # Filter for PCI devices
                    devices.append({
                        "name": device.Name,
                        "device_id": device.DeviceID,
                        "status": device.Status,
                        "pnp_device_id": device.PNPDeviceID
                    })

            return devices
        except Exception as e:
            print(f"An error occurred while accessing PCI devices: {e}")
            return []

    def diagnose_devices(self):
        """
        Diagnose each device to check if it is active or detected.
        """
        for device in self.pcie_devices:
            print(f"Device Name: {device['name']}")
            print(f"Device ID: {device['device_id']}")
            print(f"PNP Device ID: {device['pnp_device_id']}")
            print(f"Status: {device['status']}")

            if device["status"] == "OK":
                print("Status: Device is active and detected.")
            else:
                print("Status: Device is not active or not detected.")
            print("-" * 40)

    def check_driver_status(self):
        """
        Check the driver status for each PCIe device.
        """
        for device in self.pcie_devices:
            print(f"Checking driver for device: {device['name']}")
            drivers = self.wmi_client.Win32_SystemDriver(DeviceID=device["device_id"])
            if drivers:
                for driver in drivers:
                    print(f"  Driver Name: {driver.Name}")
                    print(f"  State: {driver.State}")
                    print(f"  Status: {driver.Status}")
                    if driver.State != "Running":
                        print("  Issue: Driver is not running.")
            else:
                print("  Issue: No driver found for this device.")
            print("-" * 40)

    def check_hardware_errors(self):
        """
        Check for hardware errors or problem statuses for each PCIe device.
        """
        for device in self.pcie_devices:
            print(f"Checking hardware status for device: {device['name']}")
            if hasattr(device, "ConfigManagerErrorCode"):
                error_code = device.ConfigManagerErrorCode
                if error_code != 0:
                    print(f"  Issue: Device has error code {error_code}.")
                else:
                    print("  No hardware errors detected.")
            else:
                print("  Unable to retrieve hardware error status.")
            print("-" * 40)

    def check_power_state(self):
        """
        Check the power state of each PCIe device.
        """
        for device in self.pcie_devices:
            print(f"Checking power state for device: {device['name']}")
            if hasattr(device, "PowerManagementCapabilities"):
                power_state = device.PowerManagementCapabilities
                print(f"  Power State: {power_state}")
                if power_state == 0:
                    print("  Issue: Device is in a low-power state.")
            else:
                print("  Unable to retrieve power state.")
            print("-" * 40)

    def check_event_logs(self):
        """
        Check the event logs for any issues related to PCIe devices.
        """
        try:
            result = subprocess.run(
                ["wevtutil", "qe", "System", "/q:*[System[(EventID=9 or EventID=11 or EventID=15)]]"],
                capture_output=True,
                text=True
            )
            print(result.stdout)
        except Exception as e:
            print(f"An error occurred while checking event logs: {e}")

    def run_diagnostic_command(self):
        """
        Run a diagnostic command to check PCIe devices.
        """
        try:
            result = subprocess.run(
                ["wmic", "path", "Win32_PnPEntity", "get", "/format:list"],
                capture_output=True,
                text=True
            )
            print(result.stdout)
        except Exception as e:
            print(f"An error occurred while running the diagnostic command: {e}")

    def run_all_diagnostics(self):
        """
        Run all diagnostic methods.
        """
        print("Diagnosing PCIe devices...\n")
        self.diagnose_devices()
        self.check_driver_status()
        self.check_hardware_errors()
        self.check_power_state()
        self.check_event_logs()


def main():
    diagnostics = PCIeDiagnostics()

    if not diagnostics.pcie_devices:
        print("No PCIe devices found or an error occurred.")
        return

    print(f"Found {len(diagnostics.pcie_devices)} PCIe devices.\n")
    diagnostics.run_all_diagnostics()


if __name__ == "__main__":
    main()