"""
Multi-Step Agent Pipeline with Guardrails & Validation
Addresses Part 2: Handling timeouts, malformed outputs, and data corruption.
"""

import asyncio
from typing import Dict, Any
from pydantic import BaseModel, Field, ValidationError


# ---------------------------------------------------------------------------
# 1. Pydantic Schemas for Strict Output Enforcement (Fixes Malformed Output)
# ---------------------------------------------------------------------------
class Step1Output(BaseModel):
    query: str
    intent: str = Field(..., description="Target intent extracted from query")


class Step2Output(BaseModel):
    intent: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    data_payload: Dict[str, Any]


# ---------------------------------------------------------------------------
# 2. Pipeline Implementation with Async Timeouts & Inter-Step Guardrails
# ---------------------------------------------------------------------------
class AgentPipeline:
    def __init__(self, step_timeout: float = 5.0):
        self.step_timeout = step_timeout

    async def execute_step_1(self, raw_input: Dict[str, Any]) -> Step1Output:
        """Step 1: Extract intent from user query."""
        # Simulated agent work
        await asyncio.sleep(0.5)
        
        # Enforce structured output via Pydantic model
        return Step1Output(
            query=raw_input.get("user_query", ""),
            intent="data_analysis"
        )

    async def execute_step_2(self, step1_result: Step1Output) -> Step2Output:
        """Step 2: Process intent with step-level async timeout enforcement."""
        # Enforce strict step execution deadline (Fixes Timeouts)
        async with asyncio.timeout(self.step_timeout):
            await asyncio.sleep(0.5)  # Simulating external tool/LLM call
            
            output = Step2Output(
                intent=step1_result.intent,
                confidence_score=0.95,
                data_payload={"status": "success", "processed_records": 120}
            )

        # Inter-step assertion guardrail (Fixes Silent Data Corruption)
        self._validate_intermediate_data(output)
        return output

    def _validate_intermediate_data(self, output: Step2Output) -> None:
        """Runtime assertion guardrail to catch bad/corrupted state."""
        if output.confidence_score < 0.5:
            raise ValueError(f"Confidence score too low: {output.confidence_score}")
        if "processed_records" not in output.data_payload:
            raise ValueError("Corrupted payload: missing 'processed_records'")

    async def run(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution flow with centralized error handling."""
        try:
            # Step 1: Parse input
            step1_out = await self.execute_step_1(raw_input)
            
            # Step 2: Process step with guardrails
            step2_out = await self.execute_step_2(step1_out)
            
            return {
                "status": "success",
                "final_output": step2_out.model_dump()
            }

        except TimeoutError:
            return {"status": "error", "message": "Pipeline step timed out."}
        except ValidationError as ve:
            return {"status": "error", "message": f"Malformed LLM output: {ve}"}
        except Exception as e:
            return {"status": "error", "message": f"Pipeline failure: {str(e)}"}


# ---------------------------------------------------------------------------
# Execution Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    pipeline = AgentPipeline()
    sample_request = {"user_query": "Analyze stock trends for Q2"}
    
    result = asyncio.run(pipeline.run(sample_request))
    print("Pipeline Execution Result:")
    print(result)