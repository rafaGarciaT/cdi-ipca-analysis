import argparse
from src.pipeline import Pipeline
from src.utils.directory_utils import clear_data_folders


def main():
    parser = argparse.ArgumentParser(
        description='Pipeline de processamento de dados CDI e IPCA'
    )

    parser.add_argument(
        '--mode',
        type=str,
        choices=['daily', 'yearly', 'backfill'],
        default='daily',
        help='Modo de execução da pipeline (padrão: daily)'
    )

    parser.add_argument(
        '--persistence',
        type=str,
        choices=['excel', 'sqlite'],
        default='excel',
        help='Modo de persistência dos dados (padrão: excel)'
    )

    parser.add_argument(
        '--year',
        type=int,
        help='Ano alvo para processamento (modo yearly)'
    )

    parser.add_argument(
        '--clear-data',
        action='store_true',
        help='Limpa as pastas de dados antes de executar'
    )

    args = parser.parse_args()

    if args.mode == 'yearly' and not args.year:
        parser.error("O argumento --year é obrigatório quando --mode é 'yearly'")

    if args.clear_data:
        clear_data_folders()

    pipeline = Pipeline(
        persistence_mode=args.persistence,
        execution_mode=args.mode,
        target_year=args.year
    )

    pipeline.run()


if __name__ == '__main__':
    main()
