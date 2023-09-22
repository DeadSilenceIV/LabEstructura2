import pygraphviz as pgv
from PIL import Image

class Node:
    def __init__(self, title, department, city, property_type, latitude, longitude, surface_total, surface_covered, bedrooms, bathrooms, operation_type, price, color):
        self.title = title
        self.department = department
        self.city = city
        self.property_type = property_type
        self.latitude = latitude
        self.longitude = longitude
        self.surface_total = surface_total
        self.surface_covered = surface_covered
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.operation_type = operation_type
        self.price = price
        self.metric = price / surface_total  # Calcula la métrica automáticamente
        self.left = None
        self.right = None
        self.height = 1
        self.color = color

class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if node is None:
            return 0
        return node.height

    def balance_factor(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def update_height(self, node):
        if node is not None:
            node.height = 1 + max(self.height(node.left), self.height(node.right))

    def rotate_left(self, z):
        if z is None or z.right is None:
            return z
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        self.update_height(z)
        self.update_height(y)

        return y

    def rotate_right(self, y):
        if y is None or y.left is None:
            return y
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.update_height(y)
        self.update_height(x)

        return x

    def insert(self, root, title, department, city, property_type, latitude, longitude, surface_total, surface_covered, bedrooms, bathrooms, operation_type, price,color):
        if root is None:
            return Node(title, department, city, property_type, latitude, longitude, surface_total, surface_covered, bedrooms, bathrooms, operation_type, price,color)

        if price / surface_total < root.metric:
            root.left = self.insert(root.left, title, department, city, property_type, latitude, longitude, surface_total, surface_covered, bedrooms, bathrooms, operation_type, price,color)
        else:
            root.right = self.insert(root.right, title, department, city, property_type, latitude, longitude, surface_total, surface_covered, bedrooms, bathrooms, operation_type, price,color)

        self.update_height(root)

        balance = self.balance_factor(root)

        if balance > 1:
            if price / surface_total < root.left.metric:
                return self.rotate_right(root)
            else:
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)

        if balance < -1:
            if price / surface_total > root.right.metric:
                return self.rotate_left(root)
            else:
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)

        return root

    def insert_node(self, title, department, city, property_type, latitude, longitude, surface_total, surface_covered, bedrooms, bathrooms, operation_type, price,color = 'lightblue'):
        self.root = self.insert(self.root, title, department, city, property_type, latitude, longitude, surface_total, surface_covered, bedrooms, bathrooms, operation_type, price,color)

    def delete(self, root, price, surface_total):
        if root is None:
            return root

        if price / surface_total < root.metric:
            root.left = self.delete(root.left, price, surface_total)
        elif price / surface_total > root.metric:
            root.right = self.delete(root.right, price, surface_total)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.get_min_value_node(root.right)
            root.price, root.surface_total, root.metric = temp.price, temp.surface_total, temp.metric
            root.right = self.delete(root.right, temp.price, temp.surface_total)

        self.update_height(root)

        balance = self.balance_factor(root)

        if balance > 1:
            if self.balance_factor(root.left) >= 0:
                return self.rotate_right(root)
            else:
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)

        if balance < -1:
            if self.balance_factor(root.right) <= 0:
                return self.rotate_left(root)
            else:
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)
        return root

    def delete_node(self, price, surface_total):
        self.root = self.delete(self.root, price, surface_total)

    def get_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def search_node(self, price, surface_total):
        current = self.root

        while current is not None:
            current_metric = current.price / current.surface_total

            if price / surface_total == current_metric:
                return current
            elif price / surface_total < current_metric:
                current = current.left
            else:
                current = current.right

        return None

    def search_nodes_by_criteria(self,city,bedrooms,price):
        result = []
        resultados_por_niveles = self.recorrido_por_niveles()
        if resultados_por_niveles:
            for nivel, nodos in enumerate(resultados_por_niveles, start=1):
                for nodo in nodos:
                    if nodo.city.lower() == city.lower() and nodo.bedrooms >= bedrooms and nodo.price >= price:
                        result.append(nodo)
        return result


    def recorrido_por_niveles(self):
        if self.root is None:
            return []

        resultados_por_niveles = []  # Lista para almacenar los resultados por nivel

        # Función auxiliar para realizar el recorrido por niveles de manera recursiva
        def recorrer_nivel(nodos):
            if not nodos:
                return

            nuevos_nodos = []  # Lista para almacenar los nodos del siguiente nivel
            nivel_actual = []  # Lista para almacenar los nodos del nivel actual

            for nodo in nodos:
                nivel_actual.append(nodo[0])  # Agregar el nodo actual al nivel actual
                # Agregar los hijos al nivel siguiente junto con su nivel incrementado en 1
                if nodo[0].left:
                    nuevos_nodos.append((nodo[0].left, nodo[1] + 1))
                if nodo[0].right:
                    nuevos_nodos.append((nodo[0].right, nodo[1] + 1))

            resultados_por_niveles.append(nivel_actual)  # Agregar el nivel actual a los resultados
            recorrer_nivel(nuevos_nodos)  # Llamada recursiva con los nodos del nivel siguiente

        # Comenzar el recorrido por niveles desde la raíz (nivel 1)
        recorrer_nivel([(self.root, 1)])

        return resultados_por_niveles

    def abrir_imagen(self):
        img = Image.open("temp_tree.png")
        img.show()

    def generar_imagen(self):
        if self.root:
            dot = pgv.AGraph(directed=True)

            def add_nodes_edges(node):
                if node is not None:
                    label = f"{node.metric:.1f}"
                    dot.add_node(node.title, label=label,fillcolor=node.color,style="filled")
                    if node.left:
                        dot.add_edge(node.title, node.left.title)
                        add_nodes_edges(node.left)
                    if node.right:
                        dot.add_edge(node.title, node.right.title)
                        add_nodes_edges(node.right)
            add_nodes_edges(self.root)
            dot.layout(prog='dot')
            dot.draw("temp_tree.png")

    def get_node_level(self, node):
        return self._get_node_level_recursive(self.root, node.metric, 1)

    def _get_node_level_recursive(self, node, metric_value, current_level):
        if metric_value == node.metric:
            return current_level
        elif metric_value < node.metric:
            return self._get_node_level_recursive(node.left, metric_value, current_level + 1)
        else:
            return self._get_node_level_recursive(node.right, metric_value, current_level + 1)

    def find_parent(self, node):
        if self.root is node:
            return None

        return self._find_parent_recursive(None, self.root, node.metric)


    def _find_parent_recursive(self, parent, current_node, metric_value):
        if metric_value == current_node.metric:
            return parent

        if metric_value < current_node.metric:
            return self._find_parent_recursive(current_node, current_node.left, metric_value)
        else:
            return self._find_parent_recursive(current_node, current_node.right, metric_value)

    def find_grandparent(self, node):
        if self.root is None:
            return None

        parent = self.find_parent(node)

        if parent is None:
            return None

        grandparent = self.find_parent(parent)

        return grandparent

    def find_uncle(self, node):
        if self.root is None:
            return None

        # Encuentra el nodo padre del nodo dado usando el método anterior.
        parent = self.find_parent(node)

        if parent is None:
            return None  # No se encontró el nodo padre.

        # Verifica si el nodo padre es el hijo izquierdo o derecho del abuelo.
        grandparent = self.find_parent(parent)
        if grandparent is None:
            return None  # No se encontró el nodo abuelo.

        if grandparent.left is not None and grandparent.left.metric == parent.metric:
            uncle = grandparent.right
        else:
            uncle = grandparent.left

        return uncle
