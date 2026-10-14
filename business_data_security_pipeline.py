# ================================
# BUSINESS SECURITY AND RISK DATA PIPELINE
# ================================

# 1. Import Libraries
import datetime

# ================================
# MOCK PANDAS IMPLEMENTATION
# ================================

class MockDataFrame:
    """Mock DataFrame for testing without pandas dependency."""

    def __init__(self, data):
        self.data = data or []
        if self.data and isinstance(self.data[0], dict):
            self.columns = list(self.data[0].keys())
        else:
            self.columns = []

    def to_csv(self, filename, index=False):
        """Mock CSV export."""
        if not self.data:
            return

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(','.join(self.columns) + '\n')
            for row in self.data:
                values = [str(row.get(col, '')) for col in self.columns]
                f.write(','.join(values) + '\n')

    def __str__(self):
        """Mock string representation."""
        if not self.data:
            return "Empty DataFrame"

        col_widths = {col: len(col) for col in self.columns}
        for row in self.data:
            for col in self.columns:
                col_widths[col] = max(col_widths[col], len(str(row.get(col, ''))))

        lines = []
        header = '  '.join(col.ljust(col_widths[col]) for col in self.columns)
        lines.append(header)
        lines.append('  '.join('-' * col_widths[col] for col in self.columns))

        for idx, row in enumerate(self.data):
            row_str = '  '.join(str(row.get(col, '')).ljust(col_widths[col]) for col in self.columns)
            lines.append(f"{idx}  {row_str}")

        return '\n'.join(lines)


class MockPandas:
    """Mock pandas module."""

    @staticmethod
    def DataFrame(data):
        return MockDataFrame(data)


pd = MockPandas()

# ================================
# 2. INPUT
# ================================
companies = [
    "Company A - ZEUS IT Solutions LTD",
    "Company B - ATHRODITIE CYBER DEVOPS LIMITED",
    "Company C - DEMETER SUPPLY CHAIN TECHNOLOGY SOLUTIONS LTD"
]

# ================================
# 3. DATA COLLECTION (EXTRACTION)
# ================================

def get_company_info(company_name):
    """Simulated Companies House API call."""
    mock_data = {
        "Company A - ZEUS IT Solutions LTD": {"revenue": 1200000, "years_active": 5},
        "Company B - ATHRODITIE CYBER DEVOPS LIMITED": {"revenue": 500000, "years_active": 1},
        "Company C - DEMETER SUPPLY CHAIN TECHNOLOGY SOLUTIONS LTD": {"revenue": 2500000, "years_active": 10}
    }
    return mock_data.get(company_name, {})


def get_news(company_name):
    """Simulated news extraction."""
    mock_news = {
        "Company A - ZEUS IT Solutions LTD": [
            "Positive earnings but cybersecurity regulatory warnings"
        ],
        "Company B - ATHRODITIE CYBER DEVOPS LIMITED": [
            "Multiple Security Breaches reported and delivery delays"
        ],
        "Company C - DEMETER SUPPLY CHAIN TECHNOLOGY SOLUTIONS LTD": [
            "Stable operations and strong supplier performance"
        ]
    }
    return mock_news.get(company_name, [])


# ================================
# 4. DATA TRANSFORMATION
# ================================

def clean_data(company_info):
    """Normalize and clean data."""
    if not isinstance(company_info, dict):
        return {"revenue": 0.0, "years_active": 0}

    return {
        "revenue": float(company_info.get("revenue", 0) or 0),
        "years_active": int(company_info.get("years_active", 0) or 0)
    }


def normalize_news_items(news_items):
    """Ensure text items are in a list format."""
    if news_items is None:
        return []
    if isinstance(news_items, str):
        return [news_items]
    if not isinstance(news_items, list):
        return [str(news_items)]
    return [str(item) for item in news_items]


# ================================
# 5. RISK SCORING
# ================================

def risk_score(data, news_items):
    """Assign a supplier risk score from company and news data."""
    cleaned = clean_data(data)
    score = 0

    if cleaned["years_active"] < 2:
        score += 2

    if cleaned["revenue"] < 600000:
        score += 2

    for news in normalize_news_items(news_items):
        news_lower = news.lower()

        if "breach" in news_lower or "incident" in news_lower or "cyberattack" in news_lower:
            score += 5
        if "complaint" in news_lower:
            score += 3
        if "issue" in news_lower or "delay" in news_lower:
            score += 2
        if "warning" in news_lower or "regulatory" in news_lower:
            score += 2
        if "vulnerability" in news_lower or "threat" in news_lower:
            score += 3

    return min(score, 20)


# ================================
# 6. AI ANALYSIS (SIMULATED)
# ================================

def ai_summary(news_items, company_info, score):
    """Simulated AI summary."""
    news_text = " ".join(normalize_news_items(news_items)).lower()

    if score >= 7 or "breach" in news_text or "cyberattack" in news_text:
        return "High risk: Security incidents, operational disruption, or reputational damage detected."
    elif score >= 3:
        return "Moderate risk: Some issues identified, monitoring recommended."
    else:
        return "Low risk: Supplier appears stable with no major concerns."


# ================================
# 7. AUTOMATED QUESTIONNAIRE SECTION
# ================================

def ask_yes_no_question(question_text):
    """Prompt the user and ensure a valid yes/no answer."""
    while True:
        answer = input(f"{question_text} (yes/no): ").strip().lower()
        if answer in ["yes", "y"]:
            return True
        if answer in ["no", "n"]:
            return False
        print("Please answer with 'yes' or 'no'.")


def questionnaire_risk(answers):
    """Score the questionnaire responses."""
    score = 0

    if answers.get("data_breach"):
        score += 5
    if answers.get("security_policy") is False:
        score += 2
    if answers.get("security_training") is False:
        score += 2
    if answers.get("vendor_monitoring") is False:
        score += 2
    if answers.get("incident_response") is False:
        score += 2
    if answers.get("audit_check") is False:
        score += 2

    if score >= 7:
        risk_level = "High"
    elif score >= 4:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return score, risk_level


def run_questionnaire(company_name):
    """Run an automated security questionnaire for a supplier."""
    print(f"\n--- Supplier Security Questionnaire: {company_name} ---")

    answers = {
        "data_breach": ask_yes_no_question("Has the company reported any data breach or major cybersecurity incident in the last 12 months?"),
        "security_policy": ask_yes_no_question("Does the company maintain a formal cybersecurity policy and access control process?"),
        "security_training": ask_yes_no_question("Does the company provide regular cybersecurity awareness training to staff?"),
        "vendor_monitoring": ask_yes_no_question("Does the company monitor third-party and supplier security risks?"),
        "incident_response": ask_yes_no_question("Does the company have an incident response and recovery procedure?"),
        "audit_check": ask_yes_no_question("Has the company completed a recent external security or compliance audit?")
    }

    questionnaire_score, risk_level = questionnaire_risk(answers)

    print("\nQuestionnaire results:")
    for key, value in answers.items():
        print(f"- {key}: {'Yes' if value else 'No'}")

    print(f"Questionnaire Risk Score: {questionnaire_score}")
    print(f"Questionnaire Risk Level: {risk_level}")

    return {
        "Company": company_name,
        "Questionnaire Score": questionnaire_score,
        "Questionnaire Risk Level": risk_level,
        "Answers": answers
    }


# ================================
# 8. PIPELINE EXECUTION
# ================================

def run_pipeline():
    results = []

    for company in companies:
        print(f"Processing: {company}")

        info = get_company_info(company)
        news = get_news(company)
        cleaned_data = clean_data(info)
        score = risk_score(cleaned_data, news)
        summary = ai_summary(news, cleaned_data, score)

        results.append({
            "Company": company,
            "Revenue": cleaned_data["revenue"],
            "Years Active": cleaned_data["years_active"],
            "Risk Score": score,
            "Risk Level": (
                "High" if score >= 7 else
                "Medium" if score >= 3 else
                "Low"
            ),
            "AI Summary": summary,
            "Processed Date": datetime.datetime.now().strftime("%Y-%m-%d")
        })

    return results


# ================================
# 9. OUTPUT
# ================================

def save_results(results):
    df = pd.DataFrame(results)
    df.to_csv("supplier_risk_report.csv", index=False)

    print("\nPipeline complete.")
    print("Results saved to supplier_risk_report.csv\n")
    print(df)


# ================================
# RUN PIPELINE
# ================================

if __name__ == "__main__":
    results = run_pipeline()
    save_results(results)

    print("\nAutomated supplier questionnaires are now starting...\n")
    for company in companies:
        run_questionnaire(company)