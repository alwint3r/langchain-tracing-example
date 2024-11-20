from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .searcher import agent
from ..utils.cost import calculate_cost

from langchain_core.messages import HumanMessage
from opentelemetry import trace
from langfuse.callback import CallbackHandler

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


tracer = trace.get_tracer(__name__)

langfuse_callback = CallbackHandler()


@router.post("/langfuse")
async def chat_langfuse(request: ChatRequest):
    try:
        configuration = {
            "configurable": {"thread_id": "1"},
            "callbacks": [langfuse_callback],
        }
        messages = [HumanMessage(request.question)]
        response = agent.invoke(
            {"messages": messages},
            configuration,
        )
        return {"content": response["messages"][-1].content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def chat(request: ChatRequest):
    with tracer.start_as_current_span("agent_chat") as span:
        try:
            configuration = {"configurable": {"thread_id": "1"}}
            messages = [HumanMessage(request.question)]
            response = agent.invoke(
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
