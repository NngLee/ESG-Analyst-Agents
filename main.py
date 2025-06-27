from model import ESGModel
from deepseek_api import generate_esg_commentary

model = ESGModel()
model.step()

for firm in model.firms:
    scores = model.get_firm_scores()[firm]
    disclosure = model.current_disclosures.get(firm, "暂无披露")
    summary = generate_esg_commentary(disclosure, scores)

    print(f"\nFirm {firm.unique_id}:")
    print(f"  ESG Score: {scores['esg_score']:.2f}, Rating: {scores['esg_rating']}")
    print(f"  Investment: {firm.investment_received:.2f}")
    print(summary)
