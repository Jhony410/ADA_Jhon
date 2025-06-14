import tkinter as tk
from tkinter import ttk
import math
import random
from collections import defaultdict

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n)) # Cada nodo es su propio padre inicialmente
        self.rank = [0] * n
    
    def find(self, x): # Encontrar raíz con compresión de caminos
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y): # Unir dos componentes
        px, py = self.find(x), self.find(y)
        if px == py:
            return False# Ya están conectados (formaría ciclo)
        # Union por rango para eficiencia
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True # Conexión exitosa

class MSTVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Algoritmos MST - Kruskal vs Prim")
        self.root.geometry("1000x700")
        
        # Variables
        self.nodes = []  # [(x, y, id), ...]
        self.edges = []  # [(node1_id, node2_id, weight), ...]
        self.mst_edges = []
        self.node_counter = 0
        self.dragging = False
        self.drag_node = None
        self.algorithm = "none"
        
        # Colores
        self.colors = {
            'kruskal': '#FF6B6B',  # Rojo coral para Kruskal
            'prim': '#4ECDC4',     # Turquesa para Prim
            'node': '#FFE66D',     # Amarillo para nodos
            'edge': '#95A5A6',     # Gris para aristas normales
            'background': '#2C3E50' # Azul oscuro de fondo
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de controles
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botones
        ttk.Button(control_frame, text="Añadir Nodo", 
                  command=self.add_node).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Limpiar Todo", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        # Separador
        ttk.Separator(control_frame, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Botones de algoritmos
        ttk.Button(control_frame, text="🔴 Ejecutar Kruskal", 
                  command=self.run_kruskal).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="🔷 Ejecutar Prim", 
                  command=self.run_prim).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Limpiar MST", 
                  command=self.clear_mst).pack(side=tk.LEFT, padx=5)
        
        # Canvas para dibujar
        self.canvas = tk.Canvas(main_frame, bg=self.colors['background'], 
                               width=980, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Eventos del mouse
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        # Frame de información
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.info_label = ttk.Label(info_frame, 
                                   text="Haz clic en 'Añadir Nodo' para empezar. Los nodos se conectarán automáticamente.")
        self.info_label.pack()
        
    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def add_node(self):
        # Posición aleatoria en el canvas
        x = random.randint(50, 930)
        y = random.randint(50, 550)
        
        # Evitar superposición con nodos existentes
        while any(self.distance((x, y), (nx, ny)) < 60 for nx, ny, _ in self.nodes):
            x = random.randint(50, 930)
            y = random.randint(50, 550)
        
        self.nodes.append((x, y, self.node_counter))
        
        # Conectar automáticamente con todos los nodos existentes
        current_node = self.node_counter
        for _, _, node_id in self.nodes[:-1]:  # Excluir el nodo actual
            weight = int(self.distance((x, y), 
                                     next((nx, ny) for nx, ny, nid in self.nodes if nid == node_id)))
            self.edges.append((min(current_node, node_id), 
                             max(current_node, node_id), weight))
        
        self.node_counter += 1
        self.clear_mst()
        self.draw_graph()
        self.update_info()
    
    def clear_all(self):
        self.nodes = []
        self.edges = []
        self.mst_edges = []
        self.node_counter = 0
        self.algorithm = "none"
        self.canvas.delete("all")
        self.update_info()
    
    def clear_mst(self):
        self.mst_edges = []
        self.algorithm = "none"
        self.draw_graph()
    
    def get_node_at_position(self, x, y):
        for nx, ny, node_id in self.nodes:
            if self.distance((x, y), (nx, ny)) <= 20:
                return node_id
        return None
    
    def on_click(self, event):
        node_id = self.get_node_at_position(event.x, event.y)
        if node_id is not None:
            self.dragging = True
            self.drag_node = node_id
    
    def on_drag(self, event):
        if self.dragging and self.drag_node is not None:
            # Actualizar posición del nodo
            for i, (x, y, node_id) in enumerate(self.nodes):
                if node_id == self.drag_node:
                    self.nodes[i] = (event.x, event.y, node_id)
                    break
            
            # Recalcular pesos de las aristas
            self.recalculate_edges()
            self.clear_mst()
            self.draw_graph()
    
    def on_release(self, event):
        self.dragging = False
        self.drag_node = None
    
    def recalculate_edges(self):
        # Recalcular todas las aristas basándose en las nuevas posiciones
        new_edges = []
        node_positions = {node_id: (x, y) for x, y, node_id in self.nodes}
        
        for node1_id, node2_id, _ in self.edges:
            pos1 = node_positions[node1_id]
            pos2 = node_positions[node2_id]
            weight = int(self.distance(pos1, pos2))
            new_edges.append((node1_id, node2_id, weight))
        
        self.edges = new_edges
    
    def run_kruskal(self):
        if len(self.nodes) < 2:
            self.info_label.config(text="Necesitas al menos 2 nodos para ejecutar Kruskal")
            return
        
        self.algorithm = "kruskal"
        self.mst_edges = []
        
        # ===== AQUÍ EMPIEZA EL ALGORITMO DE KRUSKAL =====
        # Paso 1: Ordenar todas las aristas por peso
        edges_sorted = sorted(self.edges, key=lambda x: x[2])
        
        # Paso 2: Inicializar Union-Find para detectar ciclos
        uf = UnionFind(self.node_counter)
        
        # Paso 3: Procesar aristas en orden de peso
        for node1, node2, weight in edges_sorted:
            # Si los nodos están en componentes diferentes (no forma ciclo)
            if uf.union(node1, node2):
                # Añadir arista al MST
                self.mst_edges.append((node1, node2, weight))
                # Parar cuando tengamos n-1 aristas
                if len(self.mst_edges) == len(self.nodes) - 1:
                    break
        
        self.draw_graph()
        total_weight = sum(weight for _, _, weight in self.mst_edges)
        self.info_label.config(text=f"🔴 Kruskal completado - Peso total del MST: {total_weight}")
    
    def run_prim(self):
        if len(self.nodes) < 2:
            self.info_label.config(text="Necesitas al menos 2 nodos para ejecutar Prim")
            return
        
        self.algorithm = "prim"
        self.mst_edges = []
        
        # Algoritmo de Prim
        if not self.nodes:
            return
        
        # ===== AQUÍ EMPIEZA EL ALGORITMO DE PRIM =====
        # Paso 1: Crear grafo de adyacencia
        graph = defaultdict(list)
        for node1, node2, weight in self.edges:
            graph[node1].append((node2, weight))
            graph[node2].append((node1, weight))
        
        # Paso 2: Empezar desde el primer nodo
        start_node = self.nodes[0][2]
        visited = {start_node} # Nodos ya incluidos en el MST
        edges_available = [] # Aristas disponibles para expandir
        
        # Paso 3: Añadir todas las aristas del nodo inicial
        for neighbor, weight in graph[start_node]:
            edges_available.append((weight, start_node, neighbor))
        
        edges_available.sort() # Mantener ordenadas por peso
        
        # Paso 4: Crecer el árbol iterativamente
        while edges_available and len(self.mst_edges) < len(self.nodes) - 1:
            # Tomar la arista más barata disponible
            weight, node1, node2 = edges_available.pop(0)
            
            # Si el nodo destino ya está visitado, saltar
            if node2 in visited:
                continue
            
            # Añadir arista al MST
            self.mst_edges.append((node1, node2, weight))
            visited.add(node2)
            
            # Añadir nuevas aristas disponibles desde el nuevo nodo
            for neighbor, w in graph[node2]:
                if neighbor not in visited:
                    edges_available.append((w, node2, neighbor))
                    edges_available.sort()
        
        self.draw_graph()
        total_weight = sum(weight for _, _, weight in self.mst_edges)
        self.info_label.config(text=f"🔷 Prim completado - Peso total del MST: {total_weight}")
    
    def draw_graph(self):
        self.canvas.delete("all")
        
        # Dibujar aristas normales
        for node1, node2, weight in self.edges:
            pos1 = next((x, y) for x, y, nid in self.nodes if nid == node1)
            pos2 = next((x, y) for x, y, nid in self.nodes if nid == node2)
            
            # Verificar si esta arista está en el MST
            is_mst_edge = any((n1 == node1 and n2 == node2) or (n1 == node2 and n2 == node1) 
                             for n1, n2, _ in self.mst_edges)
            
            if is_mst_edge:
                color = self.colors[self.algorithm] if self.algorithm != "none" else self.colors['edge']
                width = 4
            else:
                color = self.colors['edge']
                width = 1
            
            self.canvas.create_line(pos1[0], pos1[1], pos2[0], pos2[1], 
                                  fill=color, width=width, tags="edge")
            
            # Dibujar peso en el medio de la arista
            mid_x = (pos1[0] + pos2[0]) // 2
            mid_y = (pos1[1] + pos2[1]) // 2
            self.canvas.create_text(mid_x, mid_y, text=str(weight), 
                                  fill="white", font=("Arial", 8, "bold"))
        
        # Dibujar nodos
        for x, y, node_id in self.nodes:
            self.canvas.create_oval(x-20, y-20, x+20, y+20, 
                                  fill=self.colors['node'], outline="white", width=2)
            self.canvas.create_text(x, y, text=str(node_id), 
                                  fill="black", font=("Arial", 12, "bold"))
    
    def update_info(self):
        if not self.nodes:
            self.info_label.config(text="Haz clic en 'Añadir Nodo' para empezar. Los nodos se conectarán automáticamente.")
        else:
            self.info_label.config(text=f"Nodos: {len(self.nodes)} | Aristas: {len(self.edges)} | Arrastra los nodos para moverlos")

if __name__ == "__main__":
    root = tk.Tk()
    app = MSTVisualizer(root)
    root.mainloop()