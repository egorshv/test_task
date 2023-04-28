import networkx as nx
from bokeh.models import Range1d, Plot, Circle, HoverTool, MultiLine, CustomJS, TapTool
from bokeh.models.graphs import NodesAndLinkedEdges
from bokeh.plotting import show, from_networkx

G = nx.gnm_random_graph(15, 30)

p = Plot(x_range=Range1d(-2, 2), y_range=Range1d(-2, 2))
g = from_networkx(G, nx.spring_layout, scale=1.8, center=(0, 0))
p.renderers.append(g)

g.node_renderer.glyph = Circle(size=20, fill_color='navy')
g.edge_renderer.glyph = MultiLine(line_color='lightblue', line_alpha=0.8, line_width=2)

g.node_renderer.hover_glyph = Circle(size=20, fill_color='firebrick')
g.edge_renderer.hover_glyph = MultiLine(line_color='firebrick', line_width=5)

g.node_renderer.data_source.data['node'] = list(range(len(G)))
g.node_renderer.data_source.data['field1'] = [f'field1_value{i}' for i in range(len(G))]
g.node_renderer.data_source.data['field2'] = [f'field2_value{i}' for i in range(len(G))]

g.inspection_policy = NodesAndLinkedEdges()

hover = HoverTool()
hover.tooltips = """
<div>
    <h5>Node ID: @node</h5>
    <p>Field 1: @field1</p>
    <p>Field 2: @field2</p>
</div>
"""

js_code = """
    var id = cb_data.source.selected.indices;
    var nodes = source.nodes;

    function checkNode(node) {
        return node.id != id;
    }

    nodes = nodes.filter(checkNode);
    source.nodes = nodes;
"""

source = nx.json_graph.node_link_data(G)

callback = CustomJS(args=dict(source=source), code=js_code)

tap = TapTool(callback=callback)

p.add_tools(tap)

p.add_tools(hover)

show(p)
