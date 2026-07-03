from langgraph.graph import StateGraph

from app.graph.state import LearnovaState
from app.graph.nodes.topic_node import topic_extraction_node
from app.graph.nodes.blueprint_node import blueprint_node
from app.graph.nodes.mcq_node import mcq_generation_node
from app.graph.nodes.document_loader_node import document_loader_node

graph = StateGraph(
    LearnovaState
)

graph.add_node(
    "topic_extraction",
    topic_extraction_node
)
graph.add_node(
    "document_loader",
    document_loader_node
)

graph.add_node(
    "blueprint",
    blueprint_node
)

graph.add_node(
    "mcq_generation",
    mcq_generation_node
)

graph.add_edge(
    "document_loader",
    "topic_extraction"
)

graph.add_edge(
    "topic_extraction",
    "blueprint"
)

graph.add_edge(
    "blueprint",
    "mcq_generation"
)

graph.set_entry_point(
    "document_loader"
)

graph.set_finish_point(
    "mcq_generation"
)

learnova_graph = graph.compile()