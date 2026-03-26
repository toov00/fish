# fish

A simple && tiny CLI that wraps a timer (or a command) and shows a small in-terminal  animation of a fish. 

```
  ·    o     ·    ·

    ><(((((°>       swims and turns in place

  ·    ·    o    ·
```

## What It Does

Runs a subprocess with stdout and stderr suppressed so the screen stays clean, then redraws the animation in place until the process exits. You get a heat bar under the art, and on completion it shows a short finish frame. On completion, fish plays a best-effort sound cue.

## Installation

Need Python 3.9+.

```bash
cd /path/to/tea
pip install -e .
# or for an isolated install:
pipx install .
```

To run from source (no install), from the repo root run `python3 -m fish`.

## Usage

Wrap a command:

```bash
fish npm run build
fish cargo test
fish python train.py
```

Timer only:

```bash
fish --time 30
```

## Reference

Flags:

- `--time N` / `-t N`: countdown for N seconds, no command

Arguments:

- `command ...`: the command to run (everything after flags is treated as the command)

## Limitations

- Subprocess output is suppressed by design; this is meant for jobs where you do not need to watch logs live.
- On completion, fish plays a best-effort sound (depends on your OS and terminal settings).

## Contributing

Issues and PRs are welcome. If you are changing the visuals, include a screenshot in the PR description.

## License

Not specified yet.

## Resources

- [pipx](https://pypa.github.io/pipx/) for an isolated install
# fish
