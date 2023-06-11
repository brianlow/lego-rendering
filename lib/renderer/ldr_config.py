import os
import re
import shutil

class LdrConfig:
    def __init__(self, ldraw_path = "./ldraw"):
        self.ldraw_path = ldraw_path
        self.ldr_config_path = os.path.join(ldraw_path, "LDConfig.ldr")
        self.backup_ldr_config_path = os.path.join(ldraw_path, "LDConfig.ldr.original")
        self.lines = []

    def open(self):
        with open(self.ldr_config_path, 'r') as file:
            self.lines = file.readlines()

    def save(self):
        self._backup()
        with open(self.ldr_config_path, 'w') as file:
            file.writelines(self.lines)

    def change_color(self, code, new_value):
        # regex pattern to match a line with the desired color code
        line_pattern = re.compile(r'\bCODE\s+{}\b'.format(code))

        # regex pattern to match the VALUE field
        value_pattern = re.compile(r'\bVALUE\s+#([0-9A-Fa-f]{6})\b')

        # modifying the color value
        for i, line in enumerate(self.lines):
            # checking if the line matches the desired color code pattern
            if line_pattern.search(line):
                # replacing the old value with the new value
                self.lines[i] = value_pattern.sub(f'VALUE #{new_value}', line)
                break

    def _backup(self):
        # check if self.backup_ldr_config_path exists
        # if not, copy self.ldr_config_path to self.backup_ldr_config_path
        if not os.path.exists(self.backup_ldr_config_path):
            shutil.copyfile(self.ldr_config_path, self.backup_ldr_config_path)
