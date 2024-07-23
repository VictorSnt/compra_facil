#std
from datetime import datetime
import json
from typing import List
#app
from src.exceptions.err import NotFoundException
from src.schemas.purchase_suggestion_schema import PurchaseSuggestionSchema
from src.calculators.purchase_suggestion_calc import PurchaseSuggestionCalc
from src.database.redis_cache_maker import RedisConnection
from src.repository.product_repository import ProductRepository
from src.model.product import Product


class ReportService:
    def __init__(self, repository: ProductRepository) -> None:
        self.repo = repository
        self.redis_conn = RedisConnection

    def shopping_suggestion(
        self, product_ids: List[str]
    ) -> List[PurchaseSuggestionSchema]:
        try:
            with self.redis_conn() as redis:
                redis_keys = [f'suggestion:{id}' for id in product_ids]
                results = redis.get_all(redis_keys)
            redis_reponse = [json.loads(data) for data in results]
            suggestions = PurchaseSuggestionSchema.bulk_instanceate(
                redis_reponse
            )
            return sorted(suggestions, key=lambda s: s.sugestao, reverse=True)
        except Exception as e:
            print(f"Erro ao buscar sugestões do cache: {e}")
            return []

    def cache_suggestions(
            self, repositions_days: int
        ) -> List[PurchaseSuggestionSchema]:

        products = self.repo.find_active_products()
        suggestions = []
        try:
            with self.redis_conn() as redis:
                errors = []
                for product in products:
                    try:
                        suggestion = self._create_suggestion(
                            product, repositions_days
                        )
                        cache_key = f"suggestion:{product.iddetalhe}"
                        suggestion_json = suggestion.model_dump()
                        redis.set(cache_key, json.dumps(suggestion_json))
                        suggestions.append(suggestion)
                    except (Exception) as e:
                        print(e)
                        errors.append(product.iddetalhe)
                        continue
                if errors:
                    redis_key = 'erros'
                    redis.set(redis_key, json.dumps(errors))

        except Exception as e:
            print(f"Erro ao cachear sugestões: {e}")

        return suggestions

    def generate_quote(self):
        product_ids = [
            prod.iddetalhe for prod in 
            self.repo.find_active_products()
        ]
        current_suggestions = self.shopping_suggestion(product_ids)
        quote = [suggestion for suggestion in current_suggestions]
        return sorted(quote, key= lambda sugg: datetime.strptime(
            sugg.dtreferencia, '%d/%m/%Y'), reverse=True
        )

    def find_similar_products(self, iddetalhe: str):
        product = self.repo.find_by_id(iddetalhe)
        if not product: return []
        fist_word = str(product.dsdetalhe).split(' ', maxsplit=1)[0].upper()
        matchs = self.repo.find_similar_products(fist_word, product.idfamilia)

        if not matchs:
            raise NotFoundException

        match_ids = [prod.iddetalhe for prod in matchs]
        match_suggestions = self.shopping_suggestion(match_ids)
        return match_suggestions

    def _create_suggestion(
        self, product: Product,
        reposition_period: int
    ) -> PurchaseSuggestionSchema:

        qtstock = product.stock_plus_orders(self.repo.session)
        last_purchase = product.last_relevant_purchase(self.repo.session)
        days_since_last_purchase = (datetime.now() - last_purchase).days

        sales_after = (
            product.sales_after_period(self.repo.session, last_purchase)
        )
        avg_sales_daily = (
            PurchaseSuggestionCalc.calculate_avg_sales_daily(
                sales_after, days_since_last_purchase
            )
        )
        demand_variance = (
            product.daily_demand_variance(self.repo.session, last_purchase)
        )
        security_stock = (
            PurchaseSuggestionCalc.calculate_security_stock(demand_variance)
        )

        avg_sales = (
            PurchaseSuggestionCalc.calculate_avg_sales(
                avg_sales_daily, reposition_period
            )
            )

        quantity_to_buy = (
            PurchaseSuggestionCalc.calculate_quantity_to_buy(
                avg_sales, security_stock, qtstock
            )
        )
        days_of_supply = (
            PurchaseSuggestionCalc.calculate_days_of_supply(
                qtstock, avg_sales_daily
            )
        )

        return PurchaseSuggestionSchema(
            iddetalhe=str(product.iddetalhe),
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
