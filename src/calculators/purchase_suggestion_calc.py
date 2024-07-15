class PurchaseSuggestionCalc:

    @classmethod
    def calculate_avg_sales_daily(
        cls,
        sales_after: float,
        days_since_last_purchase: int
    ) -> float:

        if days_since_last_purchase <= 0:
            return 0
        if sales_after <= 0:
            return 0
        return sales_after / days_since_last_purchase

    @classmethod
    def calculate_security_stock(
        cls,
        demand_variance: float,
        points_of_security: float = 1.65
    ) -> float:

        if demand_variance < 0:
            raise ValueError("demand_variance must be non-negative")
        if points_of_security <= 0:
            raise ValueError("points_of_security must be greater than 0")
        return points_of_security * demand_variance

    @classmethod
    def calculate_avg_sales(cls, avg_sales_daily: float, reposition_period: int) -> float:
        if avg_sales_daily < 0:
            raise ValueError("avg_sales_daily must be non-negative")
        if reposition_period <= 0:
            raise ValueError("reposition_period must be greater than 0")
        return avg_sales_daily * reposition_period

    @classmethod
    def calculate_quantity_to_buy(
        cls,
        avg_sales: float,
        security_stock: float,
        stock: float
    ) -> float:

        if avg_sales < 0:
            raise ValueError("avg_sales must be non-negative")
        if security_stock < 0:
            raise ValueError("security_stock must be non-negative")
        if stock < 0:
            raise ValueError("stock must be non-negative")
        quantity_to_buy = avg_sales + security_stock - stock
        return max(quantity_to_buy, 0)

    @classmethod
    def calculate_days_of_supply(cls, stock: float, avg_sales_daily: float) -> float:
        if stock <= 0:
            return 0
        if avg_sales_daily <= 0:
            return 0
        return stock / avg_sales_daily
