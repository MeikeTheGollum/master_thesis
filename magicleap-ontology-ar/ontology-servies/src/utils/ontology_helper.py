from difflib import SequenceMatcher
from functools import cached_property
from typing import List, Optional, Dict, Any
from rdflib import URIRef
import owlready2
from owlready2 import Ontology
from gensim.models import Word2Vec, KeyedVectors
class OntologyHelper:
    ontology: Ontology
    _concept_embeddings: Optional[KeyedVectors] = None


    def __init__(self, ontology: Ontology):
        self.ontology = ontology
        self.ontology.load()


    @cached_property
    def get_classes(self) -> List[str]:
        """
        Helper method to create a list of every class inside the ontology.
        :return: The list of all classes currently present inside the ontology
        """
        classes = []
        for concept in self.ontology.classes():
            if concept.label:
                classes.append(concept.label[0])  # take first label
            else:
                classes.append(concept.name)  # fallback
        return classes

    @cached_property
    def get_class_annotations(self) -> Dict[str, Dict[str, List[Any]]]:
        """
        Helper method to collect the AnnotationProperties of each created Class in the ontology.
        :return: The Dictionary with the class name and every AnnotationPropterty of it
        """
        result = {}
        for cls in self.ontology.classes():
            cls_name = cls.label[0] if cls.label else cls.name
            annotations = {}

            for ap in self.ontology.annotation_properties():
                values = getattr(cls, ap.name, [])
                if values:
                    annotations[ap.name] = list(values)

            result[cls_name] = annotations
        return result


    @property
    def get_class_embeddings(self) -> KeyedVectors:
        """
        Creates keyed vectors for each class of the ontology for further possibilities
        for entity matching.
        :return: The list of vectors based on the Word2Vec approach
        """
        if not self._concept_embeddings:
            data = [[name] for name in self.concept_names]
            model = Word2Vec(data, min_count=1, vector_size = 100, window=5)
            self._concept_embeddings = model.wv
        return self._concept_embeddings

    def get_class_seeAlso(self, obj: str) -> str:
        """
        Helper method to get the rdfs:seeAlso property of a given class.
        :param obj: The class
        :return: The WikiData link
        """
        for cls in self.ontology.classes():
            if cls.label and obj.lower() == cls.label[0].lower():
                print(getattr(cls, "seeAlso", [])[0])
                return getattr(cls, "seeAlso", [])[0]
        return []
    def get_class_synonyms(self, obj:str) -> List[str]:
        """
        Helper method to create the list of synonyms of a given class
        :param: obj: the class
        :return: The list of synonyms for the class
        """
        test = self.get_class_annotations[obj]['synonym']
        print(test)
    def find_class_by_label(self, label:str, fuzzy: bool = False) -> Optional[Dict[str, Any]]:
        """
        Method to find an ontology class by its rdfs:label. If fuzzy is set to true, it
        performs an approximate string matching. It returns a dictionary containing every
        important information
        :param label: The label we search for
        :param fuzzy: Whether to use approximate string matching
        :return: A dict with class info, or None if not found
        """
        bestMatch = None
        bestScore = 0.0

        for cls in self.ontology.classes():
            if not cls.label:
                continue
            clsLabel = cls.label[0]
            if fuzzy:
                score = SequenceMatcher(None, label.lower(), clsLabel.lower()).ratio()
                if score > bestScore:
                    bestMatch, bestScore = cls, score
            else:
                if clsLabel.lower() == label.lower():
                    bestMatch = cls
                    break
        if not bestMatch:
            print("Nothing found")
            return None

        annotations = {}
        for ap in self.ontology.annotation_properties():
            values = getattr(bestMatch, ap.name, [])
            if values:
                annotations[ap.name] = list(values)
        if not fuzzy:
            externalSources = self.get_class_seeAlso(label)
        else:
            externalSources = self.get_class_seeAlso(clsLabel)
        return {
            "class": bestMatch,
            "uri": bestMatch.iri,
            "name": bestMatch.name,
            "annotations": annotations ,
            "sources": externalSources
        }
    @get_class_embeddings.setter
    def concept_embeddings(self, value: KeyedVectors):
        self._concept_embeddings = value
