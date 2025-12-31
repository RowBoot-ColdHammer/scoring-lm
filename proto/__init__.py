"""
Proto definitions for Credit Scoring Service
"""
from .credit_scoring_pb2 import *
from .credit_scoring_pb2_grpc import *

__all__ = [
    'CreditRequest',
    'CreditResponse',
    'CreditScoringServiceServicer',
    'CreditScoringServiceStub',
    'add_CreditScoringServiceServicer_to_server',
]
