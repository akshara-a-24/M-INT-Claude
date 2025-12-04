import os

DIRECTORY_STRUCTURE = {
    "api": ["main.py"],
    "core": {
        "__init__.py": "",
        "config.py": "",
        "vision_client.py": "",
        "reasoner_client.py": "",
        "forensics": {
            "__init__.py": "",
            "exif.py": "",
            "ela.py": "",
            "noise.py": "",
            "provenance.py": "",
        },
        "utils": {
            "__init__.py": "",
            "image_loader.py": "",
            "logger.py": "",
            "parsing.py": "",
        },
    },
    "pipeline": {
        "__init__.py": "",
        "registry.py": "",
        "loader.py": "",
        "pipeline_runner.py": "",
        "plugins": {
            "__init__.py": "",
            "onlycars": {
                "__init__.py": "",
                "schema.py": "",
                "visual.py": "",
                "supplemental.py": "",
                "decision.py": "",
            },
            "drinkwise": {
                "__init__.py": "",
                "schema.py": "",
                "visual.py": "",
                "supplemental.py": "",
                "decision.py": "",
            },
        },
    },
    "schemas": {"__init__.py": "", "base.py": "", "request.py": "", "response.py": ""},
    "utils": {"__init__.py": "", "id_gen.py": "", "time.py": ""},
}


def create_structure(base_path, structure):
    """Recursively create directory and file structure."""
    if isinstance(structure, dict):
        for name, content in structure.items():
            path = os.path.join(base_path, name)

            # Create directory
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                create_structure(path, content)

            # Create file
            elif isinstance(content, str):
                os.makedirs(base_path, exist_ok=True)
                with open(path, "w") as f:
                    f.write(content)

    elif isinstance(structure, list):
        for file_name in structure:
            path = os.path.join(base_path, file_name)
            os.makedirs(base_path, exist_ok=True)
            with open(path, "w") as f:
                f.write("")


if __name__ == "__main__":
    BASE_DIR = os.getcwd()  # Runs inside M-INT directory
    print(f"Creating full project structure inside: {BASE_DIR}")

    for folder, content in DIRECTORY_STRUCTURE.items():
        create_structure(os.path.join(BASE_DIR, folder), content)

    print("✅ Directory structure created successfully!")
