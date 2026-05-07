"""
Customer Churn Prediction Pipeline
===================================
Author: Rakibul Hassan
Company: Link3 Technologies
Purpose: End-to-end ML pipeline for predicting ISP customer churn using local LLMs
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class ChurnPipeline:
    """
    End-to-end pipeline for customer churn prediction.
    Integrates with local LLMs (Qwen/Gemma) for classification.
    """
    
    def __init__(self, api_url: str = "http://localhost:1234/v1/chat/completions"):
        self.api_url = api_url
        self.risk_thresholds = {
            'high': 0.7,
            'medium': 0.4,
            'low': 0.0
        }
    
    def ingest_customer_data(self, customer_data: Dict) -> Dict:
        """Stage 1: Data Ingestion - Collect customer information"""
        required_fields = ['customer_id', 'complaints', 'billing_history', 'support_tickets']
        
        for field in required_fields:
            if field not in customer_data:
                customer_data[field] = [] if field in ['complaints', 'support_tickets'] else {}
        
        customer_data['_ingested_at'] = datetime.now().isoformat()
        return customer_data
    
    def feature_engineering(self, customer_data: Dict) -> Dict:
        """Stage 2: Feature Engineering - Extract predictive features"""
        features = {}
        
        # Complaint-based features
        complaints = customer_data.get('complaints', [])
        features['total_complaints'] = len(complaints)
        features['recent_complaints_30d'] = self._count_recent(complaints, 30)
        features['recent_complaints_90d'] = self._count_recent(complaints, 90)
        
        # Categorize complaint types
        categories = {'network': 0, 'billing': 0, 'service': 0, 'technical': 0}
        for c in complaints:
            cat = c.get('category', 'service').lower()
            if cat in categories:
                categories[cat] += 1
        features['complaint_categories'] = categories
        
        # Support ticket features
        tickets = customer_data.get('support_tickets', [])
        features['total_tickets'] = len(tickets)
        features['open_tickets'] = sum(1 for t in tickets if t.get('status') == 'open')
        features['avg_resolution_time'] = self._avg_resolution_time(tickets)
        
        # Billing features
        billing = customer_data.get('billing_history', {})
        features['payment_delays'] = billing.get('delays', 0)
        features['plan_downgrades'] = billing.get('downgrades', 0)
        features['subscription_months'] = billing.get('months', 12)
        
        # Engagement score
        features['engagement_score'] = self._calculate_engagement(features)
        
        return features
    
    def _count_recent(self, items: List, days: int) -> int:
        """Count items from recent days"""
        # Simplified: assume all items are recent for demo
        return len(items) if len(items) <= 5 else len(items) // 2
    
    def _avg_resolution_time(self, tickets: List) -> float:
        """Calculate average ticket resolution time in hours"""
        resolved = [t for t in tickets if t.get('status') == 'resolved']
        if not resolved:
            return 0.0
        return sum(t.get('resolution_hours', 24) for t in resolved) / len(resolved)
    
    def _calculate_engagement(self, features: Dict) -> float:
        """Calculate customer engagement score (0-1)"""
        score = 1.0
        
        # Reduce for complaints
        score -= features.get('total_complaints', 0) * 0.05
        score -= features.get('recent_complaints_30d', 0) * 0.1
        
        # Reduce for billing issues
        score -= features.get('payment_delays', 0) * 0.1
        
        # Reduce for poor service
        if features.get('avg_resolution_time', 0) > 48:
            score -= 0.15
        
        return max(0.0, min(1.0, score))
    
    def predict_with_llm(self, features: Dict, model: str = "qwen") -> Dict:
        """Stage 3: LLM-based prediction using local models"""
        prompt = self._build_prediction_prompt(features)
        
        try:
            response = self._call_llm(prompt, model)
            return self._parse_prediction(response, features)
        except Exception as e:
            # Fallback to rule-based prediction
            return self._rule_based_prediction(features)
    
    def _build_prediction_prompt(self, features: Dict) -> str:
        """Build prompt for LLM prediction"""
        return f"""Analyze this ISP customer for churn risk:

Features:
- Total Complaints: {features['total_complaints']}
- Recent Complaints (30d): {features['recent_complaints_30d']}
- Open Tickets: {features['open_tickets']}
- Payment Delays: {features['payment_delays']}
- Avg Resolution Time: {features['avg_resolution_time']:.1f}h
- Engagement Score: {features['engagement_score']:.2f}

Respond with:
1. Churn Risk: HIGH/MEDIUM/LOW
2. Risk Score: 0.0-1.0
3. Key Factors: list of contributing factors
4. Retention Actions: recommended actions"""
    
    def _call_llm(self, prompt: str, model: str) -> str:
        """Call local LLM via LM Studio"""
        import requests
        
        payload = {
            "messages": [
                {"role": "system", "content": "You are a customer retention specialist."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }
        
        response = requests.post(self.api_url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    
    def _parse_prediction(self, llm_response: str, features: Dict) -> Dict:
        """Parse LLM response into structured prediction"""
        # Simple parsing based on keywords
        response_lower = llm_response.lower()
        
        if 'high' in response_lower and 'risk' in response_lower:
            risk_level = 'HIGH'
            risk_score = 0.85
        elif 'medium' in response_lower and 'risk' in response_lower:
            risk_level = 'MEDIUM'
            risk_score = 0.55
        else:
            risk_level = 'LOW'
            risk_score = 0.25
        
        # Derive from features if LLM parsing ambiguous
        if risk_score == 0.25:
            risk_score = self._calculate_risk_score(features)
            risk_level = self._score_to_level(risk_score)
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'model_used': 'llm_analysis',
            'factors': self._extract_factors(llm_response, features)
        }
    
    def _rule_based_prediction(self, features: Dict) -> Dict:
        """Fallback rule-based prediction"""
        risk_score = self._calculate_risk_score(features)
        return {
            'risk_level': self._score_to_level(risk_score),
            'risk_score': risk_score,
            'model_used': 'rule_based',
            'factors': self._identify_top_factors(features)
        }
    
    def _calculate_risk_score(self, features: Dict) -> float:
        """Calculate risk score from features"""
        score = 0.0
        
        # High complaint frequency
        if features['total_complaints'] > 3:
            score += 0.3
        if features['recent_complaints_30d'] > 2:
            score += 0.25
        
        # Open tickets
        if features['open_tickets'] > 1:
            score += 0.2
        
        # Billing issues
        if features['payment_delays'] > 0:
            score += 0.15
        
        # Poor resolution time
        if features['avg_resolution_time'] > 48:
            score += 0.1
        
        # Low engagement
        if features['engagement_score'] < 0.5:
            score += 0.2
        
        return min(1.0, score)
    
    def _score_to_level(self, score: float) -> str:
        """Convert score to risk level"""
        if score >= self.risk_thresholds['high']:
            return 'HIGH'
        elif score >= self.risk_thresholds['medium']:
            return 'MEDIUM'
        return 'LOW'
    
    def _extract_factors(self, response: str, features: Dict) -> List[str]:
        """Extract key factors from LLM response"""
        factors = []
        
        if features['total_complaints'] > 3:
            factors.append(f"High complaint volume ({features['total_complaints']})")
        if features['open_tickets'] > 0:
            factors.append(f"Unresolved tickets ({features['open_tickets']})")
        if features['payment_delays'] > 0:
            factors.append("Payment history issues")
        if features['avg_resolution_time'] > 24:
            factors.append("Slow support response")
        
        return factors or ["Standard customer profile"]
    
    def _identify_top_factors(self, features: Dict) -> List[str]:
        """Identify top contributing factors"""
        factors = []
        
        if features['recent_complaints_30d'] > 1:
            factors.append("Recent complaint spike")
        if features['open_tickets'] > 0:
            factors.append("Open support tickets")
        if features['payment_delays'] > 0:
            factors.append("Payment delays")
        if features['engagement_score'] < 0.6:
            factors.append("Low engagement")
        
        return factors or ["No significant risk indicators"]
    
    def evaluate_model(self, predictions: List[Dict], actuals: List[bool]) -> Dict:
        """Stage 4: Model Evaluation"""
        if len(predictions) != len(actuals):
            raise ValueError("Predictions and actuals must have same length")
        
        true_positives = sum(1 for p, a in zip(predictions, actuals) 
                           if p['risk_level'] == 'HIGH' and a)
        false_positives = sum(1 for p, a in zip(predictions, actuals) 
                            if p['risk_level'] == 'HIGH' and not a)
        false_negatives = sum(1 for p, a in zip(predictions, actuals) 
                            if p['risk_level'] != 'HIGH' and a)
        true_negatives = sum(1 for p, a in zip(predictions, actuals) 
                          if p['risk_level'] != 'HIGH' and not a)
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        accuracy = (true_positives + true_negatives) / len(predictions) if len(predictions) > 0 else 0
        
        return {
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'accuracy': accuracy,
            'true_positives': true_positives,
            'false_positives': false_positives,
            'false_negatives': false_negatives,
            'true_negatives': true_negatives,
            'total_samples': len(predictions)
        }
    
    def run_pipeline(self, customer_data: Dict, model: str = "qwen") -> Dict:
        """Execute full ML pipeline"""
        print("=" * 60)
        print("MLOps Customer Churn Prediction Pipeline")
        print("=" * 60)
        
        # Stage 1: Ingestion
        print("\n[Stage 1] Data Ingestion...")
        data = self.ingest_customer_data(customer_data)
        print(f"  ✓ Customer {data['customer_id']} data ingested")
        
        # Stage 2: Feature Engineering
        print("\n[Stage 2] Feature Engineering...")
        features = self.feature_engineering(data)
        print(f"  ✓ Extracted {len(features)} features")
        print(f"    - Engagement Score: {features['engagement_score']:.2f}")
        
        # Stage 3: Prediction
        print(f"\n[Stage 3] LLM Prediction ({model})...")
        prediction = self.predict_with_llm(features, model)
        print(f"  ✓ Risk Level: {prediction['risk_level']}")
        print(f"  ✓ Risk Score: {prediction['risk_score']:.2f}")
        print(f"  ✓ Model Used: {prediction['model_used']}")
        
        # Output
        result = {
            'customer_id': data['customer_id'],
            'features': features,
            'prediction': prediction,
            'pipeline_version': '1.0.0',
            'timestamp': datetime.now().isoformat()
        }
        
        print("\n" + "=" * 60)
        print(f"FINAL RESULT: {prediction['risk_level']} RISK")
        print("=" * 60)
        
        return result
