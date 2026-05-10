import ollama, time

# qwen3.5:4b vs current lineup
# Reasoning slot: vs sage (qwen3:4b)
# Coding slot: vs swift (qwen2.5-coder:3b) and forge (qwen2.5-coder:7b)

REASONING_MODELS = [
    ("sage (qwen3:4b /think)", "qwen3:4b", "/think "),
    ("qwen3.5:4b /think", "qwen3.5:4b", "/think "),
    ("qwen3.5:4b /no_think", "qwen3.5:4b", "/no_think "),
]

CODING_MODELS = [
    ("swift (qwen2.5-coder:3b)", "qwen2.5-coder:3b", ""),
    ("forge (qwen2.5-coder:7b)", "qwen2.5-coder:7b", ""),
    ("qwen3.5:4b", "qwen3.5:4b", "/no_think "),
]

REASONING_TASKS = [
    "A bat and ball cost $1.10. The bat costs $1 more than the ball. How much does the ball cost? Show your reasoning.",
    "If all Bloops are Razzies and all Razzies are Lazzies, are all Bloops definitely Lazzies? Explain why.",
    "What is the next number in this sequence: 2, 6, 12, 20, 30, 42, ? Explain the pattern.",
]

CODING_TASKS = [
    "Write a Python function that takes a list of integers and returns the two numbers that add up to a target sum. Include edge cases.",
    "Debug this Python code and fix it:\ndef fibonacci(n):\n    if n = 0: return 0\n    if n == 1 return 1\n    return fibonacci(n-1) + fibonacci(n-2)\nprint(fibonacci(10))",
    "Write a Python decorator that measures and prints the execution time of any function it wraps.",
]

results = []

def run_bench(section_name, models, tasks, prefix_in_prompt=True):
    print(f"\n{'#'*60}")
    print(f"  {section_name}")
    print(f"{'#'*60}")

    for name, model, prefix in models:
        print(f"\n{'='*60}")
        print(f"  {name}")
        print(f"{'='*60}")
        total_time = 0

        for i, task in enumerate(tasks, 1):
            prompt = prefix + task
            print(f"\nQ{i}: {task[:70]}...")
            t0 = time.time()
            resp = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.1, "num_predict": 2000}
            )
            elapsed = time.time() - t0
            total_time += elapsed
            answer = resp["message"]["content"].strip()
            print(f"A{i}:\n{answer}")
            print(f"\n    [{elapsed:.1f}s]")

        results.append((name, total_time, section_name))

run_bench("REASONING", REASONING_MODELS, REASONING_TASKS)
run_bench("CODING", CODING_MODELS, CODING_TASKS)

print(f"\n\n{'='*60}")
print("  SUMMARY")
print(f"{'='*60}")
for section in ["REASONING", "CODING"]:
    print(f"\n  {section}:")
    for name, t, s in results:
        if s == section:
            print(f"    {name}: {t:.1f}s total")
