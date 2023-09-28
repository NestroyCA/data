import os
import json
from data.python_scripts.config import br_client, BASEROW_DB_ID, JSON_FOLDER

os.makedirs(JSON_FOLDER, exist_ok=True)
json_file_paths = br_client.dump_tables_as_json(
    BASEROW_DB_ID,
    folder_name="json_dumps", 
    indent=2
)