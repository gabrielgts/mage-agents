from crewai.tools import BaseTool
from magento import Client
from magento.search import ProductSearch, OrderSearch
from typing import Any, Optional, Type

class MagentoProductSearchTool(BaseTool):
    """
    Tool para interação com a API do Magento 2 usando MyMagento.
    Permite buscar produtos.
    """
    def __init__(self, product_att: str, product_ref: str):
        super().__init__()
        self.client = Client(domain="https://magento.test", username="gabriel", password="teste123@", local=True, login=False, token="xzzxlxqx4jdh7rqfmx1ra43adjt1h567")
        self.product_ref = product_ref
        self.product_att = product_att

    def search_product(self):
        """Busca um produto pelo SKU no Magento."""
        product_search = ProductSearch(self.client)
        result = product_search.add_criteria({self.product_att: self.product_ref}).execute()
        return result[0] if result else "Produto não encontrado."
    
    def _run(self, search_query: str, **kwargs: Any) -> Any:
        return super()._run(query=search_query, **kwargs)

class MagentoProductCreationTool(BaseTool):
    """
    Tool para interação com a API do Magento 2 usando MyMagento.
    Permite criar produtos.
    """
    def __init__(self, sku: str, name: str, price: float, description: str):
        super().__init__()
        self.client = Client(domain="https://magento.test", username="gabriel", password="teste123@", local=True, login=False, token="xzzxlxqx4jdh7rqfmx1ra43adjt1h567")
        self.sku = sku
        self.name = name
        self.price = price
        self.description = description
        
    def create_product(self):
        """Cria um novo produto no Magento."""
        new_product = {
            "sku": self.sku,
            "name": self.name,
            "price": self.price,
            "status": 1,
            "visibility": 4,
            "type_id": "simple",
            "attribute_set_id": 4,
            "custom_attributes": [
                {"attribute_code": "description", "value": self.description}
            ]
        }
        response = self.client.post("products", data=new_product)
        return response.json() if response.ok else f"Erro ao criar o produto: {response.text}"

    def _run(self, search_query: str, **kwargs: Any) -> Any:
    return super()._run(query=search_query, **kwargs)

    def update_stock(self, sku: str, qty: int):
        """Atualiza o estoque de um produto no Magento."""
        response = self.client.post(f'stockItems/{sku}', data={"qty": qty, "is_in_stock": True})
        return "Estoque atualizado com sucesso!" if response.ok else f"Erro ao atualizar estoque: {response.text}"

    def list_orders(self):
        """Lista pedidos recentes no Magento."""
        order_search = OrderSearch(self.client)
        result = order_search.get_all()
        return [{"order_id": order.increment_id, "status": order.status} for order in result]
    
