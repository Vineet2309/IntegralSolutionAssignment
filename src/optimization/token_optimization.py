"""
Token Optimization Benchmark Simulation
Demonstrates Context Pruning and Prompt Schema Compression.
"""


def calculate_tokens(prompt_text: str) -> int:
    """Rough estimation of token count (~4 chars per token)."""
    return len(prompt_text) // 4


def run_benchmark():
    # Baseline prompt simulating ~100K token overload
    raw_context = "User log history data... " * 15000  # ~85k tokens
    verbose_system_prompt = "You are a helpful assistant... " * 2000  # ~15k tokens

    baseline_tokens = calculate_tokens(raw_context + verbose_system_prompt)

    # Optimization 1: Top-k Context Chunking & Metadata Stripping
    pruned_context = "Relevant chunk 1... Relevant chunk 2..."  # ~8.5k tokens

    # Optimization 2: YAML Schema & System Prompt Caching
    cached_schema_prompt = "schema: {query: str, action: str}"  # ~3.2k tokens

    optimized_tokens = calculate_tokens(pruned_context + cached_schema_prompt)

    print(f"Baseline Tokens: {baseline_tokens}")
    print(f"Optimized Tokens: {optimized_tokens}")
    print(f"Reduction: {((baseline_tokens - optimized_tokens) / baseline_tokens) * 100:.2f}%")


if __name__ == "__main__":
    run_benchmark()
