# MageAgents Crew

Bem-vindo ao **MageAgents Crew**, um sistema multi-agente baseado no [crewAI](https://crewai.com) que interage com o Magento 2 (Adobe Commerce). Este projeto permite a automação de tarefas complexas no e-commerce, utilizando agentes de IA colaborativos, potenciados pelo **LLaMA 3.2 (3B)** via **Ollama**.

## ✨ Recursos Principais

- 🤖 **Multi-agentes CrewAI**: Coordene agentes para automatizar tarefas no Magento 2.
- 🔍 **Pesquisa e automação**: Os agentes podem buscar, analisar e executar ações.
- 🌐 **Integração com Magento 2**: Baseado no [docker-magento](https://github.com/markshust/docker-magento).
- 🛠️ **Customizável**: Configure agentes, tarefas e fluxos no YAML.
- 💡 **Baseado em LLaMA 3.2**: IA de ponta com **Ollama** para processamento avançado.

---

## 🚀 Instalação

### ✅ Pré-requisitos
- **Python** >= 3.10 < 3.13
- **Docker** e **Docker Compose**
- **CrewAI** e **Ollama**
- **Magento 2 (via Docker)**

### ♻️ Configuração Inicial
1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/mage-agents.git
   cd mage-agents
   ```
2. Instale o gerenciador de pacotes **UV**:
   ```bash
   pip install uv
   ```
3. Instale as dependências do projeto:
   ```bash
   crewai install
   ```
4. Configure seu arquivo **.env**:
   ```bash
   cp .env.example .env
   ```

5. Inicie o ambiente Magento 2:
   ```bash
        # Create your project directory then go into it:
        mkdir -p ~/Sites/magento
        cd $_

        # Run this automated one-liner from the directory you want to install your project.
        curl -s https://raw.githubusercontent.com/markshust/docker-magento/master/lib/onelinesetup | bash -s -- magento.test community 2.4.7-p3
   ```

---

## 🚧 Configuração dos Agentes
Os agentes do MageAgents são definidos em arquivos YAML, permitindo uma configuração modular.

- **Defina seus agentes:** `src/mage_agents/config/agents.yaml`
- **Configure tarefas:** `src/mage_agents/config/tasks.yaml`
- **Personalize fluxos:** `src/mage_agents/crew.py`
- **Ajuste entradas personalizadas:** `src/mage_agents/main.py`

Exemplo de configuração de um agente:
```yaml
agents:
  - name: "Analista de Vendas"
    role: "Monitoramento e análise de desempenho de produtos"
    tools:
      - "scraper"
      - "notificador"
```

---

## 🌟 Executando o MageAgents Crew
Para iniciar o sistema multi-agente e começar a automação no Magento 2:
```bash
crewai run
```
Isso irá ativar os agentes e executar as tarefas configuradas.

---

## 🔧 Desenvolvimento e Personalização
Este projeto permite extensões e personalizações, incluindo:
- **Adição de novas ferramentas**: Edite `src/mage_agents/tools.py`
- **Criação de novos fluxos de trabalho**: Modifique `crew.py`
- **Integração com outras APIs**: Conecte via FastAPI ou GraphQL do Magento 2

### Estrutura do Projeto
```
/mage-agents
├── src/
│   ├── mage_agents/
│   │   ├── config/
│   │   ├── tools/
│   │   ├── knowledge/
│   │   ├── crew.py
│   │   ├── main.py
├── docker-compose.yml
├── .env.example
├── README.md
```

---

## 🛠️ Suporte e Contato
- 📘 **Documentação**: [CrewAI Docs](https://docs.crewai.com)
- 🌐 **Repositório**: [GitHub MageAgents](https://github.com/gabrielgts/mage-agents)

Vamos revolucionar o e-commerce com **IA multi-agente**! 🌟

