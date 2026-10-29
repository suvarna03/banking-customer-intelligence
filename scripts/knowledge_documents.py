
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
    
    {
        "document_id": "NPCI_UPI_001",
        "title": "Failed UPI transaction and refund guidance",
        "publisher": "National Payments Corporation of India",
        "source_url": "https://www.npci.org.in/what-we-do/upi/faqs",
        "content": (
            "If a UPI transaction fails and the payer's bank account is "
            "debited, the amount should be refunded. NPCI advises contacting "
            "the bank if the refund is not received within one hour. "
            "Customers should check the transaction status and follow the "
            "applicable grievance process."
        ),
        "content_type": "official_public_guidance",
        "verification_status": "source_content_checked",
        "supported_topics": (
            "UPI; failed transaction; account debited; refund; "
            "transaction status; complaint"
        ),
    },
    {
        "document_id": "RBI_TAT_001",
        "title": "Reversal timelines for failed payment transactions",
        "publisher": "Reserve Bank of India",
        "source_url": (
            "https://www.rbi.org.in/commonman/Upload/English/Notification/"
            "PDFs/CIRCULAR677EC931A7A65E4D99AA957D8E85BC0A2A.PDF"
        ),
        "content": (
            "RBI specifies reversal timelines for particular failed "
            "payment scenarios. For a UPI funds transfer where the payer "
            "is debited but the beneficiary is not credited, the specified "
            "auto-reversal timeline is T+1 day. For a merchant payment "
            "where the account is debited but confirmation is not received "
            "at the merchant location, the specified timeline is T+5 days. "
            "The applicable timeline depends on the transaction type."
        ),
        "content_type": "official_public_guidance",
        "verification_status": "source_content_checked",
        "supported_topics": (
            "failed transaction; UPI reversal; T+1; T+5; "
            "merchant payment; reversal timeline"
        ),
    },
    {
        "document_id": "RBI_UNAUTH_001",
        "title": "Reporting unauthorized electronic banking transactions",
        "publisher": "Reserve Bank of India",
        "source_url": (
            "https://rbi.org.in/scripts/NotificationUser.aspx?Id=11188"
        ),
        "content": (
            "Customers should report unauthorized electronic banking "
            "transactions to their bank immediately after noticing them. "
            "Banks must provide channels for reporting these transactions "
            "and take steps to prevent further unauthorized transactions "
            "after receiving a report. Customer liability depends on the "
            "circumstances and applicable RBI rules, including reporting time."
        ),
        "content_type": "official_public_guidance",
        "verification_status": "source_content_checked",
        "supported_topics": (
            "unauthorized transaction; electronic banking fraud; "
            "report fraud; customer liability; bank complaint"
        ),
    },

]


output_path = Path("data/knowledge_base/documents.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

df = pd.DataFrame(documents)

if df["document_id"].duplicated().any():
    duplicates = df.loc[
        df["document_id"].duplicated(),
        "document_id"].tolist()
    raise ValueError(f"Duplicate document IDs found: {duplicates}")

df.to_csv(output_path, index=False)

print(f"Documents created: {len(df)}")
print("Official guidance documents:",
    (df["content_type"] == "official_public_guidance").sum())
print("Synthetic test documents:",
    (df["content_type"] == "synthetic_test").sum())
print(f"Saved to: {output_path}")

