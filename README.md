
# MercadoLivre Scrapy

Este projeto extrai dados do Mercado Livre usando Scrapy, transforma os dados e os serve por meio de um dashboard ou API.

## 🧱 Estrutura do Projeto

```
MERCADOLIVRE_SCRAPY/
├── .ruff_cache/                 
├── data/
│   └── data.db                  # Banco de dados SQLite
├── docs/
├── mercadolivre_scrapy/        # Pacote principal do projeto
│   ├── dashboard/
│   │   └── app.py               # Streamlit App
│   ├── extract/
│   │   ├── __init__.py
│   │   ├── items.py             # Definições dos items Scrapy
│   │   ├── settings.py          # Configurações do Scrapy
│   │   └── spiders/
│   │       ├── __init__.py
│   │       └── mercadolivre.py  # Spider principal
│   ├── transform/
│   │   ├── __init__.py
│   │   └── main.py              # Script de transformação
├── tests/                       # Testes automatizados
├── scrapy.cfg                   # Configuração principal do Scrapy
├── .gitignore
├── gitdiff.bat
├── poetry.lock
├── pyproject.toml
└── README.md
```

## 🔄 Fluxo ELT

![image](https://github.com/user-attachments/assets/726c7520-30c0-45a1-82d7-9189c2847c21)

```mermaid
flowchart TD;
  E[Extrair dados com Scrapy] -->|Dados brutos| L[Carregar dados em SQLite]
  L -->|Dados transformados| T[Transformar dados com transform/main.py]
  T -->|Visualização| V[Servir dados com Streamlit]

  %% Estilos por etapa
  style E fill:#E3F2FD,stroke:#2196F3,stroke-width:2px,color:#0D47A1
  style L fill:#E8F5E9,stroke:#4CAF50,stroke-width:2px,color:#1B5E20
  style T fill:#FFF3E0,stroke:#FB8C00,stroke-width:2px,color:#E65100
  style V fill:#FCE4EC,stroke:#E91E63,stroke-width:2px,color:#880E4F
```


## 🚀 Primeiros Passos

### Instalação

```bash
poetry install
```

### Executar o Spider

```bash
cd mercadolivre_scrapy
scrapy crawl mercadolivre -o ../data/data.json
```

### Transformar os Dados

```bash
cd transform
python main.py
```

### Rodar o App

```bash
cd ../dashboard
streamlit run app.py
```

## 🧪 Testes

```bash
pytest
```

## 📁 Dados

- `data/data.db`: Banco SQLite para armazenar dados brutos e processados

## ⚙️ Configurações

- `scrapy.cfg`: Configuração do projeto Scrapy
- `settings.py`: Configurações específicas dos spiders
