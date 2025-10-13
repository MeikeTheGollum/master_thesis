from functools import cached_property
from typing import List, Dict

import owlready2
import requests
import typing_extensions
from owlready2 import Ontology, get_ontology
from requests import Response
from typing import Any
from ontology_helper import OntologyHelper
class ConceptMatching:

    ontoHelper: OntologyHelper

    def __init__(self):
        self.ontoHelper = OntologyHelper(get_ontology)

