"""
arifosmcp.intelligence CLI Entry Point — Triple Transport Support

Usage:
    python -m arifosmcp.intelligence                # stdio (delegates to arifosmcp.transport)
    python -m arifosmcp.intelligence stdio          # stdio (delegates to arifosmcp.transport)
    python -m arifosmcp.intelligence sse            # SSE (delegates to arifosmcp.transport)
    python -m arifosmcp.intelligence http           # HTTP (delegates to arifosmcp.transport)
    python -m arifosmcp.intelligence health         # CLI subcommand (legacy)

DITEMPA BUKAN DIBERI
"""

import sys

TRANSPORT_MODES = {"stdio", "sse", "http", "streamable-http", "rest"}


def main():
    mode = (sys.argv[1] if len(sys.argv) > 1 else "stdio").strip().lower()

    # Transport now lives in the canonical arifosmcp.transport entrypoint.
    if mode in TRANSPORT_MODES or mode in {"", "-h", "--help"}:
        import warnings

        from arifosmcp.transport.__main__ import main as aaa_main

        warnings.warn(
            "arifosmcp.intelligence transport modes are deprecated; use 'python -m arifosmcp.transport' directly.",
            DeprecationWarning,
            stacklevel=2,
        )
        forwarded_mode = mode
        forwarded_args = sys.argv[2:]
        if mode == "streamable-http":
            forwarded_mode = "http"
        elif mode in {"", "-h", "--help"}:
            forwarded_mode = None
            forwarded_args = sys.argv[1:]

        forwarded_argv = ["arifosmcp.transport"]
        if forwarded_mode is not None:
            forwarded_argv.append(forwarded_mode)
        forwarded_argv.extend(forwarded_args)
        sys.argv = forwarded_argv
        aaa_main()
        return

    # Fall through to CLI for subcommands (health, processes, fs, etc.)
    from .cli import main as cli_main

    cli_main()


if __name__ == "__main__":
    main()
