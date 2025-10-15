import json
from functools import cached_property
from typing import List, Dict

import owlready2
import requests
from owlready2 import Ontology, get_ontology
from requests import Response
from typing import Any
from ontology_helper import OntologyHelper
class ConceptMatching:

    ontoHelper: OntologyHelper
    ONTO_PATH: str
    _concepts : List[str]

    def __init__(self, path: str):
        self.ONTO_PATH = path
        self.ontoHelper = OntologyHelper(get_ontology(self.ONTO_PATH))
        self._concepts = self.ontoHelper.get_classes
    def get_concept_match(self, object: str) -> Dict | int:
        """
        Return the API response of a given string from ConceptNet.
        :param name: The object
        :return: API response
        """
        url = f"http://api.conceptnet.io/c/en/{object}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            print(f"Error ferching {object}_ {e}")
            return {}
        return data

    def get_list_of_concepts_for_objects(self, objects: List[str]) -> List[Dict]:
        """
        Collects every associated API response from ConceptNet for the given list of classes of strings

        :param objects: The list of all objects of the given ontology.
        :return: list of jsons for each object
        """
        results = {}
        for obj in objects:
            print(f"Fetching ConceptNet entry for: {obj}")
            results[obj] = self.get_concept_match(obj)
        return results

    def save_concepts_to_file(self, results: List[Dict]):
        """
        Saves the results of the concept search into a json file
        :param results: The results of the search for concepts

        """
        with open("../../resources/concept_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    def test(self):
        print(self._concepts)
        print(len(self._concepts))
        #test = self.get_list_of_concepts_for_objects(self._concepts)
        test= self.ontoHelper.get_class_annotations
        print(test)
        self.ontoHelper.get_class_synonyms("armchair")
        self.ontoHelper.get_class_seeAlso("armchair")


cm = ConceptMatching(path="https://raw.githubusercontent.com/MeikeTheGollum/master_thesis/refs/heads/main/magicleap-ontology-ar/ontology-servies/resources/ontologies/apartment_objects.rdf")
cm.test()
