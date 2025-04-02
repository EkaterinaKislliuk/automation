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
            try:
                drivers = self.wmi_client.query(
                f"SELECT * FROM Win32_PnPSignedDriver WHERE DeviceID LIKE '%{device['pnp_device_id']}%'"
            )            
                if drivers:
                    for driver in drivers:
                        print(f"  Driver Name: {driver.Name}")
                        print(f"  State: {driver.State}")
                        print(f"  Status: {driver.Status}")
                        if driver.State != "Running":
                            print("  Issue: Driver is not running.")
                else:
                    print("  Issue: No driver found for this device.")
            
            except Exception as e:
                print(f"  An error occurred while checking driver status: {e}")
            finally:
                print("-&-" * 40)

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

    def check_power_status(self):
        """
        Check the power status of each PCIe device.
        """
        for device in self.pcie_devices:
            print(f"Checking power status for device: {device['name']}")
            try:
                # Check if the device supports power management
                if hasattr(device, "PowerManagementSupported") and device.PowerManagementSupported:
                    print("  Power Management: Supported")
                else:
                    print("  Power Management: Not Supported")

                # Check the power management capabilities
                if hasattr(device, "PowerManagementCapabilities") and device.PowerManagementCapabilities:
                    capabilities = device.PowerManagementCapabilities
                    print(f"  Power Management Capabilities: {capabilities}")
                    if 1 in capabilities:
                        print("  Device is in a low-power state.")
                    else:
                        print("  Device is in a normal power state.")
                else:
                    print("  Power Management Capabilities: Not Available")
            except Exception as e:
                print(f"  An error occurred while checking power status: {e}")
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
        Run a diagnostic command to check PCIe devices and write results to a log file.
        """
        log_file = "PCIe_diagnostic_results.log"
        try:
            result = subprocess.run(
                ["wmic", "path", "Win32_PnPEntity", "get", "/format:list"],
                capture_output=True,
                text=True
            )
            # Write the results to the log file
            with open(log_file, "w") as file:
                file.write("PCIe Diagnostic Results:\n")
                file.write(result.stdout)
            print(f"Diagnostic results written to {log_file}")
        except Exception as e:
            error_message = f"An error occurred while running the diagnostic command: {e}"
            print(error_message)
            # Write the error to the log file
            with open(log_file, "w") as file:
                file.write(error_message)

    def check_yellow_bang_devices(self):
        """
        Check all devices for a yellow bang (driver issues or incorrect installation).
        """
        print("Checking for devices with a yellow bang (driver issues)...")
        for device in self.pcie_devices:
            try:
                # Check if the device has a ConfigManagerErrorCode property
                if hasattr(device, "ConfigManagerErrorCode"):
                    error_code = device.ConfigManagerErrorCode
                    if error_code != 0:  # Non-zero error codes indicate an issue
                        print(f"Device Name: {device['name']}")
                        print(f"Device ID: {device['device_id']}")
                        print(f"PNP Device ID: {device['pnp_device_id']}")
                        print(f"Error Code: {error_code}")
                        print(f"Issue: {self.get_error_description(error_code)}")
                        print("-" * 40)
            except Exception as e:
                print(f"An error occurred while checking device: {device['name']}. Error: {e}")
        print("Yellow bang device check completed.\n")

    def powershell_check_yellow_bang_devices(self):
        """
        Use PowerShell to check all PCIe devices for a yellow bang (driver issues or incorrect installation).
        """
        print("Using PowerShell to check for devices with a yellow bang (driver issues)...")
        try:
            # PowerShell command to query devices with non-zero ConfigManagerErrorCode
            powershell_command = (
                "Get-WmiObject Win32_PnPEntity | "
                "Where-Object { $_.ConfigManagerErrorCode -ne 0 } | "
                "Select-Object Name, DeviceID, ConfigManagerErrorCode | "
                "Format-Table -AutoSize"
            )
            
            # Run the PowerShell command
            result = subprocess.run(
                ["powershell", "-Command", powershell_command],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Print the output of the PowerShell command
                print("Devices with a yellow bang (driver issues):")
                print(result.stdout)
            else:
                print("PowerShell command failed to execute.")
                print(f"Error: {result.stderr}")
        except Exception as e:
            print(f"An error occurred while using PowerShell to check for yellow bang devices: {e}")

    def powershell_check_all_drivers_for_yellow_bang(self):
        """
        Use PowerShell to detect all available drivers in Windows and check them for yellow bang issues.
        Outputs a list of devices with yellow bang problems.
        """
        print("Using PowerShell to check all drivers for yellow bang issues...")
        try:
            # PowerShell command to query all drivers with non-zero ConfigManagerErrorCode
            powershell_command = (
                "Get-WmiObject Win32_PnPEntity | "
                "Where-Object { $_.ConfigManagerErrorCode -ne 0 } | "
                "Select-Object Name, DeviceID, ConfigManagerErrorCode | "
                "Format-Table -AutoSize"
            )
            
            # Run the PowerShell command
            result = subprocess.run(
                ["powershell", "-Command", powershell_command],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Print the output of the PowerShell command
                print("Devices with yellow bang issues (driver problems):")
                print(result.stdout)
            else:
                print("PowerShell command failed to execute.")
                print(f"Error: {result.stderr}")
        except Exception as e:
            print(f"An error occurred while using PowerShell to check all drivers for yellow bang issues: {e}")

    def get_error_description(self, error_code):
        """
        Get a human-readable description of the ConfigManagerErrorCode.
        """
        error_descriptions = {
            1: "Device is not configured correctly.",
            2: "Device is not working properly.",
            3: "Driver for the device is not installed.",
            4: "Driver for the device is installed incorrectly.",
            5: "Device requires a resource that is not available.",
            6: "The boot configuration for the device conflicts with other devices.",
            7: "Cannot filter.",
            8: "Driver loader for the device is missing.",
            9: "Device is not working properly due to a firmware issue.",
            10: "Device cannot start.",
            11: "Device failed.",
            12: "Device cannot find enough free resources.",
            13: "Windows cannot verify the device's resources.",
            14: "Device is being removed.",
            15: "Device is disabled.",
            16: "Device is not present, not working properly, or does not have all its drivers installed.",
            17: "Device needs to be rebooted to work properly.",
        }
        return error_descriptions.get(error_code, "Unknown error code.")

    def run_all_diagnostics(self):
        """
        Run all diagnostic methods.
        """
        print("Diagnosing PCIe devices...\n")
        self.diagnose_devices()
        self.check_driver_status()
        self.check_hardware_errors()
        self.check_power_state()
        self.check_power_status()
        self.check_event_logs()
        self.run_diagnostic_command()
        self.check_yellow_bang_devices()
        self.powershell_check_yellow_bang_devices()

        
    


def main():
    diagnostics = PCIeDiagnostics()

    if not diagnostics.pcie_devices:
        print("No PCIe devices found or an error occurred.")
        return

    print(f"Found {len(diagnostics.pcie_devices)} PCIe devices.\n")
    diagnostics.run_all_diagnostics()


if __name__ == "__main__":
    main()