#!/usr/bin/env python3
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import argparse

# 1️⃣ Parse command-line arguments
parser = argparse.ArgumentParser(description="Render all Jinja2 templates in a directory using environment variables.")
parser.add_argument("--input-dir", required=True, help="Directory containing Jinja2 templates")
parser.add_argument("--output-dir", required=True, help="Directory to write rendered files")
args = parser.parse_args()

TEMPLATE_DIR = Path(args.input_dir)
OUTPUT_DIR = Path(args.output_dir)

# 2️⃣ Validate input directory
if not TEMPLATE_DIR.is_dir():
    print(f"Error: {TEMPLATE_DIR} is not a valid directory")
    exit(1)

# 3️⃣ Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 4️⃣ Load environment variables
env_vars = dict(os.environ)

# 5️⃣ Setup Jinja2 environment
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=False)
jinja_env.globals['env'] = env_vars  # make env variables available as {{ env.VAR }}

# 6️⃣ Iterate and render all files
for template_file in TEMPLATE_DIR.glob("*"):
    if template_file.is_file():
        template = jinja_env.get_template(template_file.name)
        rendered_content = template.render()

        output_path = OUTPUT_DIR / template_file.name
        output_path.write_text(rendered_content)
        print(f"Rendered {template_file.name} → {output_path}")
