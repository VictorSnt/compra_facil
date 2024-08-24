#ext
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
#app
from src.controllers.order_controller import OrderControlle
from src.controllers.group_controller import GroupController
from src.controllers.person_controller import PersonController
from src.controllers.report_controller import ReportController
from src.controllers.family_controller import FamilyController
from src.controllers.product_controller import ProductController
from src.controllers.quotation_controller import QuotationController
from src.controllers.order_item_controller import OrderItemController
from src.controllers.quote_submit_controller import QuotationSubmitController
from src.controllers.quotation_item_controller import QuotationItemController

from src.model.models import (
    Product, Person, Docitem,
    Document, Family, Group,
    ProductInfo, Stock
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(OrderControlle.get_router())
app.include_router(GroupController.get_router())
app.include_router(PersonController.get_router())
app.include_router(ReportController.get_router())
app.include_router(FamilyController.get_router())
app.include_router(ProductController.get_router())
app.include_router(OrderItemController.get_router())
app.include_router(QuotationController.get_router())
app.include_router(QuotationItemController.get_router())
app.include_router(QuotationSubmitController.get_router())



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
