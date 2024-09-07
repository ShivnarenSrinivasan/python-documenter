import json
from dataclasses import dataclass
import networkx as nx
import matplotlib.pyplot as plt

@dataclass
class FunctionCall:
    call_stack_depth: int
    call_count: int
    calling_function: str
    filename: str
    function: str
    code: str

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return [FunctionCall(**item) for item in data]

def create_execution_graph(function_calls):
    G = nx.DiGraph()

    for call in function_calls:
        caller = call.calling_function
        callee = call.function
        G.add_node(caller, label=caller)
        G.add_node(callee, label=callee)
        G.add_edge(caller, callee, label=f"call_count={call.call_count}")

    return G

def plot_graph(G):
    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold', arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red')
    plt.show()


def remove_duplicates(function_calls):
    unique_calls = []
    seen = set()

    for call in function_calls:
        identifier = (call.call_stack_depth, call.calling_function, call.function)
        if identifier not in seen:
            seen.add(identifier)
            unique_calls.append(call)

    return unique_calls

if __name__ == "__main__":
    json_file_path = r'C:\Users\wb570819\shiv\repos\wbg-credit_limit\wbg\credit_limit\scripts\program_trace.json'
    # json_file_path = r'C:\Users\wb570819\shiv\repos\python-documenter\out.json'
    function_calls = remove_duplicates(read_json(json_file_path))
    G = create_execution_graph(function_calls)
    plot_graph(G)
