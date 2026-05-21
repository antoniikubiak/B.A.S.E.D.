import argparse
import os
import subprocess
import sys
from based.parser.BasedCompiler import BasedCompiler

def get_platform_extension() -> str:
    """Detects the native operating system shared library extension."""
    if sys.platform == "win32":
        return ".dll"
    return ".so"

def main():
    parser = argparse.ArgumentParser(
        description="B.A.S.E.D. Language parser Interface"
    )
    parser.add_argument(
        "input",
        help="Path to the source file containing your math functions."
    )
    parser.add_argument(
        "-o", "--output",
        help="Custom output file name for the compiled library binary."
    )
    parser.add_argument(
        "--cc",
        default="gcc",
        help="The backend C compiler executable to use (default: gcc)."
    )
    parser.add_argument(
        "--keep-c",
        action="store_true",
        help="Keep the intermediate generated .c file on disk instead of purging it."
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' could not be found.", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r") as f:
        source_code = f.read()

    base_name, _ = os.path.splitext(args.input)
    output_ext = get_platform_extension()
    output_file = args.output if args.output else f"{base_name}{output_ext}"
    temp_c_file = f"{base_name}_codegen.c"

    try:
        print(f"Parsing and optimizing '{args.input}'...")
        compiled_c_text = BasedCompiler.compile(source_code)

        with open(temp_c_file, "w") as f:
            f.write("#include <math.h>\n\n")
            f.write(compiled_c_text)

        compile_cmd = [
            args.cc,
            "-O3",
            "-shared",
            "-o", output_file,
            "-fPIC",
            temp_c_file,
            "-lm",
        ]
        print(f"Triggering compilation via '{args.cc}'...")
        result = subprocess.run(compile_cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"C compilation step failed:\n{result.stderr}", file=sys.stderr)
            sys.exit(1)

        print(f"Success! Generated library saved to: {os.path.abspath(output_file)}")

    except Exception as e:
        print(f"parser error encountered: {e}", file=sys.stderr)
        sys.exit(1)

    finally:
        if not args.keep_c and os.path.exists(temp_c_file):
            os.remove(temp_c_file)

if __name__ == "__main__":
    main()
