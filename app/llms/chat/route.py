from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .chain import chatbot
from langchain_core.messages import HumanMessage
from opentelemetry import trace

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


tracer = trace.get_tracer(__name__)

_costs = {
    "input_tokens": 0.15,
    "output_tokens": 0.60,
}


def calculate_cost(input_tokens, output_tokens):
    input_cost = (input_tokens / 1e6) * _costs["input_tokens"]
    output_cost = (output_tokens / 1e6) * _costs["output_tokens"]
    total_cost = input_cost + output_cost
    return (total_cost, input_cost, output_cost)


@router.post("/")
async def chat(request: ChatRequest):
    with tracer.start_as_current_span("chat") as span:
        try:
            configuration = {"configurable": {"thread_id": "1"}}
            messages = [HumanMessage(request.question)]
            response = chatbot.invoke(
                {"messages": messages},
                configuration,
            )

            ai_message = response["messages"][-1]
            span.set_attribute("llm.response", ai_message.content)
            span.set_attribute("llm.input", request.question)

            tokens_usage = ai_message.usage_metadata
            span.set_attribute("llm.usage.input_tokens", tokens_usage["input_tokens"])
            span.set_attribute("llm.usage.output_tokens", tokens_usage["output_tokens"])
            span.set_attribute(
                "llm.model.name", ai_message.response_metadata["model_name"]
            )

            print(ai_message.response_metadata)
            print(ai_message.usage_metadata)

            total_cost, input_cost, output_cost = calculate_cost(
                tokens_usage["input_tokens"],
                tokens_usage["output_tokens"],
            )
            span.set_attribute("llm.cost.total", total_cost)
            span.set_attribute("llm.cost.input", input_cost)
            span.set_attribute("llm.cost.output", output_cost)

            return {"content": ai_message.content}
        except Exception as e:
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=str(e))
