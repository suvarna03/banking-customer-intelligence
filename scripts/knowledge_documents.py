
import pandas as pd
from pathlib import Path

documents = [
    {
        "document_id": "RBI_SAFE_001",
        "title": "Protect banking credentials",
        "publisher": "Reserve Bank of India",
        "source_url": "https://rbikehtahai.rbi.org.in/safeguards-for-digital-banking.html",
        "content": (
            "Never share your banking password, PIN, OTP, CVV or UPI PIN "
            "with anyone. Register your mobile number and email with your "
            "bank to receive transaction alerts. Use verified and trusted "
            "websites for online banking."
        ),
        "content_type": "official_public_guidance",
        "verification_status": "source_content_checked",
        "supported_topics": "banking security; PIN; OTP; passwords; transaction alerts",
    },
    {
        "document_id": "RBI_SAFE_002",
        "title": "Lost or stolen payment card",
        "publisher": "Reserve Bank of India",
        "source_url": "https://rbikehtahai.rbi.org.in/safeguards-for-digital-banking.html",
        "content": (
            "If an ATM card, debit card, credit card or prepaid card is "
            "lost or stolen, block the card immediately."
        ),
        "content_type": "official_public_guidance",
        "verification_status": "source_content_checked",
        "supported_topics": "lost card; stolen card; compromised card",
    },
    {
        "document_id": "RBI_CYBER_001",
        "title": "Avoid suspicious banking links",
        "publisher": "Reserve Bank of India",
        "source_url": "https://rbikehtahai.rbi.org.in/digital-banking-cyber-security.html",
        "content": (
            "Do not share passwords, PINs, OTPs or CVVs over phone or online. "
            "Do not click suspicious links received through SMS, email "
            "or social media."
        ),
        "content_type": "official_public_guidance",
        "verification_status": "source_content_checked",
        "supported_topics": "phishing; suspicious links; banking credentials",
    },
    {
        "document_id": "NPCI_FRAUD_001",
        "title": "Recognise digital payment fraud",
        "publisher": "National Payments Corporation of India",
        "source_url": "https://www.npci.org.in/fraud-awareness",
        "content": (
            "Be cautious of fake cashback links, QR codes from unknown "
            "people, unknown applications, fake investment schemes and "
            "messages designed to deceive payment users. Scanning a QR "
            "code and entering a UPI PIN is for making a payment, "
            "not for receiving money."
        ),
        "content_type": "official_public_guidance",
        "verification_status": "source_content_checked",
        "supported_topics": "UPI; QR codes; cashback scams; payment fraud",
    },
    {
        "document_id": "TEST_REFUND_001",
        "title": "Synthetic test: refund status",
        "publisher": "Project test fixture",
        "source_url": "",
        "content": (
            "This is synthetic test content, not a real banking policy. "
            "A customer asks about a missing refund. The system should "
            "explain that refund timing depends on the merchant and "
            "payment provider and direct the customer to the relevant "
            "merchant or provider for transaction-specific status."
        ),
        "content_type": "synthetic_test",
        "verification_status": "synthetic_not_a_policy",
        "supported_topics": "refund; refund not received",
    },
    {
        "document_id": "TEST_UNSUPPORTED_001",
        "title": "Synthetic test: unsupported bank-specific fee",
        "publisher": "Project test fixture",
        "source_url": "",
        "content": (
            "This is a synthetic fallback test, not a real banking policy. "
            "It does not establish any actual bank's fees, charges or "
            "transaction limits. If a customer asks for an unsupported "
            "bank-specific fee, the system should request the bank name "
            "or refer the customer to the bank's official fee schedule."
        ),
        "content_type": "synthetic_test",
        "verification_status": "synthetic_not_a_policy",
        "supported_topics": "unsupported question; bank-specific fees; fallback",
    },
]

output_path = Path("data/knowledge_base/documents.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

df = pd.DataFrame(documents)
df.to_csv(output_path, index=False)

print(f"Documents created: {len(df)}")
print(f"Official guidance documents: {(df['content_type'] == 'official_public_guidance').sum()}")
print(f"Synthetic test documents: {(df['content_type'] == 'synthetic_test').sum()}")
print(f"Saved to: {output_path}")
