import pandas as pd


class AnalyticsService:

    @staticmethod
    def analyze_csv(filepath):

        df = pd.read_csv(filepath)

        total_cost = float(df["Cost"].sum())

        highest_row = df.loc[df["Cost"].idxmax()]

        highest_service = highest_row["Service"]

        highest_cost = float(highest_row["Cost"])

        average_cost = round(float(df["Cost"].mean()), 2)

        total_services = len(df)

        if total_cost <= 5000:
            health_score = 95
        elif total_cost <= 10000:
            health_score = 85
        else:
            health_score = 70

        estimated_savings = round(total_cost * 0.15, 2)

        return {
            "total_cost": total_cost,
            "highest_service": highest_service,
            "highest_cost": highest_cost,
            "average_cost": average_cost,
            "total_services": total_services,
            "health_score": health_score,
            "estimated_savings": estimated_savings
        }