import json
import re 

class Jsonyfier:
    @staticmethod
    def parse(selected_items):
        parsed_items = []
        for item in selected_items:
            try:
                json_format = item.replace("'", '"')
                parsed_item = json.loads(json_format)
                parsed_items.append(parsed_item)
            except json.JSONDecodeError:
                regex = r'("[^"]*")([^"]*")'
                json_corrected = re.sub(regex, r'\1', json_format)
                parsed_item = json.loads(json_corrected)
                parsed_items.append(parsed_item)
        return parsed_items