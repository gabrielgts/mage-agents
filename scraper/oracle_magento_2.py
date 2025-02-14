import requests
import xml.etree.ElementTree as ET
import time
import random
import json
import ollama
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Configurações
SITEMAP_URL = "https://experienceleague.adobe.com/en/sitemap.xml"
OUTPUT_FILE = "adobe_commerce_knowledge_3.json"

# Inicializa UserAgent para rotação
ua = UserAgent()

def get_headers():
    """Gera headers com um User-Agent aleatório."""
    return {"User-Agent": ua.random}

def fetch_sitemap(url):
    """Busca e parseia o sitemap XML."""
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return ET.fromstring(response.content)
    else:
        print(f"Erro ao buscar o sitemap: {response.status_code}")
        return None

def extract_commerce_links(sitemap_root):
    """Extrai links relevantes para Adobe Commerce."""
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    links = []
    for url in sitemap_root.findall('ns:url', namespace):
        loc = url.find('ns:loc', namespace).text
        if '/docs/commerce' in loc or '/docs/commerce-admin/' in loc:
            links.append(loc)
    return links

def scrape_page(url):
    """Raspa o conteúdo de uma página."""
    try:
        response = requests.get(url, headers=get_headers())
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.get_text(separator='\n', strip=True)
        else:
            print(f"Erro ao acessar {url}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao raspar {url}: {e}")
        return None

def generate_summary(text):
    """Gera um resumo do conteúdo usando o modelo local."""
    prompt = f"Resuma o seguinte texto:\n{text[:2000]}"  # Limita a entrada para evitar problemas
    response = ollama.chat(model='llama3.2:latest', messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def classify_category(text):
    """Classifica o conteúdo em uma categoria relevante."""
    prompt = """
    Classifique o seguinte texto em uma das categorias: Administração, Marketing, Desenvolvimento, SEO, Configuração.
    Retorne apenas o nome da categoria.
    
    Texto:\n{text[:2000]}
    """
    response = ollama.chat(model='llama3.2:latest', messages=[{"role": "user", "content": prompt}])
    return response['message']['content'].strip()

def generate_embeddings(text):
    """Gera embeddings do conteúdo para busca semântica."""
    response = ollama.embeddings(model='llama3.2:latest', prompt=text[:2000])
    return response['embedding']

def load_existing_data(filename):
    """Carrega dados já salvos."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_to_json(data, filename):
    """Salva os dados no arquivo JSON."""
    existing_data = load_existing_data(filename)
    existing_data.update(data)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

def main():
    sitemap_root = fetch_sitemap(SITEMAP_URL)
    if sitemap_root is None:
        return

    commerce_links = extract_commerce_links(sitemap_root)
    print(f"Encontradas {len(commerce_links)} páginas do Adobe Commerce.")
    
    existing_data = load_existing_data(OUTPUT_FILE)
    
    for link in commerce_links:
        if link in existing_data:
            print(f"Pulando {link}, já processado.")
            continue
        
        print(f"Processando {link}...")
        content = scrape_page(link)
        if content:
            summary = generate_summary(content)
            category = classify_category(content)
            embeddings = generate_embeddings(content)
            
            save_to_json({
                link: {
                    "summary": summary,
                    "category": category,
                    "embeddings": embeddings,
                    "content": content
                }
            }, OUTPUT_FILE)
        
        # Espera aleatória para evitar bloqueios
        time.sleep(random.uniform(1, 3))
    
    print(f"Extração concluída! Dados salvos em {OUTPUT_FILE}")

if __name__ == "__main__":
    main()