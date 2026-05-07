"""
MLOps Module for Customer Churn Prediction
============================================
Author: Rakibul Hassan
Company: Link3 Technologies
Purpose: Demonstrates MLOps practices with local LLMs for ISP customer churn prediction
"""

from .churn_pipeline import ChurnPipeline
from .model_registry import ModelRegistry
from .monitor import PerformanceMonitor
from .ab_tester import ABTester
from .retrain_trigger import RetrainTrigger

__all__ = [
    'ChurnPipeline',
    'ModelRegistry', 
    'PerformanceMonitor',
    'ABTester',
    'RetrainTrigger'
]

__version__ = '1.0.0'
