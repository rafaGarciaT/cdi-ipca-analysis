import argparse
import sys
from src.pipeline import Pipeline
from src.utils.directory_utils import clear_data_folders
from src.config import FIRST_YEAR_LIMIT


def main():
    parser = argparse.ArgumentParser(
        description='Pipeline de coleta e processamento de dados CDI e IPCA',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
    Exemplos de uso:
      python main.py --mode month
      python main.py --mode yearly --year 2024
      python main.py --mode backfill
      python main.py --clear-data --mode month
      python main.py --clear-data-only
            """
    )


    parser.add_argument(
        '--mode',
        type=str,
        choices=['month', 'yearly', 'backfill'],
        default='month',
        help='Modo de execução da pipeline (padrão: month)'
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
        '--end-year',
        type=int,
        help='Ano final para processamento de range (opcional, usado com --mode yearly)'
    )

    parser.add_argument(
        '--clear-data',
        action='store_true',
        help='Limpa as pastas de dados antes de executar a pipeline'
    )

    parser.add_argument(
        '--clear-data-only',
        action='store_true',
        help='Apenas limpa as pastas de dados sem executar a pipeline'
    )

    args = parser.parse_args()

    if args.clear_data_only:
        clear_data_folders()
        sys.exit(0)

    if args.clear_data:
        clear_data_folders()

    if not args.mode:
        parser.error("--mode é obrigatório (escolha: month, yearly, backfill)")

    if args.mode == 'yearly':
        if args.year <= FIRST_YEAR_LIMIT:
            parser.error(f"--year deve ser maior ou igual a {FIRST_YEAR_LIMIT}")

        start_year = args.year
        end_year = args.end_year if args.end_year else args.year

        if end_year < start_year:
            parser.error("--end-year deve ser maior ou igual a --year")

        for year in range(start_year, end_year + 1):
            pipeline = Pipeline(
                processed_persistence_mode=args.persistence,
                execution_mode=args.mode,
                target_year=year
            )
            pipeline.run()
    else:
        pipeline = Pipeline(
            processed_persistence_mode=args.persistence,
            execution_mode=args.mode,
            target_year=args.year
        )
        pipeline.run()


if __name__ == '__main__':
    main()
