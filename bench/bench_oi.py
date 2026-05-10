import sys, time
sys.path.insert(0, '/home/z/.venvs/openinterp/lib/python3.14/site-packages')

from interpreter import interpreter as oi

MODELS = [
    ("craft",  "ollama/qwen2.5-coder:7b"),
]

# Explicit Python-only task — no bash ambiguity, small models can handle it
TASK = (
    "Write and run a Python script that: "
    "1) reads /home/z/test_folder/data.csv using the csv module, "
    "2) finds the student with the highest score, "
    "3) prints: 'Top student: <name> with <score>'. "
    "Use Python only, no bash."
)

results = []

for alias, model in MODELS:
    print(f"\n{'='*60}")
    print(f"  {alias.upper()}  ({model})")
    print(f"{'='*60}\n")

    oi.__init__()  # reset state between runs
    oi.llm.model = model
    oi.llm.api_base = "http://localhost:11434"
    oi.llm.context_window = 4096
    oi.llm.max_tokens = 512
    oi.llm.supports_functions = False
    oi.llm.supports_vision = False
    oi.llm.temperature = 0.1
    oi.offline = True
    oi.auto_run = True
    oi.safe_mode = "off"
    oi.custom_instructions = (
        "Use `bash` for shell commands. Never re-execute shell output as Python code. "
        "Be concise. Complete the task in as few steps as possible."
    )
    oi.verbose = False
    oi.max_turns = 6  # bail out after 6 back-and-forths

    t0 = time.time()
    messages = oi.chat(TASK, display=True, stream=False)
    elapsed = time.time() - t0

    # Extract final text response
    final = next(
        (m["content"] for m in reversed(messages) if m.get("role") == "assistant" and isinstance(m.get("content"), str)),
        "(no text response)"
    )

    results.append((alias, model, elapsed, final[:200]))
    print(f"\n  Time: {elapsed:.1f}s")

print(f"\n\n{'='*60}")
print("  BENCHMARK SUMMARY")
print(f"{'='*60}")
print(f"{'Model':<10} {'Time':>8}   Final response (truncated)")
print("-"*60)
for alias, model, elapsed, final in results:
    short = final.replace('\n', ' ')[:55]
    print(f"{alias:<10} {elapsed:>7.1f}s   {short}")
print()
