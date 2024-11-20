import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsItem, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QGraphicsEllipseItem, QGraphicsLineItem, QLabel, QTextEdit, QScrollArea, QFormLayout
from PyQt5.QtGui import QPixmap, QPen, QColor, QBrush, QPainter
from PyQt5.QtCore import Qt, QPointF
from collections import defaultdict, deque
import heapq

class CampusMap:
    def __init__(self):
        self.graph = defaultdict(list)
        self.accessible_graph = defaultdict(list)
        self.building_names = {
            'TSU': 'Titan Student Union',
            'CPAC': 'Clayes Performing Arts Center',
            'PL': 'Pollak Library',
            'DBH': 'Dan Black Hall',
            'MH': 'McCarthy Hall',
            'GH': 'Gordon Hall',
            'CS': 'Computer Science',
            'EC': 'Engineering Complex',
            'VA': 'Visual Arts',
            'TG': 'Titan Gym',
            'SRC': 'Student Recreation Center',
            'SHCC': 'SHCC',
            'SGMH': 'SGMH',
            'NPS': 'NPS',
            'ENPS/ESPS': 'ENPS/ESPS',
            'ASC/TH': 'ASC/TH',
            'Lot A': 'Lot A',
            'Lot I': 'Lot I',
            'Lot A South': 'Lot A South',
            'TSC': 'TSC',
            'LH': 'LH',
            'Lot G': 'Lot G',
            'RGC': 'RGC',
            'Lot D': 'Lot D',
            'C East': 'C East',
            'C West': 'C West',
            'CP South': 'CP South',
            'GF': 'GF',
            'AF': 'AF',
            'TSF': 'TSF',
            'TTC': 'TTC',
            'TTF': 'TTF',
            'TS': 'TS',
            'RH':'RH',
            'Lot F': 'Lot F',
            'ECS Quad': 'ECS Quad',
            'H': 'H',
            'B': 'B',
            'Lot S': 'Lot S',
            'GAH': 'GAH',
            'Fullerton Mariott': 'Fullerton Marriott',
            'East Playfield': 'East Playfield',
        }
        self.building_positions = {
            'TSU': (178, 510),
            'CPAC': (230, 572),
            'PL': (310, 540),
            'DBH': (290, 680),
            'MH': (317, 640),
            'GH': (387, 640),
            'CS': (455, 460),
            'EC': (382, 532),
            'VA': (152, 570),
            'SRC': (167, 432),
            'TG': (255, 432),
            'SHCC': (373, 415),
            'SGMH': (404, 681),
            'NPS': (155, 665),
            'ENPS/ESPS': (490, 575),
            'ASC/TH': (52, 534),
            'Lot A': (140, 180),
            'Lot I': (449, 525),
            'Lot A South': (125, 295),
            'TSC': (285, 227),
            'LH': (368, 684),
            'Lot G': (270, 100),
            'RGC': (420, 405),
            'Lot D': (175, 370),
            'C East': (133, 723),
            'C West': (222, 715),
            'CP South': (406, 795),
            'GF': (325, 160),
            'AF': (336, 205),
            'TSF': (358, 266),
            'TTC': (224, 335),
            'TTF': (260, 297),
            'TS': (235, 205),
            'RH': (473, 400),
            'Lot F': (444, 575),
            'ECS Quad': (382, 492),
            'H': (358, 592),
            'B': (227, 485),
            'Lot S': (410, 846),
            'GAH': (92, 455),
            'Fullerton Mariott': (484, 681),
            'East Playfield': (334, 365),
        }
        self._initialize_campus()
        self.accessible_graph = defaultdict(list)  # Graph for accessible paths
        self.update_accessible_graph(False)

    def _initialize_campus(self):
        edges = [
            ('TSU', 'CPAC', 460),
            ('TSU', 'VA', 360),
            ('CPAC', 'PL', 481),
            ('CPAC', 'DBH', 500),
            ('PL', 'MH', 528),
            ('PL', 'EC', 416),
            ('DBH', 'MH', 279),
            ('MH', 'GH', 376),
            ('GH', 'EC', 598),
            ('CS', 'EC', 570),
            ('SRC', 'TG', 517),
            ('TG', 'SHCC', 634),
            ('TSU', 'SRC', 436),
            ('CS', 'SHCC', 558),
            ('GH', 'SGMH', 259),
            ('PL', 'TG', 651),
            ('NPS', 'VA', 529),
            ('NPS', 'CPAC', 692),
            ('NPS', 'DBH', 768),
            ('ENPS/ESPS', 'CS', 704),
            ('ENPS/ESPS', 'GH', 656),
            ('ASC/TH', 'NPS', 946),
            ('ASC/TH', 'VA', 580),
            ('ASC/TH', 'TSU', 694),
            ('ASC/TH', 'SRC', 834),
            ('Lot I', 'CS', 361),
            ('Lot I', 'ENPS/ESPS', 376),
            ('Lot I', 'EC', 372),
            ('Lot A', 'Lot A South', 591),
            ('TSC', 'Lot A South', 960),
            ('TSC', 'TG', 1158),
            ('LH', 'GH', 271),
            ('LH', 'SGMH', 154),
            ('LH', 'MH', 381),
            ('LH', 'DBH', 450),
            ('Lot G', 'Lot A', 904),
            ('RGC', 'TSC', 1217),
            ('RGC', 'SHCC', 289),
            ('RGC', 'CS', 394),
            ('PL', 'SHCC', 795),
            ('CPAC', 'MH', 598),
            ('Lot D', 'Lot A South', 502),
            ('Lot D', 'SRC', 415),
            ('C East', 'C West', 491),
            ('C East', 'NPS', 326),
            ('C West', 'NPS', 446),
            ('C West', 'DBH', 425),
            ('CP South', 'SGMH', 671),
            ('CP South', 'LH', 701),
            ('GF', 'Lot G', 482),
            ('GF', 'TSC', 400),
            ('GF', 'AF', 320),
            ('AF', 'TSC', 301),
            ('TSF', 'TSC', 366),
            ('AF', 'TSF', 287),
            ('RGC', 'TSF', 875),
            ('Lot D', 'TTC', 370),
            ('TTF', 'TTC', 256),
            ('TTF', 'TSC', 403),
            ('TG', 'TTC', 647),
            ('Lot A', 'TS', 590),
            ('Lot G', 'TS', 648),
            ('TSC', 'TS', 307),
            ('RGC', 'RH', 268),
            ('CS', 'RH', 340),
            ('Lot F', 'ENPS/ESPS', 271),
            ('Lot F', 'Lot I', 275),
            ('Lot F', 'EC', 408),
            ('Lot F', 'GH', 447),
            ('ECS Quad', 'CS', 462),
            ('ECS Quad', 'SHCC', 424),
            ('ECS Quad', 'EC', 237),
            ('ECS Quad', 'PL', 506),
            ('H', 'EC', 380),
            ('H', 'GH', 293),
            ('H', 'MH', 320),
            ('B', 'CPAC', 473),
            ('B', 'TSU', 341),
            ('B', 'SRC', 433),
            ('B', 'TG', 304),
            ('B', 'PL', 563),
            ('TS', 'Lot A South', 736),
            ('CP South', 'Lot S', 372),
            ('GAH', 'ASC/TH', 481),
            ('GAH', 'SRC', 407),
            ('Fullerton Mariott', 'SGMH', 490),
            ('Fullerton Mariott', 'ENPS/ESPS', 565),
            ('East Playfield', 'SHCC', 339),
            ('East Playfield', 'TSC', 843),
            ('East Playfield', 'TTF', 543),
        ]
        
        for source, dest, weight in edges:
            self.graph[source].append({'node': dest, 'weight': weight})
            self.graph[dest].append({'node': source, 'weight': weight})

        self.update_accessible_graph(False) # Initialize with all paths accessible

    def update_accessible_graph(self, accessibility_on):
        """Create a filtered graph based on accessibility toggle."""
        self.accessible_graph.clear()  # Clear previous accessible paths
        for source, neighbors in self.graph.items():
            for neighbor in neighbors:
                if not accessibility_on or neighbor['weight'] <= 675:  # Only include accessible paths
                    self.accessible_graph[source].append(neighbor)

    def bfs_shortest_path(self, start, end):
            graph = self.accessible_graph
            queue = deque([[start]])
            visited = set([start])
            
            while queue:
                path = queue.popleft()
                current = path[-1]
                
                if current == end:
                    return path
                    
                for neighbor in graph[current]:
                    next_node = neighbor['node']
                    if next_node not in visited:
                        visited.add(next_node)
                        new_path = list(path)
                        new_path.append(next_node)
                        queue.append(new_path)
        
            return None

    def dfs_all_paths(self, start, end, cap=100, limit=50000):
        def dfs_recursive(current, destination, path, visited, all_paths, total_paths_count):
            if total_paths_count[0] >= limit:
                return

            path.append(current)
            visited.add(current)

            if current == destination:
                total_paths_count[0] += 1
                if len(all_paths) < cap:
                    all_paths.append(list(path))
            else:
                for neighbor in self.accessible_graph[current]:
                    next_node = neighbor['node']
                    if next_node not in visited:
                        dfs_recursive(next_node, destination, path, visited, all_paths, total_paths_count)

            path.pop()
            visited.remove(current)

        all_paths = []
        total_paths_count = [0]
        dfs_recursive(start, end, [], set(), all_paths, total_paths_count)

        if total_paths_count[0] >= limit:
            return all_paths, "50,000+"
        else:
            return all_paths, total_paths_count[0]

    def dijkstra_shortest_path(self, start, end):
        graph = self.accessible_graph
        distances = {building: float('infinity') for building in graph}
        distances[start] = 0
        pq = [(0, start)]
        previous = {building: None for building in graph}
        
        while pq:
            current_distance, current = heapq.heappop(pq)
            
            if current == end:
                path = []
                while current:
                    path.append(current)
                    current = previous[current]
                return current_distance, path[::-1]
                
            if current_distance > distances[current]:
                continue
                
            for neighbor in graph[current]:
                distance = current_distance + neighbor['weight']
                
                if distance < distances[neighbor['node']]:
                    distances[neighbor['node']] = distance
                    previous[neighbor['node']] = current
                    heapq.heappush(pq, (distance, neighbor['node']))
                    
        return None, None

class CampusNavigationGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.campus_map = CampusMap()
        self.drawn_lines = []
        self.accessible_paths = []  # To store paths for accessibility toggle
        self.accessibility_on = False  # Toggle state
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Campus Navigation System')
        self.setGeometry(100, 100, 1000, 800)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create graphics view and scene
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(self.view)

        # Load and set background image
        background = QPixmap('Map.png')
        if not background.isNull():
            self.scene.setSceneRect(0, 0, background.width(), background.height())
            self.scene.addPixmap(background)

        # Add building nodes
        for building, pos in self.campus_map.building_positions.items():
            node = QGraphicsEllipseItem(pos[0] - 5, pos[1] - 5, 10, 10)
            node.setBrush(QBrush(Qt.red))
            node.setToolTip(self.campus_map.building_names[building])
            self.scene.addItem(node)

        # Add path lines with condition to categorize accessibility paths
        for source in self.campus_map.graph:
            for dest in self.campus_map.graph[source]:
                start_pos = self.campus_map.building_positions[source]
                end_pos = self.campus_map.building_positions[dest['node']]
                line = QGraphicsLineItem(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
                pen = QPen(QColor(100, 200, 200, 130), 2, Qt.SolidLine)
                
                # Paths longer than 600 units marked as "inaccessible"
                if dest['weight'] > 675:
                    self.accessible_paths.append(line)
                    pen.setStyle(Qt.DashLine)

                line.setPen(pen)
                self.scene.addItem(line)

        # Create control panel
        control_panel = QFormLayout()
        layout.addLayout(control_panel)

        # Start building selection
        start_label = QLabel('Start:')
        self.start_combo = QComboBox()
        self.start_combo.addItems(self.campus_map.building_names.keys())
        control_panel.addRow(start_label, self.start_combo)

        # End building selection
        end_label = QLabel('End:')
        self.end_combo = QComboBox()
        self.end_combo.addItems(self.campus_map.building_names.keys())
        control_panel.addRow(end_label, self.end_combo)

        # Algorithm selection
        algo_label = QLabel('Algorithm:')
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(['BFS', 'DFS', 'Dijkstra'])
        control_panel.addRow(algo_label, self.algo_combo)

        # Add buttons in a horizontal layout next to each other
        button_layout = QHBoxLayout()
        find_path_btn = QPushButton('Find Path')
        find_path_btn.clicked.connect(self.find_path)
        button_layout.addWidget(find_path_btn)

        clear_btn = QPushButton('Clear')
        clear_btn.clicked.connect(self.clear_scene)
        button_layout.addWidget(clear_btn)

        # Accessibility toggle button
        accessibility_btn = QPushButton('Toggle Accessibility Paths')
        accessibility_btn.clicked.connect(self.toggle_accessibility)
        button_layout.addWidget(accessibility_btn)

        # Add the button layout to the form layout
        control_panel.addRow(button_layout)

        # Scrollable result area
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.result_text)
        layout.addWidget(scroll_area)

    def toggle_accessibility(self):
        self.accessibility_on = not self.accessibility_on
        self.campus_map.update_accessible_graph(self.accessibility_on)  # Update accessible graph
        for line in self.accessible_paths:
            line.setVisible(not self.accessibility_on)

    def find_path(self):
        start = self.start_combo.currentText()
        end = self.end_combo.currentText()
        algorithm = self.algo_combo.currentText().lower()

        self.clear_drawn_paths()
        self.result_text.clear()

        if algorithm == 'bfs':
            path = self.campus_map.bfs_shortest_path(start, end)
            if path:
                self.draw_path(path)
                self.result_text.setText(f"Shortest path (fewest stops): {' → '.join(path)}")
            else:
                self.result_text.setText("No path found.")
        elif algorithm == 'dfs':
            paths, total_paths = self.campus_map.dfs_all_paths(start, end, cap=100, limit=50000)
            paths_text = "\n".join([f"Path {i+1}: {' → '.join(path)}" for i, path in enumerate(paths)])
            if total_paths == "50,000+":
                self.result_text.setText(f"Found 50,000+ path(s):\n{paths_text}")
            else:
                self.result_text.setText(f"Found {total_paths} path(s):\n{paths_text}")

            if paths:
                self.draw_path(paths[0])
        else:
            distance, path = self.campus_map.dijkstra_shortest_path(start, end)
            if path:
                self.draw_path(path)
                self.result_text.setText(f"Shortest path (by distance): {' → '.join(path)}\nTotal distance: {distance} ft")
            else:
                self.result_text.setText("No path found.")

    def draw_path(self, path):
        for i in range(len(path) - 1):
            start_pos = self.campus_map.building_positions[path[i]]
            end_pos = self.campus_map.building_positions[path[i+1]]
            line = QGraphicsLineItem(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
            line.setPen(QPen(Qt.red, 3))
            self.scene.addItem(line)
            self.drawn_lines.append(line)
    
    def clear_scene(self):
        """Clear drawn paths and reset result text."""
        self.clear_drawn_paths()
        self.result_text.clear()

    def clear_drawn_paths(self):
        """Helper method to remove drawn paths from the scene."""
        for line in self.drawn_lines:
            self.scene.removeItem(line)
        self.drawn_lines.clear()

def main():
    app = QApplication(sys.argv)
    gui = CampusNavigationGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
