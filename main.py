import json
import os
from pathlib import Path

from kili.client import Kili
from dotenv import load_dotenv

env_path = Path('') / '.env'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv('key')
project_name = os.getenv('PROJECT_NAME')
kili = Kili(api_key=api_key)
data = {}
project_id = kili.projects()
for project in project_id:
    if project['title'] == project_name:
        all_data = []
        assets = kili.assets(project_id=project['id'])
        for item in assets:
            data = {"id": item['id'], "asterixs": [], "obelixs": []}
            label = item['labels']
            for lab in label:
                values = lab['jsonResponse']
                if 'JOB_0' in values:
                    value_ = values['JOB_0']['annotations']
                    for value in value_:
                        if value['categories'][0]['name'] == "ASTERIX":
                            for rect in value['boundingPoly'][0]['normalizedVertices']:
                                s = rect['x'] * rect['y']
                                data["asterixs"].append(s)
                        else:
                            for rect in value['boundingPoly'][0]['normalizedVertices']:
                                s = rect['x'] * rect['y']
                                data["obelixs"].append(s)
            all_data.append(data)
        with open(f'{project["title"]}.json', 'w') as f:
            json.dump(all_data, f, indent=2)
