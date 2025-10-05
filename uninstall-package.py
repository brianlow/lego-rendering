import sys
import subprocess

print("Uninstalling lego-rendering package...")
print(f"Python executable: {sys.executable}")

# Uninstall the package using the current Python executable
result = subprocess.run(
    [sys.executable, "-m", "pip", "uninstall", "-y", "lego-rendering"],
    capture_output=True,
    text=True
)

print(result.stdout)
if result.stderr:
    print(result.stderr)

if result.returncode == 0:
    print("\n✓ Successfully uninstalled lego-rendering")
else:
    print(f"\n✗ Uninstallation failed with return code {result.returncode}")
    sys.exit(result.returncode)
