from model import ESGModel

if __name__ == "__main__":
    model = ESGModel(N_firms=3, N_investors=2)
    for i in range(3):
        print(f"\nStep {i+1}")
        model.step()
        for f in model.firms:
            print(f"Firm {f.unique_id} received investment: {f.investment_received:.2f}")