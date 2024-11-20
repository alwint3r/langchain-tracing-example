from app.llms.chat_openai import get_model_default
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

_model = get_model_default()
_workflow = StateGraph(state_schema=MessagesState)


def _call_model(state: MessagesState):
    response = _model.invoke(state["messages"])
    return {"messages": response}


_workflow.add_edge(START, "model")
_workflow.add_node("model", _call_model)

_memory = MemorySaver()

chatbot = _workflow.compile(checkpointer=_memory)
