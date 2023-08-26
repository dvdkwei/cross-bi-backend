import json
import yaml

json_file = open(
    "/Users/davidweinardy/Desktop/BA/cross-bi/cross-bi-backend/config.json", "r"
)

yaml_file = open(
    "/Users/davidweinardy/Desktop/BA/cross-bi/cross-bi-backend/meltano.yml", "r"
)

js = json.load(json_file)

mel = yaml.safe_load(yaml_file)
mel_js = json.loads(json.dumps(mel))

mel_js['plugins']['extractors'][0]['config']['tables'].append(js['tables'][0])

print(yaml.dump(mel_js))
new_file = open('/Users/davidweinardy/Desktop/BA/cross-bi/cross-bi-backend/meltano.yml', 'w')


yaml.dump(mel_js, new_file)
new_file.close()