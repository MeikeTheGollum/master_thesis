import json
from functools import cached_property
from typing import List, Dict, Optional
from difflib import SequenceMatcher

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

    def get_external_sources(self, obj: str) -> Dict| int:
        """
        Returns every external sources saved inside the ConceptNet entry for a specific string.
        :param obj: The object
        :return: API response
        """
        url = f"http://api.conceptnet.io/query?start=/c/en/{obj}&rel=/r/ExternalURL&limit=10"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print(data)
        except requests.RequestException as e:
            print(f"Error fetching {obj}")

        results = []
        for n in data['edges']:
            results.append(n['end']['@id'])
        return data

    def get_concept_synonyms_of_class(self, obj:str) -> Dict | int:
        """
        Returns the lists of synonym of a given string from ConceptNet.
        :param obj: The object
        :return: API response
        """
        url = f"http://api.conceptnet.io/c/en/{obj}?rel=/Synonym&limit=100"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print(data)
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
    def get_related_terms_of_class(self, obj:str)->List[str]:
        """
        Method to
        :param obj:
        :return:
        """


    def test(self):
        print(self._concepts)
        print(len(self._concepts))
        print(self.get_concept_match("armchair"))
        #test = self.get_list_of_concepts_for_objects(self._concepts)
        test= self.ontoHelper.get_class_annotations
        print(test)
        self.ontoHelper.get_class_synonyms("armchair")
        self.ontoHelper.get_class_seeAlso("armchair")
        #self.get_concept_synonyms_of_class("armchair")
        self.get_external_sources("armchair")

        result = self.ontoHelper.find_class_by_label("arm chair", fuzzy=True)
        if result:
            print("Class: ", result["class"])
            print("URI: ", result["uri"])
            print("Annotations: ", result["annotations"])
            print("Sources", result["sources"])


cm = ConceptMatching(path="https://raw.githubusercontent.com/MeikeTheGollum/master_thesis/refs/heads/main/magicleap-ontology-ar/ontology-servies/resources/ontologies/apartment_objects.rdf")
cm.test()
