import ollama, time

MODELS = [
    ("swift (qwen2.5-coder:3b)", "qwen2.5-coder:3b", ""),
    ("sage /no_think (qwen3:4b)", "qwen3:4b", "/no_think "),
    ("sage /think (qwen3:4b)", "qwen3:4b", "/think "),
    ("forge (qwen2.5-coder:7b)", "qwen2.5-coder:7b", ""),
    ("rune (deepseek-r1:7b)", "deepseek-r1:7b", ""),
]

TASKS = [
    "A bat and ball cost $1.10. The bat costs $1 more than the ball. How much does the ball cost? Show your reasoning.",
    "If all Bloops are Razzies and all Razzies are Lazzies, are all Bloops definitely Lazzies? Explain why.",
    "What is the next number in this sequence: 2, 6, 12, 20, 30, 42, ? Explain the pattern.",
]

results = []

for name, model, prefix in MODELS:
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")
    total_time = 0

    for i, task in enumerate(TASKS, 1):
        prompt = prefix + task
        print(f"\nQ{i}: {task[:60]}...")
        t0 = time.time()
        resp = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.1, "num_predict": 2000}
        )
        elapsed = time.time() - t0
        total_time += elapsed
        answer = resp["message"]["content"].strip()
        print(f"A{i}: {answer}")
        print(f"    [{elapsed:.1f}s]")

    results.append((name, total_time))

print(f"\n\n{'='*60}")
print("  SUMMARY")
print(f"{'='*60}")
for name, t in results:
    print(f"  {name}: {t:.1f}s total")
