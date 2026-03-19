"""
aclip_cai CLI Entry Point — Triple Transport Support

Usage:
    python -m aclip_cai                # stdio (delegates to aaa_mcp)
    python -m aclip_cai stdio          # stdio (delegates to aaa_mcp)
    python -m aclip_cai sse            # SSE (delegates to aaa_mcp)
    python -m aclip_cai http           # HTTP (delegates to aaa_mcp)
    python -m aclip_cai health         # CLI subcommand (legacy)

DITEMPA BUKAN DIBERI
"""

import sys

TRANSPORT_MODES = {"stdio", "sse", "http", "streamable-http", "rest"}


def main():
    mode = (sys.argv[1] if len(sys.argv) > 1 else "stdio").strip().lower()

    # Transport now lives in the canonical aaa_mcp entrypoint.
    if mode in TRANSPORT_MODES or mode in {"", "-h", "--help"}:
        import warnings

        from aaa_mcp.__main__ import main as aaa_main

        warnings.warn(
            "aclip_cai transport modes are deprecated; use 'python -m aaa_mcp' directly.",
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

        forwarded_argv = ["aaa_mcp"]
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
