import json
from typing import Dict


class JSONHelper:
    def __init__(self, file: str):
        self.jsonFile = file
        self.data = None

    def load_file(self):
        """
        Helper method to load the already collected ConceptNet api responses
        :return:
        """
        try:
            with open(f"{self.jsonFile}", encoding="utf-8") as file:
                self.data = json.load(file)
            print(f"Successfully loaded {self.jsonFile}")

        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file {self.jsonFile} not found")
    def get_entry(self, obj : str) -> Dict:
        """
        Helper method to return the entry from the object
        :param obj:
        :return:
        """
        try:
            result = self.data[obj]
        except KeyError:
            print(f"{obj} was not found")
            return []
        return result



test = JSONHelper(file="C:/Users/meike/Desktop/master_thesis/magicleap-ontology-ar/ontology-servies/resources/concept_results.json")
test.load_file()
test.get_entry("armchair")