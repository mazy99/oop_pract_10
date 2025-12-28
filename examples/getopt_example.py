import getopt
import sys


def main() -> None:
    full_cmd_args: list[str] = sys.argv
    argument_list: list[str] = full_cmd_args[1:]
    short_options: str = "ho:v"
    long_options: list[str] = ["help", "output=", "verbose"]

    try:
        arguments: list[tuple[str, str]]
        values: list[str]
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    for current_argument, current_value in arguments:
        if current_argument in ("-h", "--help"):
            print("Displaying help")
        elif current_argument in ("-o", "--output"):
            print(f"Output set to: {current_value}")
        elif current_argument in ("-v", "--verbose"):
            print("Verbose mode enabled")

    if values:
        print(f"Remaining arguments: {values}")


if __name__ == "__main__":
    main()
