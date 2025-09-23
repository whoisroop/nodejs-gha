#!/usr/bin/env python3
import os
import sys
import argparse
import yaml
import shutil
from jinja2 import Environment, FileSystemLoader, StrictUndefined, Template

def render_file(template_path, env, vars_data):
    """Render a single file, or return original content if no template syntax present."""
    with open(template_path, 'r') as f:
        content = f.read()

    # If there's no Jinja delimiters at all, just return original content
    if "{{" not in content and "{%" not in content:
        return content

    # Render via Jinja environment
    # We can't use env.get_template easily for arbitrary paths, so use Template directly
    template = env.from_string(content)
    return template.render(vars_data)

def render_path(input_path, values_file, strict=False):
    # Load variables from YAML
    with open(values_file, 'r') as vf:
        vars_data = yaml.safe_load(vf) or {}

    # Choose Jinja environment
    if strict:
        env = Environment(autoescape=False, undefined=StrictUndefined)
    else:
        env = Environment(autoescape=False)

    env.globals['env'] = dict(os.environ)

    if os.path.isfile(input_path):
        # Single file case
        out_file = f"{input_path}-rendered"
        rendered = render_file(input_path, env, vars_data)
        with open(out_file, 'w') as f:
            f.write(rendered)
        print(f"Rendered {input_path} -> {out_file}")

    elif os.path.isdir(input_path):
        # Directory case
        base_name = os.path.basename(input_path.rstrip(os.sep))
        parent_dir = os.path.dirname(input_path.rstrip(os.sep)) or '.'
        output_dir = os.path.join(parent_dir, f"{base_name}-rendered")

        for root, dirs, files in os.walk(input_path):
            rel_dir = os.path.relpath(root, input_path)
            dest_dir = os.path.join(output_dir, rel_dir) if rel_dir != '.' else output_dir
            os.makedirs(dest_dir, exist_ok=True)

            for d in dirs:
                os.makedirs(os.path.join(dest_dir, d), exist_ok=True)

            for file_name in files:
                src_file = os.path.join(root, file_name)
                dest_file = os.path.join(dest_dir, file_name)
                try:
                    rendered_content = render_file(src_file, env, vars_data)
                    with open(dest_file, 'w') as f:
                        f.write(rendered_content)
                    print(f"Rendered {src_file} -> {dest_file}")
                except Exception as e:
                    print(f"Error rendering {src_file}: {e}", file=sys.stderr)
    else:
        print(f"Path not found: {input_path}", file=sys.stderr)
        sys.exit(3)

def main():
    parser = argparse.ArgumentParser(description="Render YAML/templates preserving structure")
    parser.add_argument('--path', required=True, help='Path to template file or directory')
    parser.add_argument('--values', required=True, help='YAML file with variables')
    parser.add_argument('--strict', action='store_true',
                        help='Fail on undefined Jinja variables (StrictUndefined)')
    args = parser.parse_args()
    render_path(args.path, args.values, args.strict)

if __name__ == '__main__':
    main()
