class MockModel:

    def predict(self, messages):
        results = []

        for message in messages:

            text = message.lower()

            if "card" in text:
                results.append("card_issue")
            elif "transfer" in text:
                results.append("transfer_issue")
            elif "cash" in text or "atm" in text:
                results.append("cash_withdrawal")
            else:
                results.append("unknown")

        return results

    def predict_proba(self, messages):
        return [
            [0.90, 0.05, 0.05]
            for _ in messages
        ]
