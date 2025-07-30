import matplotlib.pyplot as plt
import os

def render_graph(data: list, filename: str = "/app/data/graph_output.png") -> str:
    """
    Render a simple line graph from a list of numeric data.
    """
    try:
        plt.figure()
        plt.plot(data, marker='o')
        plt.title("Generated Graph")
        plt.grid(True)
        plt.savefig(filename)
        plt.close()
        return f"📊 Graph saved to {filename}"
    except Exception as e:
        return f"⚠️ Graph Rendering Error: {e}"
