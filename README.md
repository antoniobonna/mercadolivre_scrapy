
# MercadoLivre Scrapy

Este projeto extrai dados do Mercado Livre usando Scrapy, transforma os dados e os serve por meio de um dashboard ou API.

## 🧱 Estrutura do Projeto

```
mercadolivre_scrapy/
├── data/                      # Armazenamento de dados (ex: SQLite)
├── docs/
│   └── mercadolivre_scrapy/
│       └── dashboard/         # Frontend/backend do dashboard
│       └── app.py             # Ponto de entrada da aplicação
├── extract/
│   ├── spiders/               # Spiders do Scrapy
│   │   ├── mercadolivre.py    # Spider principal do Mercado Livre
│   │   ├── items.py           # Definições dos items
│   │   └── settings.py        # Configurações do Scrapy
│   └── __init__.py
├── transform/
│   └── main.py                # Scripts de transformação
├── tests/                     # Testes
├── poetry.lock
├── pyproject.toml
└── README.md
```

## 🔄 Fluxo ELT

```mermaid
graph TD
  A[Start] --> B[Extrair dados com Scrapy (mercadolivre.py)]
  B --> C[Armazenar dados brutos em data.db]
  C --> D[Transformar dados com transform/main.py]
  D --> E[Servir dados via app.py ou dashboard]
```

## 🚀 Primeiros Passos

### Instalação

```bash
poetry install
```

### Executar o Spider

```bash
cd extract
scrapy crawl mercadolivre
```

### Transformar os Dados

```bash
cd transform
python main.py
```

### Rodar o App

```bash
cd docs/mercadolivre_scrapy
python app.py
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
