# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

Este arquivo segue o padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) 
e está conforme [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [0.2.0] - 2026-02-23

### Adicionado
- Primeiros notebooks de demonstração e análise de dados.
- Primeira classe de visualização de dados.
- Primeiros testes unitários e de QA.
- Classe de indicadores com a lógica referente que antes pertencia à Pipeline.
- Sistema de logging para monitoramento da execução da Pipeline.
- Classes relacionadas à persistência de dados brutos.
- Script Makefile para facilitar a execução em CLI.

### Modificado
- Arquitetura da Pipeline e de todas suas camadas. Permitindo maior flexibilidade e escalabilidade.
- Scripts de execução foram expandidos e adaptados para a nova arquitetura.

### Limitações conhecidas
- Testes não garantem a total funcionalidade da Pipeline.
- Exceções ainda não são tratadas de forma robusta.

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

