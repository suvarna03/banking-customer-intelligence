
import pandas as pd
from pathlib import Path

data_path = Path("data/raw/banking77_train.csv")
output_path = Path("artifacts/phase_5/intent_knowledge_coverage.csv")

df = pd.read_csv(data_path)

intent_inventory = (
    df.groupby("category")
    .agg(
        sample_count=("text", "size"),
        sample_queries=("text", lambda x: " | ".join(x.head(3)))
    )
    .reset_index()
    .rename(columns={"category": "intent"})
    .sort_values("intent")
)

intent_inventory["knowledge_topic"] = ""
intent_inventory["source_status"] = "not_reviewed"
intent_inventory["source_title"] = ""
intent_inventory["source_publisher"] = ""
intent_inventory["source_url"] = ""
intent_inventory["source_date"] = ""
intent_inventory["content_type"] = ""
intent_inventory["coverage_notes"] = ""

output_path.parent.mkdir(parents=True, exist_ok=True)
intent_inventory.to_csv(output_path, index=False)

print(f"Total intents: {len(intent_inventory)}")
print(f"Output saved to: {output_path}")
print("\nSample rows:")
print(intent_inventory[["intent", "sample_count", "sample_queries"]].head(5).to_string(index=False))
