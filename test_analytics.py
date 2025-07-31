#!/usr/bin/env python3
"""
Test script for Gantt Analytics functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.analytics_service import AnalyticsService

def test_analytics():
    print("Testing Gantt Analytics Service...")
    
    try:
        analytics = AnalyticsService()
        
        # Test project health data
        print("\n1. Testing Project Health Data:")
        health_data = analytics.get_project_health_data()
        print(f"Found {len(health_data)} projects")
        for project in health_data[:3]:  # Show first 3
            print(f"  - {project['name']}: {project['status']} ({project['progress']}%)")
        
        # Test resource utilization
        print("\n2. Testing Resource Utilization:")
        resource_data = analytics.get_resource_utilization_data()
        print(f"Found {len(resource_data)} resources")
        for resource in resource_data[:3]:  # Show first 3
            print(f"  - {resource['name']}: {resource['utilization']}% utilization")
        
        # Test performance metrics
        print("\n3. Testing Performance Metrics:")
        performance_data = analytics.get_performance_metrics()
        print(f"Performance data for {len(performance_data)} periods")
        
        # Test predictive analytics
        print("\n4. Testing Predictive Analytics:")
        predictive_data = analytics.get_predictive_analytics()
        print(f"  - Estimated completion: {predictive_data['estimated_completion']}")
        print(f"  - Budget variance: {predictive_data['budget_variance']}%")
        print(f"  - Risk score: {predictive_data['risk_score']}/100")
        
        # Test report generation
        print("\n5. Testing Report Generation:")
        reports = [
            ('Project Health', analytics.generate_project_health_report()),
            ('Resource Utilization', analytics.generate_resource_utilization_report()),
            ('Performance Metrics', analytics.generate_performance_metrics_report()),
            ('Risk Assessment', analytics.generate_risk_assessment_report())
        ]
        
        for report_name, report_data in reports:
            print(f"  - {report_name}: Generated successfully")
            print(f"    Title: {report_data['title']}")
            print(f"    Generated at: {report_data['generated_at']}")
        
        print("\n✅ All analytics tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Analytics test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_analytics()
    sys.exit(0 if success else 1)