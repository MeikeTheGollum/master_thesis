from functools import cached_property
from typing import List, Optional

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

    @get_class_embeddings.setter
    def concept_embeddings(self, value: KeyedVectors):
        self._concept_embeddings = value
