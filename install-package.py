import sys
import subprocess

print("Installing lego-rendering package...")
print(f"Python executable: {sys.executable}")

# Install the package using the current Python executable
result = subprocess.run(
    [sys.executable, "-m", "pip", "install", "--upgrade", "--user", "lego-rendering"],
    capture_output=True,
    text=True
)

print(result.stdout)
if result.stderr:
    print(result.stderr)

if result.returncode == 0:
    print("\n✓ Successfully installed lego-rendering")
else:
    print(f"\n✗ Installation failed with return code {result.returncode}")
    sys.exit(result.returncode)
