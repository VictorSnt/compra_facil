from typing import List, Dict
from collections import defaultdict

from src.schemas.quotation_schema import GetQuotationSubmit, Item, UserQuotation

class QuotationProcessor:
    def __init__(self):
        self.user_data: Dict[int, Dict] = defaultdict(lambda: {
            "user_id": None,
            "user_name": None,
            "submited_count": 0,
            "cheaper_items_count": 0,
            "total": 0.0,
            "quotation_items_count": 0,
            "items": [],
            "cheaper_items_list": []
        })
        self.item_price_map: defaultdict[str, List[tuple]] = defaultdict(list)

    def process_quotations(self, quotations: List[GetQuotationSubmit]) -> List[UserQuotation]:
        self._process_quotations_data(quotations)
        quotations_data = self._generate_quotations_data()
        return quotations_data

    def _process_quotations_data(self, quotations: List[GetQuotationSubmit]) -> None:
        quotations = [quote.model_dump() for quote in quotations]

        for quotation in quotations:
            user_id = quotation.get("user_id")
            user_name = quotation.get("user_name")
            items = quotation.get("items", [])
            quotation_qtitems = len(items)

            filtered_items = [item for item in items if item.get("qtitem") is not None and item.get("item_price") is not None]

            if user_id is None:
                raise ValueError("User ID should not be None")

            self.user_data[user_id]["user_id"] = user_id
            self.user_data[user_id]["user_name"] = user_name
            self.user_data[user_id]["submited_count"] += len(filtered_items)
            self.user_data[user_id]["total"] += round(sum(item["item_price"] * item["qtitem"] for item in filtered_items), 2)
            self.user_data[user_id]["quotation_items_count"] = quotation_qtitems
            self.user_data[user_id]["items"].extend(filtered_items)

            for item in filtered_items:
                item_name = item["item_name"]
                qtitem = item["qtitem"]
                item_price = item["item_price"]
                self.item_price_map[item_name].append((user_id, item_price))

        for item_name, prices in self.item_price_map.items():
            min_price = min(prices, key=lambda x: x[1])[1]
            for user_id, price in prices:
                if price == min_price:
                    self.user_data[user_id]["cheaper_items_count"] += 1
                    self.user_data[user_id]["cheaper_items_list"].append(item_name)

    def _generate_quotations_data(self) -> List[UserQuotation]:
        quotations_data = []
        for user_id, data in self.user_data.items():
            quotation_data = UserQuotation(
                user_id=user_id,
                user_name=data["user_name"],
                submited_count=data["submited_count"],
                cheaper_items_count=data["cheaper_items_count"],
                total=data["total"],
                quotation_items_count=data["quotation_items_count"],
                items=[Item(**item) for item in data["items"]],
                cheaper_items_list=data["cheaper_items_list"]
            )
            quotations_data.append(quotation_data)
        return quotations_data
