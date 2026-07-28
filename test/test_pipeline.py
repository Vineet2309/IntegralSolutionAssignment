import pytest
import asyncio
from src.pipeline.agent_pipeline import AgentPipeline
from src.optimization.token_optimization import calculate_tokens


def test_token_calculation():
    sample_text = "Hello world! This is a test string."
    tokens = calculate_tokens(sample_text)
    assert tokens > 0
    assert isinstance(tokens, int)


@pytest.mark.asyncio
async def test_agent_pipeline_success():
    pipeline = AgentPipeline(step_timeout=5.0)
    input_data = {"user_query": "Test query for unit testing"}
    
    result = await pipeline.run(input_data)
    
    assert result["status"] == "success"
    assert "final_output" in result
    assert result["final_output"]["confidence_score"] == 0.95


@pytest.mark.asyncio
async def test_agent_pipeline_timeout():
    # Pass an extremely small timeout to trigger the timeout failure path
    pipeline = AgentPipeline(step_timeout=0.0001)
    input_data = {"user_query": "Trigger timeout"}
    
    result = await pipeline.run(input_data)
    
    assert result["status"] == "error"
    assert "timed out" in result["message"]