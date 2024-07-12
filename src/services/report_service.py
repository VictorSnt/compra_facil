#std
from datetime import datetime
from typing import List
#app
from src.schemas.purchase_sugestion_schema import PurchaseSuggestionSchema
from src.calculators.purchase_sugestion_calc import PurchaseSuggestionCalc
from src.repository.product_repository import ProductRepository
from src.model.product import Product


class ReportService:

    def __init__(self, repository: ProductRepository) -> None:
        self.repo = repository

    def shopping_suggestion(
        self,
        product_ids: List[str]
    ) -> List[PurchaseSuggestionSchema]:

        products: List[Product] = (
            self.repo.find_products_with_current_stock(product_ids)
        )
        suggestions = []

        for product in products:
            try:
                suggestion = self._create_suggestion(product)
            except (ValueError, TypeError) as e:
                print(f"Ignorando produto inválido: {product.iddetalhe}, erro: {e}")
                continue

            suggestions.append(suggestion)

        return suggestions

    def _create_suggestion(self, product: Product):

        stock_obj = product.latest_stock
        qtstock = stock_obj.qtestoque if stock_obj else 0.0
        last_purchase = product.last_relevant_purchase(self.repo.session)
        days_since_last_purchase = (datetime.now() - last_purchase).days

        sales_after = product.sales_after_period(self.repo.session, last_purchase)

        avg_sales_daily = PurchaseSuggestionCalc.calculate_avg_sales_daily(
            sales_after, days_since_last_purchase
        )

        demand_variance = product.daily_demand_variance(
            self.repo.session, last_purchase
        )
        security_stock = PurchaseSuggestionCalc.calculate_security_stock(
            demand_variance
        )

        reposition_period = 60
        avg_sales = PurchaseSuggestionCalc.calculate_avg_sales(
            avg_sales_daily, reposition_period
        )

        quantity_to_buy = PurchaseSuggestionCalc.calculate_quantity_to_buy(
            avg_sales, security_stock, qtstock
        )
        days_of_supply = PurchaseSuggestionCalc.calculate_days_of_supply(
            qtstock, avg_sales_daily
        )

        return PurchaseSuggestionSchema(
            cdprincipal=str(product.cdprincipal),
            dsdetalhe=str(product.dsdetalhe),
            stock=qtstock,
            dias_suprimento=days_of_supply,
            sugestao=quantity_to_buy,
            dtreferencia=last_purchase.strftime('%d/%m/%Y'),
            sales=sales_after,
            security_stock=security_stock,
            avg_sales_daily=avg_sales_daily,
            avg_sales_60_days=avg_sales
        )
