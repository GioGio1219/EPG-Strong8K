#!/usr/bin/env python3
"""Junta vários *.channels.xml num só, sem duplicar xmltv_id.

Uso: merge_channels.py config/channels.txt <pasta_upstream> <saida.xml>
"""
import glob
import os
import sys
import xml.etree.ElementTree as ET


def main(cfg, upstream, out):
    patterns = []
    with open(cfg, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)

    seen, root, files = set(), ET.Element("channels"), 0
    for pat in patterns:
        matches = sorted(glob.glob(os.path.join(upstream, pat))) or sorted(glob.glob(pat))
        if not matches:
            print(f"AVISO: sem ficheiros para '{pat}'", file=sys.stderr)
        for path in matches:
            files += 1
            for ch in ET.parse(path).getroot().findall("channel"):
                cid = ch.get("xmltv_id")
                if not cid or cid in seen:
                    continue
                seen.add(cid)
                root.append(ch)

    if not seen:
        sys.exit("ERRO: nenhum canal encontrado. Verifique config/channels.txt")
    ET.ElementTree(root).write(out, encoding="utf-8", xml_declaration=True)
    print(f"{len(seen)} canais únicos de {files} ficheiros -> {out}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
