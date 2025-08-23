import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import uuid


class CompanyStage(Enum):
    SEED = "seed"
    SERIES_A = "series_a" 
    SERIES_B = "series_b"
    GROWTH = "growth"


class FinancialScenario(Enum):
    HEALTHY_GROWTH = "healthy_growth"
    CASH_CRUNCH = "cash_crunch"
    RAPID_BURN = "rapid_burn"
    SEASONAL_BUSINESS = "seasonal_business"
    POST_FUNDING = "post_funding"


@dataclass
class MockCompanyProfile:
    name: str
    stage: CompanyStage
    scenario: FinancialScenario
    monthly_revenue: float
    employee_count: int
    funding_raised: float
    target_runway_months: int


class MockFinancialDataGenerator:
    """Generate realistic mock financial data for startups"""
    
    def __init__(self, company_profile: MockCompanyProfile = None):
        self.company_profile = company_profile or self._generate_default_profile()
        self.base_date = datetime.now() - timedelta(days=90)  # 3 months of history
        self.transactions_cache = []
        self.accounts_cache = []
        self._initialize_accounts()
        self._generate_transaction_history()
        
    def _generate_default_profile(self) -> MockCompanyProfile:
        """Generate a realistic default company profile"""
        scenarios = list(FinancialScenario)
        stages = list(CompanyStage)
        
        stage = random.choice(stages)
        scenario = random.choice(scenarios)
        
        # Realistic ranges based on stage
        stage_ranges = {
            CompanyStage.SEED: {"revenue": (5000, 25000), "employees": (3, 12), "funding": (250000, 2000000)},
            CompanyStage.SERIES_A: {"revenue": (20000, 100000), "employees": (8, 35), "funding": (2000000, 15000000)},
            CompanyStage.SERIES_B: {"revenue": (80000, 500000), "employees": (25, 100), "funding": (10000000, 50000000)},
            CompanyStage.GROWTH: {"revenue": (300000, 2000000), "employees": (75, 300), "funding": (25000000, 200000000)}
        }
        
        ranges = stage_ranges[stage]
        
        return MockCompanyProfile(
            name=random.choice(["TechFlow", "DataVault", "CloudScale", "AIForge", "FinanceFlow"]),
            stage=stage,
            scenario=scenario,
            monthly_revenue=random.uniform(*ranges["revenue"]),
            employee_count=random.randint(*ranges["employees"]),
            funding_raised=random.uniform(*ranges["funding"]),
            target_runway_months=random.randint(12, 24)
        )
    
    def _initialize_accounts(self):
        """Initialize mock bank accounts"""
        self.accounts_cache = [
            {
                "id": "acc_operating_001",
                "name": "Operating Account",
                "type": "checking",
                "balance": self._calculate_current_balance(),
                "currency": "USD",
                "status": "active"
            },
            {
                "id": "acc_savings_001", 
                "name": "Reserve Account",
                "type": "savings",
                "balance": self._calculate_reserve_balance(),
                "currency": "USD",
                "status": "active"
            }
        ]
    
    def _calculate_current_balance(self) -> float:
        """Calculate realistic current balance based on scenario"""
        base_monthly_burn = self._calculate_monthly_burn()
        
        scenario_multipliers = {
            FinancialScenario.HEALTHY_GROWTH: random.uniform(3.0, 6.0),  # 3-6 months runway
            FinancialScenario.CASH_CRUNCH: random.uniform(0.5, 2.0),    # 0.5-2 months runway
            FinancialScenario.RAPID_BURN: random.uniform(1.0, 3.0),     # 1-3 months runway
            FinancialScenario.SEASONAL_BUSINESS: random.uniform(2.0, 8.0), # Variable
            FinancialScenario.POST_FUNDING: random.uniform(8.0, 24.0)   # 8-24 months runway
        }
        
        multiplier = scenario_multipliers[self.company_profile.scenario]
        return base_monthly_burn * multiplier
    
    def _calculate_reserve_balance(self) -> float:
        """Calculate reserve account balance"""
        operating_balance = self.accounts_cache[0]["balance"] if self.accounts_cache else 100000
        return operating_balance * random.uniform(0.1, 0.3)  # 10-30% of operating
    
    def _calculate_monthly_burn(self) -> float:
        """Calculate realistic monthly burn rate"""
        # Base burn on employee count and stage
        per_employee_cost = {
            CompanyStage.SEED: 8000,      # $8k per employee
            CompanyStage.SERIES_A: 9500,  # $9.5k per employee
            CompanyStage.SERIES_B: 11000, # $11k per employee
            CompanyStage.GROWTH: 12500    # $12.5k per employee
        }
        
        base_burn = self.company_profile.employee_count * per_employee_cost[self.company_profile.stage]
        
        # Add other operational costs
        operational_costs = base_burn * random.uniform(0.3, 0.6)  # 30-60% additional costs
        
        # Adjust for scenario
        scenario_multipliers = {
            FinancialScenario.HEALTHY_GROWTH: random.uniform(0.8, 1.1),
            FinancialScenario.CASH_CRUNCH: random.uniform(0.7, 0.9),    # Trying to cut costs
            FinancialScenario.RAPID_BURN: random.uniform(1.2, 1.8),     # High spending
            FinancialScenario.SEASONAL_BUSINESS: random.uniform(0.6, 1.4),
            FinancialScenario.POST_FUNDING: random.uniform(1.1, 1.5)    # Scaling up
        }
        
        total_burn = (base_burn + operational_costs) * scenario_multipliers[self.company_profile.scenario]
        return total_burn
    
    def _generate_transaction_history(self):
        """Generate 90 days of realistic transaction history"""
        self.transactions_cache = []
        current_date = self.base_date
        monthly_burn = self._calculate_monthly_burn()
        daily_burn = monthly_burn / 30
        
        # Generate transactions for 90 days
        for day in range(90):
            transaction_date = current_date + timedelta(days=day)
            
            # Generate revenue transactions (less frequent, larger amounts)
            if random.random() < 0.15:  # 15% chance of revenue per day
                revenue_amount = self._generate_revenue_transaction()
                if revenue_amount > 0:
                    self.transactions_cache.append({
                        "id": f"txn_{uuid.uuid4().hex[:8]}",
                        "amount": {"amount": int(revenue_amount * 100), "currency": "USD"},
                        "description": random.choice([
                            "Customer Payment - Enterprise Plan",
                            "Subscription Revenue",
                            "Professional Services",
                            "API Usage Revenue",
                            "Annual Contract Payment"
                        ]),
                        "posted_at": transaction_date.isoformat(),
                        "merchant": {"name": "Revenue"},
                        "category": "revenue",
                        "type": "credit"
                    })
            
            # Generate expense transactions (more frequent, varied amounts)
            daily_expenses = self._generate_daily_expenses(daily_burn, transaction_date)
            self.transactions_cache.extend(daily_expenses)
            
            # Generate periodic large expenses
            if transaction_date.day == 1:  # Monthly expenses
                monthly_expenses = self._generate_monthly_expenses(transaction_date)
                self.transactions_cache.extend(monthly_expenses)
        
        # Sort transactions by date
        self.transactions_cache.sort(key=lambda x: x["posted_at"])
    
    def _generate_revenue_transaction(self) -> float:
        """Generate realistic revenue transaction"""
        base_revenue = self.company_profile.monthly_revenue / 30  # Daily average
        
        # Revenue varies based on scenario
        scenario_multipliers = {
            FinancialScenario.HEALTHY_GROWTH: random.uniform(0.8, 1.8),
            FinancialScenario.CASH_CRUNCH: random.uniform(0.3, 0.8),
            FinancialScenario.RAPID_BURN: random.uniform(0.9, 1.5),
            FinancialScenario.SEASONAL_BUSINESS: random.uniform(0.2, 2.5),
            FinancialScenario.POST_FUNDING: random.uniform(1.0, 2.0)
        }
        
        multiplier = scenario_multipliers[self.company_profile.scenario]
        return base_revenue * multiplier * random.uniform(0.5, 3.0)  # Transaction size variance
    
    def _generate_daily_expenses(self, daily_burn: float, transaction_date: datetime) -> List[Dict]:
        """Generate realistic daily expenses"""
        expenses = []
        remaining_burn = daily_burn
        
        # Small operational expenses throughout the day
        expense_count = random.randint(1, 8)
        
        for _ in range(expense_count):
            if remaining_burn <= 0:
                break
                
            # Varied expense sizes
            expense_amount = min(
                remaining_burn * random.uniform(0.05, 0.4),
                remaining_burn
            )
            
            expense_category, merchant_name = self._get_random_expense_category()
            
            expenses.append({
                "id": f"txn_{uuid.uuid4().hex[:8]}",
                "amount": {"amount": -int(expense_amount * 100), "currency": "USD"},
                "description": f"{merchant_name} - {expense_category}",
                "posted_at": (transaction_date + timedelta(hours=random.randint(9, 18))).isoformat(),
                "merchant": {"name": merchant_name, "mcc_description": expense_category},
                "category": expense_category.lower().replace(" ", "_"),
                "type": "debit"
            })
            
            remaining_burn -= expense_amount
        
        return expenses
    
    def _generate_monthly_expenses(self, transaction_date: datetime) -> List[Dict]:
        """Generate large monthly recurring expenses"""
        monthly_expenses = []
        
        # Payroll (biggest expense)
        payroll_amount = self.company_profile.employee_count * random.uniform(6000, 15000)
        monthly_expenses.append({
            "id": f"txn_{uuid.uuid4().hex[:8]}",
            "amount": {"amount": -int(payroll_amount * 100), "currency": "USD"},
            "description": "Payroll Processing",
            "posted_at": transaction_date.isoformat(),
            "merchant": {"name": "Gusto Payroll", "mcc_description": "Payroll Services"},
            "category": "payroll",
            "type": "debit"
        })
        
        # Office rent
        if self.company_profile.employee_count > 10:
            rent_amount = self.company_profile.employee_count * random.uniform(300, 800)
            monthly_expenses.append({
                "id": f"txn_{uuid.uuid4().hex[:8]}",
                "amount": {"amount": -int(rent_amount * 100), "currency": "USD"},
                "description": "Office Rent",
                "posted_at": transaction_date.isoformat(),
                "merchant": {"name": "WeWork", "mcc_description": "Real Estate"},
                "category": "office_rent",
                "type": "debit"
            })
        
        # Software subscriptions
        software_costs = [
            ("AWS", random.uniform(2000, 15000)),
            ("Salesforce", random.uniform(500, 3000)),
            ("Slack", random.uniform(200, 1500)),
            ("GitHub", random.uniform(100, 800)),
            ("Figma", random.uniform(200, 1000))
        ]
        
        for vendor, amount in software_costs:
            if random.random() < 0.7:  # 70% chance of having this subscription
                monthly_expenses.append({
                    "id": f"txn_{uuid.uuid4().hex[:8]}",
                    "amount": {"amount": -int(amount * 100), "currency": "USD"},
                    "description": f"{vendor} Subscription",
                    "posted_at": transaction_date.isoformat(),
                    "merchant": {"name": vendor, "mcc_description": "Software"},
                    "category": "software",
                    "type": "debit"
                })
        
        return monthly_expenses
    
    def _get_random_expense_category(self) -> tuple:
        """Get random expense category and merchant"""
        expense_types = {
            "Software": [
                "GitHub", "AWS", "Slack", "Zoom", "Notion", "Figma", 
                "Linear", "Vercel", "DataDog", "Stripe"
            ],
            "Office Supplies": [
                "Staples", "Amazon Business", "Office Depot", "Best Buy Business"
            ],
            "Marketing": [
                "Google Ads", "Facebook Ads", "LinkedIn Marketing", "HubSpot",
                "Mailchimp", "ConvertKit"
            ],
            "Travel": [
                "United Airlines", "Delta", "Uber", "Lyft", "Marriott", "Airbnb"
            ],
            "Meals": [
                "DoorDash", "Uber Eats", "Starbucks", "Sweetgreen", "Chipotle"
            ],
            "Professional Services": [
                "Legal Counsel", "Accounting Firm", "Consultants", "Recruiting Agency"
            ],
            "Utilities": [
                "Internet Provider", "Phone Service", "Electricity", "Water"
            ]
        }
        
        category = random.choice(list(expense_types.keys()))
        merchant = random.choice(expense_types[category])
        return category, merchant
    
    # Public API methods matching original Brex implementation
    def get_accounts(self) -> Dict[str, Any]:
        """Get mock account data"""
        return {
            "data": self.accounts_cache
        }
    
    def get_transactions(self, start_date: str = None, end_date: str = None, limit: int = 100) -> Dict[str, Any]:
        """Get mock transaction data"""
        transactions = self.transactions_cache.copy()
        
        # Apply date filtering if provided
        if start_date:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            transactions = [t for t in transactions if datetime.fromisoformat(t["posted_at"].replace('Z', '+00:00')) >= start_dt]
        
        if end_date:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            transactions = [t for t in transactions if datetime.fromisoformat(t["posted_at"].replace('Z', '+00:00')) <= end_dt]
        
        # Apply limit
        transactions = transactions[-limit:] if limit else transactions
        
        return {
            "data": transactions
        }
    
    def get_current_cash_flow_data(self) -> Dict[str, Any]:
        """Generate current cash flow analysis"""
        accounts_data = self.get_accounts()
        total_balance = sum(account["balance"] for account in accounts_data["data"])
        
        # Calculate burn rate from recent transactions
        recent_transactions = self.get_transactions(
            start_date=(datetime.now() - timedelta(days=30)).isoformat()
        )["data"]
        
        monthly_expenses = sum(
            abs(t["amount"]["amount"]) / 100
            for t in recent_transactions
            if t["amount"]["amount"] < 0
        )
        
        monthly_revenue = sum(
            t["amount"]["amount"] / 100
            for t in recent_transactions
            if t["amount"]["amount"] > 0
        )
        
        net_burn = monthly_expenses - monthly_revenue
        runway_days = int(total_balance / (net_burn / 30)) if net_burn > 0 else 999
        
        # Calculate burn rate change (simulate trend)
        burn_rate_change = self._calculate_burn_rate_change()
        
        return {
            "total_balance": total_balance,
            "burn_rate_monthly": net_burn,
            "runway_days": runway_days,
            "accounts": len(accounts_data["data"]),
            "last_updated": datetime.now().isoformat(),
            "burn_rate_change_percent": burn_rate_change,
            "monthly_revenue": monthly_revenue,
            "monthly_expenses": monthly_expenses,
            "scenario": self.company_profile.scenario.value,
            "company_stage": self.company_profile.stage.value
        }
    
    def _calculate_burn_rate_change(self) -> float:
        """Calculate realistic burn rate change based on scenario"""
        scenario_changes = {
            FinancialScenario.HEALTHY_GROWTH: random.uniform(-5, 10),     # Slight increase
            FinancialScenario.CASH_CRUNCH: random.uniform(-25, -5),      # Cutting costs
            FinancialScenario.RAPID_BURN: random.uniform(15, 45),        # Increasing spend
            FinancialScenario.SEASONAL_BUSINESS: random.uniform(-20, 30), # High variance
            FinancialScenario.POST_FUNDING: random.uniform(20, 60)       # Scaling up
        }
        
        return scenario_changes[self.company_profile.scenario]
    
    def get_large_recent_expenses(self, threshold: float = 5000) -> List[Dict]:
        """Get recent large expenses for monitoring"""
        recent_transactions = self.get_transactions(
            start_date=(datetime.now() - timedelta(days=7)).isoformat()
        )["data"]
        
        large_expenses = [
            t for t in recent_transactions
            if t["amount"]["amount"] < -threshold * 100  # Convert to cents
        ]
        
        return large_expenses
    
    def simulate_financial_alert_scenario(self, alert_type: str) -> Dict[str, Any]:
        """Simulate specific financial alert scenarios for testing"""
        
        if alert_type == "critical_runway":
            # Simulate critical cash runway scenario
            self.accounts_cache[0]["balance"] = 50000  # Very low balance
            return self.get_current_cash_flow_data()
        
        elif alert_type == "burn_rate_spike":
            # Add some large unexpected expenses
            large_expense = {
                "id": f"txn_alert_{uuid.uuid4().hex[:8]}",
                "amount": {"amount": -2500000, "currency": "USD"},  # $25k expense
                "description": "Emergency Infrastructure Scaling",
                "posted_at": datetime.now().isoformat(),
                "merchant": {"name": "AWS", "mcc_description": "Cloud Services"},
                "category": "infrastructure",
                "type": "debit"
            }
            self.transactions_cache.append(large_expense)
            return self.get_current_cash_flow_data()
        
        elif alert_type == "revenue_drop":
            # Simulate revenue decline
            self.company_profile.monthly_revenue *= 0.4  # 60% revenue drop
            return self.get_current_cash_flow_data()
        
        elif alert_type == "large_expense":
            return {"large_expenses": self.get_large_recent_expenses(1000)}
        
        return self.get_current_cash_flow_data()
    
    def get_expense_analysis(self) -> Dict[str, Any]:
        """Generate expense analysis"""
        recent_transactions = self.get_transactions(
            start_date=(datetime.now() - timedelta(days=30)).isoformat()
        )["data"]
        
        # Categorize expenses
        categories = {}
        for transaction in recent_transactions:
            if transaction["amount"]["amount"] < 0:  # Expense
                category = transaction.get("category", "other")
                amount = abs(transaction["amount"]["amount"]) / 100
                
                if category not in categories:
                    categories[category] = {
                        "total": 0,
                        "count": 0,
                        "transactions": []
                    }
                
                categories[category]["total"] += amount
                categories[category]["count"] += 1
                categories[category]["transactions"].append(transaction)
        
        # Sort by total spend
        sorted_categories = dict(sorted(
            categories.items(),
            key=lambda x: x[1]["total"],
            reverse=True
        ))
        
        return {
            "categories": sorted_categories,
            "total_transactions": len([t for t in recent_transactions if t["amount"]["amount"] < 0]),
            "analysis_date": datetime.now().isoformat(),
            "top_expense_category": list(sorted_categories.keys())[0] if sorted_categories else None
        }
    
    def update_scenario(self, new_scenario: FinancialScenario):
        """Update the financial scenario for testing different conditions"""
        self.company_profile.scenario = new_scenario
        self._initialize_accounts()  # Recalculate balances
        # Regenerate recent transactions with new scenario
        self.transactions_cache = self.transactions_cache[:-30]  # Keep older transactions
        current_date = datetime.now() - timedelta(days=30)
        
        # Generate new 30 days with new scenario
        monthly_burn = self._calculate_monthly_burn()
        daily_burn = monthly_burn / 30
        
        for day in range(30):
            transaction_date = current_date + timedelta(days=day)
            daily_expenses = self._generate_daily_expenses(daily_burn, transaction_date)
            self.transactions_cache.extend(daily_expenses)
            
            # Revenue transactions
            if random.random() < 0.15:
                revenue_amount = self._generate_revenue_transaction()
                if revenue_amount > 0:
                    self.transactions_cache.append({
                        "id": f"txn_{uuid.uuid4().hex[:8]}",
                        "amount": {"amount": int(revenue_amount * 100), "currency": "USD"},
                        "description": "Customer Payment",
                        "posted_at": transaction_date.isoformat(),
                        "merchant": {"name": "Revenue"},
                        "category": "revenue",
                        "type": "credit"
                    })
        
        self.transactions_cache.sort(key=lambda x: x["posted_at"])


# Pre-defined company profiles for different scenarios
DEMO_PROFILES = {
    "healthy_saas": MockCompanyProfile(
        name="HealthySaaS Co",
        stage=CompanyStage.SERIES_A,
        scenario=FinancialScenario.HEALTHY_GROWTH,
        monthly_revenue=85000,
        employee_count=25,
        funding_raised=8000000,
        target_runway_months=18
    ),
    
    "cash_crunch_startup": MockCompanyProfile(
        name="CrunchTime AI",
        stage=CompanyStage.SEED,
        scenario=FinancialScenario.CASH_CRUNCH,
        monthly_revenue=15000,
        employee_count=8,
        funding_raised=1200000,
        target_runway_months=6
    ),
    
    "post_funding_scale": MockCompanyProfile(
        name="ScaleUp Tech",
        stage=CompanyStage.SERIES_B,
        scenario=FinancialScenario.POST_FUNDING,
        monthly_revenue=250000,
        employee_count=75,
        funding_raised=25000000,
        target_runway_months=24
    ),
    
    "seasonal_ecommerce": MockCompanyProfile(
        name="Seasonal Commerce",
        stage=CompanyStage.SERIES_A,
        scenario=FinancialScenario.SEASONAL_BUSINESS,
        monthly_revenue=120000,
        employee_count=35,
        funding_raised=12000000,
        target_runway_months=15
    )
}