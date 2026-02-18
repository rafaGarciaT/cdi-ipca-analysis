# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

Este arquivo segue o padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) 
e está conforme [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Adicionado
- Primeiros notebooks de demonstração e análise de dados.

### Modificado
- Arquitetura da Pipeline e de todas suas camadas. Permitindo maior flexibilidade e escalabilidade.


## [0.1.0] - 2026-01-20

### Adicionado
- Implementação inicial da Pipeline.
- Utilitários para manipulação de datas e diretórios.
- Implementação dos indicadores CDI e IPCA.
- Modos de execução: Month, Year, Backfill.
- Persistência de dados em Excel.
- Cálculos de mensurações de CDI e IPCA.
- Documentação inicial.
- Scripts bash para execução em CLI.

### Limitações conhecidas
- Exceções fracas no fetch de dados. 
- Falta de testes.
- Arquitetura não escalável.
- Pipeline com complexidade cognitiva alta.

### Próximos passos
- Adicionar testes unitários e de integração.
- Melhorar tratamento de exceções.
- Implementar persistência em SQLite.
- Implementar dashboards interativos e análises em notebooks Jupyter. 
- Tornar a arquitetura mais modular e escalável.
- Revisar métodos de execução.

