#!/usr/bin/env python3
"""Serve the local static preview with the site's official price endpoint."""

import html
import json
import re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent.parent / "dist"
SOURCE = "https://publicgold.com.my/"


def parse_table(source: str, heading: str) -> list[dict]:
    title = source.find(heading)
    if title < 0:
        return []
    start = source.find("<table", title)
    end = source.find("</table>", start)
    if start < 0 or end < 0:
        return []
    rows = re.findall(r"<tr\b[^>]*>([\s\S]*?)</tr>", source[start : end + 8], re.I)[1:]
    prices = []
    for row in rows:
        cells = re.findall(r"<td\b[^>]*>([\s\S]*?)</td>", row, re.I)
        if len(cells) < 2:
            continue
        purity = html.unescape(re.sub(r"<[^>]+>", " ", cells[0])).strip()
        value = re.search(r"[0-9]+(?:\.[0-9]+)?", html.unescape(re.sub(r"<[^>]+>", " ", cells[1])))
        if purity in {"999", "916"} and value:
            prices.append({"purity": purity, "price": float(value.group())})
    return prices


class PreviewHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if self.path.split("?", 1)[0] != "/api/prices":
            return super().do_GET()
        try:
            request = Request(SOURCE, headers={"User-Agent": "Mozilla/5.0 (compatible; GoldPriceReader/1.0)"})
            with urlopen(request, timeout=15) as response:
                page = response.read().decode("utf-8", "ignore")
            jewel = parse_table(page, "PG Jewel")
            buyback = parse_table(page, "Non-PG Gold Buyback")
            updates = [date for date in re.findall(r"Last Update\s+(\d{1,2}-[A-Za-z]{3}-\d{4}\s+\d{2}:\d{2}:\d{2})", page) if "2021" not in date]
            if len(jewel) != 2 or len(buyback) != 2 or not updates:
                raise ValueError("Official price tables could not be verified")
            status = 200
            payload = {"ok": True, "jewel": jewel, "buyback": buyback, "updatedAt": updates[0], "source": SOURCE}
        except Exception:
            status = 503
            payload = {"ok": False, "error": "Harga semasa Public Gold tidak dapat dipaparkan buat sementara waktu."}
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 4185), PreviewHandler).serve_forever()
