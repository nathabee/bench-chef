#!/usr/bin/env python3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os
import sys


class AngularFallbackHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        requested = Path(self.translate_path(self.path))
        if requested.exists():
            return super().send_head()

        self.path = "/index.html"
        return super().send_head()


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: serve_frontend.py <directory> <port>", file=sys.stderr)
        return 2

    directory = Path(sys.argv[1]).resolve()
    port = int(sys.argv[2])

    if not (directory / "index.html").is_file():
        print(f"Missing index.html in {directory}", file=sys.stderr)
        return 1

    os.chdir(directory)
    server = ThreadingHTTPServer(("0.0.0.0", port), AngularFallbackHandler)
    print(f"Serving BenchChef frontend from {directory} on port {port}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
