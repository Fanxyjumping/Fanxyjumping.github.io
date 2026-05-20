#!/usr/bin/env python3
from __future__ import annotations

import http.server
import socketserver
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build_posts.py"
DEFAULT_PORT = 8000


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def build_posts() -> None:
    subprocess.run([sys.executable, str(BUILD_SCRIPT)], cwd=ROOT, check=True)


def serve(port: int) -> None:
    handler = http.server.SimpleHTTPRequestHandler
    with ReusableTCPServer(("", port), handler) as httpd:
        print(f"Serving {ROOT}")
        print(f"Open http://localhost:{port}/")
        httpd.serve_forever()


def main() -> None:
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    build_posts()
    try:
        serve(port)
    except OSError as exc:
        if exc.errno == 48:
            raise SystemExit(f"Port {port} is already in use. Try: python3 scripts/serve.py {port + 1}")
        raise
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()
