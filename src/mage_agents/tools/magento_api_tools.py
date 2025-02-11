from crewai import Agent, Task, Crew
from my_magento import Client
import inspect
import spacy
import re

# Carregar modelo de NLP (Spacy para extração de entidades)
nlp = spacy.load("en_core_web_sm")

class MagentoAPI:
    def __init__(self, base_url, access_token):
        self.client = Client(base_url, access_token)
        self.commands = self._map_api_methods()

    def _map_api_methods(self):
        """Dinamicamente descobre e mapeia todos os métodos da API."""
        commands = {}
        for module_name in dir(self.client):
            module = getattr(self.client, module_name)
            if inspect.ismodule(module) or hasattr(module, '__dict__'):
                for method_name in dir(module):
                    if not method_name.startswith("_"):
                        method = getattr(module, method_name)
                        if callable(method):
                            commands[f"{module_name}.{method_name}"] = method
        return commands

    def execute_command(self, command_name, *args, **kwargs):
        """Executa um comando da API baseado no nome e argumentos."""
        method = self.commands.get(command_name)
        if method:
            return method(*args, **kwargs)
        return f"Erro: Comando '{command_name}' não encontrado"

    def parse_description(self, description):
        """Analisa a descrição em linguagem natural e mapeia para comandos Magento."""
        doc = nlp(description.lower())
        
        # Mapeamento de ações comuns para API do Magento
        action_map = {
            "update": "catalog.products.update",
            "change": "catalog.products.update",
            "list": "catalog.products.list",
            "create": "sales.orders.create",
            "order": "sales.orders.create",
            "stock": "inventory.stockItems.update"
        }
        
        # Identificar ação
        action = None
        for token in doc:
            if token.lemma_ in action_map:
                action = action_map[token.lemma_]
                break
        
        if not action:
            return "Erro: Não foi possível determinar a ação."
        
        # Identificar SKU e preço, se aplicável
        sku = None
        price = None
        for ent in doc.ents:
            if ent.label_ == "MONEY":
                price = float(re.sub(r'[^0-9.]', '', ent.text))
            elif ent.label_ == "PRODUCT":
                sku = ent.text
        
        args = []
        kwargs = {}
        
        if "update" in action and sku and price:
            args = [sku, {"price": price}]
        
        return (action, args, kwargs)
