import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'career'))

from models import db, Job
from app import create_app
from datetime import datetime

def add_sample_jobs():
    app = create_app()
    with app.app_context():
        jobs = [
            Job(
                title="Import Operations Manager",
                department="Import/Export",
                location="Mumbai",
                type="Full-time",
                experience="3-5 years",
                salary_range="₹8-12 LPA",
                description="Manage import operations, coordinate with suppliers, handle documentation and customs clearance.",
                requirements="Bachelor's degree, experience in import operations, knowledge of customs procedures.",
                benefits="Health insurance, performance bonus, travel allowance"
            ),
            Job(
                title="Export Sales Executive",
                department="Export",
                location="Delhi",
                type="Full-time",
                experience="2-4 years",
                salary_range="₹6-10 LPA",
                description="Develop export markets, manage client relationships, handle export documentation.",
                requirements="MBA/Bachelor's in International Business, export experience, excellent communication skills.",
                benefits="Incentives, medical coverage, professional development"
            ),
            Job(
                title="Trading Analyst",
                department="Trading",
                location="Bangalore",
                type="Full-time",
                experience="1-3 years",
                salary_range="₹5-8 LPA",
                description="Analyze market trends, support trading decisions, prepare market reports.",
                requirements="Finance/Economics degree, analytical skills, knowledge of trading platforms.",
                benefits="Performance bonus, health insurance, flexible hours"
            ),
            Job(
                title="Digital Marketing Specialist",
                department="Marketing",
                location="Pune",
                type="Full-time",
                experience="2-4 years",
                salary_range="₹4-7 LPA",
                description="Manage digital campaigns, SEO/SEM, social media marketing for international markets.",
                requirements="Marketing degree, digital marketing experience, Google Ads certification preferred.",
                benefits="Creative environment, skill development, health benefits"
            ),
            Job(
                title="International Trade Coordinator",
                department="Import/Export",
                location="Chennai",
                type="Full-time",
                experience="1-2 years",
                salary_range="₹3-5 LPA",
                description="Coordinate international shipments, manage trade documentation, liaise with freight forwarders.",
                requirements="Commerce degree, basic trade knowledge, attention to detail.",
                benefits="Training programs, career growth, medical insurance"
            ),
            Job(
                title="Commodity Trader",
                department="Trading",
                location="Mumbai",
                type="Full-time",
                experience="3-6 years",
                salary_range="₹10-18 LPA",
                description="Trade agricultural commodities, manage risk, develop trading strategies.",
                requirements="Finance/Agriculture degree, commodity trading experience, risk management skills.",
                benefits="High incentives, comprehensive insurance, retirement benefits"
            ),
            Job(
                title="Export Documentation Executive",
                department="Export",
                location="Kolkata",
                type="Full-time",
                experience="1-3 years",
                salary_range="₹3-6 LPA",
                description="Prepare export documents, ensure compliance, coordinate with shipping lines.",
                requirements="Commerce background, export documentation knowledge, computer proficiency.",
                benefits="Skill enhancement, health coverage, performance rewards"
            ),
            Job(
                title="Marketing Manager - International",
                department="Marketing",
                location="Hyderabad",
                type="Full-time",
                experience="5-8 years",
                salary_range="₹12-20 LPA",
                description="Develop international marketing strategies, manage global campaigns, lead marketing team.",
                requirements="MBA Marketing, international marketing experience, leadership skills.",
                benefits="Leadership development, stock options, comprehensive benefits"
            ),
            Job(
                title="Import Compliance Officer",
                department="Import/Export",
                location="Ahmedabad",
                type="Full-time",
                experience="2-5 years",
                salary_range="₹6-9 LPA",
                description="Ensure import compliance, manage regulatory requirements, conduct audits.",
                requirements="Law/Commerce degree, compliance experience, regulatory knowledge.",
                benefits="Professional certification support, health benefits, job security"
            ),
            Job(
                title="Trade Finance Executive",
                department="Trading",
                location="Mumbai",
                type="Full-time",
                experience="2-4 years",
                salary_range="₹7-11 LPA",
                description="Manage trade finance operations, handle LC/BG processing, coordinate with banks.",
                requirements="Finance degree, trade finance knowledge, banking experience preferred.",
                benefits="Banking network access, professional growth, comprehensive insurance"
            )
        ]
    
        for job in jobs:
            db.session.add(job)
        
        db.session.commit()
        print("Successfully added 10 sample jobs!")

if __name__ == "__main__":
    add_sample_jobs()