from flask import Flask, render_template, request, jsonify
from dijkstra import shortest_path

app = Flask(__name__)

from map_data import north_india_graph, districts_data

# Use the dynamically generated North India graph
default_graph = north_india_graph

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/default_graph', methods=['GET'])
def get_default_graph():
    return jsonify({
        'graph': default_graph,
        'coordinates': districts_data
    })

@app.route('/api/calculate_route', methods=['POST'])
def calculate_route():
    data = request.json
    
    graph = data.get('graph', default_graph)
    start_node = data.get('start')
    end_node = data.get('end')
    
    if not start_node or not end_node:
        return jsonify({'error': 'Start and end nodes are required.'}), 400
        
    if start_node not in graph or end_node not in graph:
        return jsonify({'error': 'Start or end node not found in the graph.'}), 400

    distance, path = shortest_path(graph, start_node, end_node)
    
    if distance == float('inf'):
        return jsonify({
            'success': False,
            'message': 'No path found between the selected nodes.'
        })
        
    return jsonify({
        'success': True,
        'distance': distance,
        'path': path
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
