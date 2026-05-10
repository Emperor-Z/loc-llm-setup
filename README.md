# Local LLM Setup

Full local AI stack on EndeavourOS (Arch Linux).
RTX 3050 Ti (4GB VRAM) · Ryzen 9 5900HX · 16GB RAM

---

## Model Lineup

| Alias | Model | Role | VRAM |
|---|---|---|---|
| `swift` | qwen2.5-coder:3b | Fast coding, quick answers | ~2.2GB full GPU |
| `sage` | qwen3:4b | Reasoning, logic, step-by-step | ~2.5GB full GPU |
| `forge` | qwen2.5-coder:7b | Code generation, technical chat | ~4.7GB split |
| `rune` | deepseek-r1:7b | Deep reasoning, hard problems | ~4.7GB split |
| `craft` | qwen2.5-coder:7b (OI) | Executes code, file tasks, automation | split |

Raw versions (no memory): `swift-raw`, `sage-raw`, `forge-raw`, `rune-raw`

---

## Restore Steps

### 1. Install Ollama and pull models
```bash
curl -fsSL https://ollama.com/install.sh | sh

ollama pull qwen2.5-coder:3b
ollama pull qwen3:4b
ollama pull qwen2.5-coder:7b
ollama pull deepseek-r1:7b
ollama pull nomic-embed-text
```

### 2. Create venvs
```bash
# Memory stack (llm-chat wrapper)
python -m venv ~/.venvs/memory
~/.venvs/memory/bin/pip install -r venvs/memory-requirements.txt

# Open Interpreter + browser tools
python -m venv ~/.venvs/openinterp
PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 pip install setuptools==69.5.1
~/.venvs/openinterp/bin/pip install -r venvs/openinterp-requirements.txt
~/.venvs/openinterp/bin/playwright install chromium
```

### 3. Install bin scripts
```bash
cp bin/llm-chat ~/.local/bin/llm-chat
cp bin/craft-run ~/.local/bin/craft-run
cp bin/browse ~/.local/bin/browse
chmod +x ~/.local/bin/llm-chat ~/.local/bin/craft-run ~/.local/bin/browse
```

Update the shebang lines in each script to point to the correct venv Python path.

### 4. Install OI profiles
```bash
mkdir -p ~/.config/open-interpreter/profiles
cp configs/oi-profiles/*.yaml ~/.config/open-interpreter/profiles/
```

### 5. Shell aliases
Add to `~/.bashrc` or `~/.zshrc`:
```bash
alias swift='llm-chat qwen2.5-coder:3b swift'
alias sage='llm-chat qwen3:4b sage'
alias forge='llm-chat qwen2.5-coder:7b forge'
alias rune='llm-chat deepseek-r1:7b rune'
alias craft='craft-run'

alias swift-raw='ollama run qwen2.5-coder:3b'
alias sage-raw='ollama run qwen3:4b'
alias forge-raw='ollama run qwen2.5-coder:7b'
alias rune-raw='ollama run deepseek-r1:7b'
```

---

## Memory Stack

- **mem0ai** + **chromadb** — unified memory at `~/.local/share/mem0/`
- **nomic-embed-text** via Ollama — local embeddings, no cloud
- All models share one memory store
- Exit with `exit` (swift/sage/forge/rune) or `Ctrl+C` (craft) to trigger save

---

## Persistent Memory Stack Notes

- mem0 LLM extractor uses `qwen3:4b`
- craft (OI) uses `qwen2.5-coder:7b` as main model, `qwen3:4b` for memory extraction
- Python 3.14 quirk for OI install: `PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1` + `setuptools==69.5.1`
- Playwright inline in OI broken (asyncio event loop conflict) — use `browse` bash command instead

---

## Browser Tool

```bash
browse <url> [css_selector]
```
Headless Chromium via Playwright. Examples:
```bash
browse https://news.ycombinator.com ".titleline > a"
browse https://example.com
```

---

## Bench Scripts

- `bench/bench_reasoning.py` — reasoning tasks across full lineup
- `bench/bench_challenger.py` — challenger bench: new model vs existing slots
- `bench/bench_oi.py` — Open Interpreter task bench (craft)

Run with the memory venv:
```bash
~/.venvs/memory/bin/python bench/bench_reasoning.py
~/.venvs/memory/bin/python bench/bench_challenger.py
```
