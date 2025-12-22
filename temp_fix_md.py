# This script is supposed to be used until this issue is solved: https://github.com/rendercv/rendercv/issues/177

import os
import re

LINK_PATTERN = re.compile(r'#link\("(.*)"\)\[(.*)\]')
LINK_REPLACEMENT = r'[\2](\1)'

for file in ["rendercv_output/english/Marion_FABRE_CV.md", "rendercv_output/french/Marion_FABRE_CV.md", "rendercv_output/french_extensive/Marion_FABRE_CV.md"]:
    with open(file, mode="r") as file_handler:
        text = file_handler.read()
        text = re.sub(LINK_PATTERN, LINK_REPLACEMENT, text)
    with open(file, mode="w") as file_handler:
        file_handler.write(text)
