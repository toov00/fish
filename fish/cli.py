import argparse

from fish.runner import boil_timer, run_with_kettle


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fish",
        description="Run a command (or timer) with a simple in-terminal wait animation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  fish --time 30
  fish --notify --time 30
  fish npm run build
  fish --notify npm run build
  fish cargo test
        """,
    )
    parser.add_argument(
        "--time",
        "-t",
        type=float,
        metavar="SECONDS",
        help="just run a timer for N seconds, no command",
    )
    parser.add_argument(
        "--notify",
        action="store_true",
        help="send a desktop notification when done (best-effort)",
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="command to run",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.time is not None:
        raise SystemExit(boil_timer(args.time, notify=args.notify))

    if not args.command:
        parser.print_help()
        raise SystemExit(0)

    cmd = args.command
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]

    raise SystemExit(
        run_with_kettle(
            cmd,
            notify=args.notify,
        )
    )


if __name__ == "__main__":
    main()
