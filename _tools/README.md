# Diagram tools (not published: Jekyll skips folders starting with "_")

- `panels.py`: draws the six story panels and the overview. Run `python3 panels.py ../presence-sync/images`.
- `arch.py`: draws the architecture diagram. Run `python3 arch.py ../presence-sync/diagrams/architecture.svg`.
- Deep-dive diagrams: edit the `.mmd` files in `presence-sync/diagrams/src/`, then export each to SVG with the Mermaid CLI:
  `mmdc -i file.mmd -o ../file.svg -c mcfg.json -b white`
