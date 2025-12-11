#!/usr/bin/env python

import sys

from tokenizer import tokenize

from parser import parse

from evaluator import evaluate

def main():
    import evaluator  # to access WATCH_* globals

    environment = {}

    # Parse command-line args
    watch_name = None
    filename = None

    for arg in sys.argv[1:]:
        if arg.startswith("watch="):
            watch_name = arg.split("=", 1)[1]
        else:
            filename = arg

    # Script mode (run file)
    if filename is not None:
        with open(filename, 'r') as f:
            source_code = f.read()
        try:
            tokens = tokenize(source_code)
            ast = parse(tokens)

            # Set up watch support if requested
            if watch_name:
                evaluator.WATCH_IDENTIFIER = watch_name
                evaluator.WATCH_LOCATION_MAP = evaluator.build_location_map(ast, tokens)

            final_value, exit_status = evaluate(ast, environment)
            if exit_status == "exit":
                sys.exit(final_value if isinstance(final_value, int) else 0)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)  # Indicate error to OS

    # REPL mode
    else:
        # If user runs: python runner.py watch=x
        if watch_name:
            evaluator.WATCH_IDENTIFIER = watch_name

        while True:
            try:
                source_code = input('>> ')

                if source_code.strip() in ['exit', 'quit']:
                    break

                tokens = tokenize(source_code)
                ast = parse(tokens)

                # For each REPL line, build a small location map
                if watch_name:
                    evaluator.WATCH_LOCATION_MAP = evaluator.build_location_map(ast, tokens)

                final_value, exit_status = evaluate(ast, environment)
                if exit_status == "exit":
                    print(f"Exiting with code: {final_value}")
                    sys.exit(final_value if isinstance(final_value, int) else 0)
                elif final_value is not None:
                    print(final_value)
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
