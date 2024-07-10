
from fastapi import FastAPI
from src.controllers.family_controller import FamilyController
from src.controllers.group_controller import GroupController
from src.controllers.person_controller import PersonController
from src.controllers.product_controller import ProductController
from src.model.models import *


app = FastAPI()

app.include_router(FamilyController.get_router())
app.include_router(GroupController.get_router())
app.include_router(PersonController.get_router())
app.include_router(ProductController.get_router())


# @app.get("/informacoes")
# async def informacoes():
#     if report_path.exists():
#         with open(report_path, 'r') as file:
#             result = json.load(file)
#         return templates.TemplateResponse("prod_list.html", {"request": request, "products": result})
#     else:
#         return {'message': 'O relatório não foi gerado, tente novamente'}


# @app.get("/create_spreadsheet")
# async def create_spreadsheet(data: str):
#     parsed_data = json.loads(data)
#     parsed_data.sort(key=lambda x: x['descricao'])
#     wb = Workbook()
#     sheet = wb.active
#     sheet['A1'] = 'codigo'
#     sheet['B1'] = 'descricao'
#     sheet['C1'] = 'compra'
#     sheet['D1'] = 'vl final'
#     sheet['E1'] = 'vl sugestao'

#     for index, item in enumerate(parsed_data, start=2):
#         sheet[f'A{index}'] = item['codigo']
#         sheet[f'B{index}'] = item['descricao']
#         sheet[f'C{index}'] = item['compra']
#         sheet[f'D{index}'] = ''
#         sheet[f'E{index}'] = ''

#     wb.save(spreadsheet_path)
#     return {'ok': True}


# @app.get("/download_spreadsheet")
# async def download_spreadsheet():
#     return FileResponse(spreadsheet_path)


# @app.post("/process_sheet")
# async def process_sheet(file: UploadFile = File(...)):
#     if file.filename.endswith('.xlsx'):
#         workbook = load_workbook(file.file)
#         sheet = workbook.active
#         data = []
#         headers = [cell.value for cell in sheet[1]]

#         for row in sheet.iter_rows(min_row=2, values_only=True):
#             row_data = {}
#             for header, value in zip(headers, row):
#                 row_data[header] = value
#             data.append(row_data)

#         return {'data': data}
#     else:
#         raise HTTPException(status_code=400, detail='Arquivo inválido')


# @app.get("/carregar_planilha")
# async def carregar_planilha():
#     return templates.TemplateResponse("load_sheet.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
