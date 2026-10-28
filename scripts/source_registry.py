
import pandas as pd
from pathlib import Path

sources = [
    {
        "source_id": "RBI_DIGITAL_SAFETY",
        "source_title": "Safeguards for Digital Banking",
        "source_publisher": "Reserve Bank of India",
        "source_url": "https://rbikehtahai.rbi.org.in/safeguards-for-digital-banking.html",
        "source_date": "",
        "content_type": "official_public_guidance",
        "source_status": "source_found",
        "supported_topics": "digital banking safety; lost or stolen card; banking credentials",
        "verification_notes": "Verify page content and current applicability before ingestion."
    },
    {
        "source_id": "RBI_DIGITAL_CYBER",
        "source_title": "Digital Banking Cyber Security",
        "source_publisher": "Reserve Bank of India",
        "source_url": "https://rbikehtahai.rbi.org.in/digital-banking-cyber-security.html",
        "source_date": "",
        "content_type": "official_public_guidance",
        "source_status": "source_found",
        "supported_topics": "passwords; PIN; OTP; suspicious links",
        "verification_notes": "Verify page content and current applicability before ingestion."
    },
    {
        "source_id": "NPCI_FRAUD_AWARENESS",
        "source_title": "Fraud Awareness",
        "source_publisher": "National Payments Corporation of India",
        "source_url": "https://www.npci.org.in/fraud-awareness",
        "source_date": "",
        "content_type": "official_public_guidance",
        "source_status": "source_found",
        "supported_topics": "digital payment fraud; QR code scams; social engineering",
        "verification_notes": "Verify page content and current applicability before ingestion."
    },
    {
        "source_id": "RBI_FAQ_INDEX",
        "source_title": "Reserve Bank of India FAQs",
        "source_publisher": "Reserve Bank of India",
        "source_url": "https://www.rbi.org.in/commonperson/english/Scripts/FAQs.aspx",
        "source_date": "",
        "content_type": "official_source_index",
        "source_status": "source_found",
        "supported_topics": "KYC; card transactions; payment systems; customer complaints",
        "verification_notes": "This is an index. Select and verify individual FAQ documents before ingestion."
    }
]

output_path = Path("data/knowledge_base/source_registry.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

df = pd.DataFrame(sources)
df.to_csv(output_path, index=False)

print(f"Sources registered: {len(df)}")
print(f"Saved to: {output_path}")
print(df[["source_id", "source_status", "source_title"]].to_string(index=False))
