from crewai.tools import BaseTool
from magento import Client
from magento.search import ProductSearch, OrderSearch

class MagentoTool(BaseTool):
    """
    Tool para interação com a API do Magento 2 usando MyMagento.
    Permite buscar, criar e atualizar produtos, além de listar pedidos.
    """
    
    client = Client(domain="https://mageos.test", username="gabriel", password="teste123@", local=True)

    def search_product(self, sku: str):
        """Busca um produto pelo SKU no Magento."""
        product_search = ProductSearch(self.client)
        result = product_search.by_sku(sku)
        return result[0] if result else "Produto não encontrado."

    def create_product(self, sku: str, name: str, price: float, description: str):
        """Cria um novo produto no Magento."""
        new_product = {
            "sku": sku,
            "name": name,
            "price": price,
            "status": 1,
            "visibility": 4,
            "type_id": "simple",
            "attribute_set_id": 4,
            "custom_attributes": [
                {"attribute_code": "description", "value": description}
            ]
        }
        response = self.client.post("products", data=new_product)
        return response.json() if response.ok else f"Erro ao criar o produto: {response.text}"

    def update_stock(self, sku: str, qty: int):
        """Atualiza o estoque de um produto no Magento."""
        response = self.client.post(f'stockItems/{sku}', data={"qty": qty, "is_in_stock": True})
        return "Estoque atualizado com sucesso!" if response.ok else f"Erro ao atualizar estoque: {response.text}"

    def list_orders(self):
        """Lista pedidos recentes no Magento."""
        order_search = OrderSearch(self.client)
        result = order_search.get_all()
        return [{"order_id": order.increment_id, "status": order.status} for order in result]
