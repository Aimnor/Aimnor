# This script is supposed to be used until next rendercv release https://github.com/rendercv/rendercv/issues/177

import os

output_dir = "rendercv_output"
for file in os.listdir(output_dir):
    if file.endswith(".md"):
        with open(os.path.join(output_dir, file), mode="r") as file_handler:
            text = file_handler.read()
            text = text.replace(r" \begin{itemize}", "").replace(r" \end{itemize}", "").replace(r"\item", "\n\t-")
        with open(os.path.join(output_dir, file), mode="w") as file_handler:
            file_handler.write(text)
