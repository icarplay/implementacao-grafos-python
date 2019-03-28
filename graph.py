

class Graph(object):

	def __init__(self, directed = False):
		self.nodesList = []
		self.edgesList = []
		self.directed = directed

		self.time = 0

	def newNode(self, node: str):
		if node.lower() not in self.nodesList:
			self.nodesList.append( node.lower() )
			self.orderListNodes()

	def newEdge(self, inputGraph: str, outputGraph: str):

		if self.directed:
			if tuple((inputGraph.lower(), outputGraph.lower())) not in self.edgesList:
				self.edgesList.append( tuple((inputGraph.lower(), outputGraph.lower())) )
				self.orderListEdges()
		else:
			if tuple((inputGraph.lower(), outputGraph.lower())) not in self.edgesList:
				if inputGraph.lower() == outputGraph.lower():
					self.edgesList.append( tuple((inputGraph.lower(), outputGraph.lower())) )
				else:
					self.edgesList.append( tuple((inputGraph.lower(), outputGraph.lower())) )
				self.orderListEdges()
	
	def orderListEdges(self):

		self.edgesList.sort(key=lambda tup: (tup[0], tup[1]))

	def orderListNodes(self):

		self.nodesList.sort()

	def searchEdge(self, u: str, v: str) -> tuple:
		for w in self.edgesList:
			initial = w[0]
			finish = w[1]

			if (initial == u and finish == v):
				return w
		
		return None
	
	def searchNode(self, node: str) -> str:

		for i in self.nodesList:
			if node.lower() == i:
				return i
			else:
				return None

	def adjacencyNodes(self, node: str) -> list:
		adjacencys = []

		for i in self.edgesList:
			if node.lower() in i:
				if node.lower() == i[0] and node.lower() == i[1]:
					adjacencys.append(i[0])
				elif node.lower() == i[0]:
					adjacencys.append(i[1])
				else:
					adjacencys.append(i[0])

		return adjacencys

	def AdjacencyList(self):

		self.adjacency_list = {}

		for i in self.nodesList:

			self.adjacency_list[i] = []

		for j in self.edgesList:

			self.adjacency_list[j[0]].append(j[1])
			self.adjacency_list[j[1]].append(j[0])

	def AdjacencyMatrix(self):

		self.adjacency_matrix = []
		self.tradutorVertices = {}

		contador = 0

		for i in self.nodesList:

			self.adjacency_matrix.append([ 0 for i in range(0, len(self.nodesList)) ])
			self.tradutorVertices[i] = contador
			self.tradutorVertices[contador] = i
			contador += 1

		for j in self.edgesList:

			posA = self.tradutorVertices[j[0]]
			posB = self.tradutorVertices[j[1]]

			self.adjacency_matrix[posA][posB] = 1
			self.adjacency_matrix[posB][posA] = 1

	def degrees(self, node: str, list_adjacency = False) -> (int, list):

		degre = 0

		adjacency = self.adjacencyNodes(node)

		for item in adjacency:

			if item == node.lower():
				degre +=2
			else:
				degre +=1

		if list_adjacency:
			return (degre, adjacency)
		else:
			return (degre)

	def components(self, node: str) -> int:
		'''
		Descrição:
		Esta é uma função faz a contagem de componentes e returna
		o número

		Utilização:
		funcao(node)

		Parâmetros:
		node
			Um vértice presente no Grafo para iniciar
		'''

		component = 0

		visitados = self.depthFirstSearch(node)

		if len(visitados) != 0:
			component+=1
		else:
			return 0

		naoVisitados = [ i for i in self.nodesList if i not in visitados ]
		
		for item in naoVisitados:
			visitadosLocal = self.depthFirstSearch(item)

			for visitar in visitadosLocal:

				if visitar not in visitados:
					visitados.append(item)
					if item in naoVisitados:
						naoVisitados.remove(item)
			
			component+=1

		return component

	def depthFirstSearch(self, node: str) -> list:
		node = node.lower()
		visitados = [node]
		fila = [node]

		while (len(fila) != 0):
			verticeVisita = fila.pop(0)

			adjacentes = self.adjacencyNodes(verticeVisita)
			verticesNaoVisitados = []
			
			for adj in adjacentes:
				if adj not in visitados:
					verticesNaoVisitados.append(adj)

			for m in verticesNaoVisitados:
				visitados.append(m)
				fila.append(m)

		return visitados

	def paridadeGraph(self, number=False) -> (bool, dict):

		paridade = True

		geral = { i : 0 for i in self.nodesList }

		for item in self.nodesList:

			numberItems = self.degrees(item)
			geral[item] = numberItems

			if paridade == True and numberItems % 2 != 0:
				paridade = False

		if number != False:
			return paridade, geral
		else:
			return paridade

	def grafoEuleriano(self, node: str) -> bool:

		paridade = self.paridadeGraph()
		componentes = self.components(node)

		if paridade == True and componentes == 1:
			return True
		else:
			return False

	def trilhaEulerianaHelper(self, node: str) -> tuple:
		'''
		Descrição:
		Esta é uma função para fazer a trilha euleriana e 
		retorna uma tupla com a trilha e se é euleriana ou não

		Utilização:
		funcao(node)

		Parâmetros:
		node
			Um vértice presente no Grafo para iniciar
		'''
		node = node.lower()

		euleriano = self.grafoEuleriano(node)

		caminho = []
		arestasVisitadas = dict()

		trilha = self.trilhaEulerianaRun(node, caminho, arestasVisitadas)
		
		return (trilha, euleriano)

	def trilhaEulerianaRun(self, node, caminho, arestasVisitadas: dict):

		for i in self.adjacencyNodes(node):

			if (node, i) in arestasVisitadas:
				if arestasVisitadas[(node, i)] == True:
					continue

			arestasVisitadas[(node, i)] = True
			arestasVisitadas[(i, node)] = True

			self.trilhaEulerianaRun(i, caminho, arestasVisitadas)
		
		caminho.append(node)

		return caminho

	def showGraph(self):
		'''
		Descrição:
		exibe os vértices e as arestas do grafo
		'''
		for i in self.adjacency_matrix:
			print(i)

	def isSafe(self, v, pos, path): 

		if self.adjacency_matrix[ path[pos-1] ][v] == 0: 
			return False

		for vertex in path: 
			if vertex == v: 
				return False
  
		return True

	def hamCycleUtil(self, path, pos): 
  
		if pos == len(self.nodesList):

			if self.adjacency_matrix[ path[pos-1] ][ path[0] ] == 1: 
				return True
			else: 
				return False

		for v in range(1, len(self.nodesList)):
  
			if self.isSafe(v, pos, path) == True: 
  
				path[pos] = v 
  
				if self.hamCycleUtil(path, pos+1) == True: 
					return True

				path[pos] = -1
  
		return False
  
	def hamCycle(self): 
		path = [-1] * len(self.nodesList)

		path[0] = 0

		if self.hamCycleUtil(path,1) == False:
			print("Não Existe Solução\n")
			return False

		self.printSolution(path) 
		return True
  
	def printSolution(self, path): 
		print("Existe Solução: ")
		for vertex in path:
			print(self.tradutorVertices[vertex])
		print(self.tradutorVertices[0], "\n")

	def componentesConexos(self):
		"""
		Descrição:
		Esta é uma função para a contagem de componentes conexos
		"""
		cc = {}

		self.idComponente = 0

		for i in self.nodesList:
			cc[i] = -1

		for i in self.nodesList:
			if cc[i] == -1:
				self.idComponente += 1
				self.dfsRcc(cc, i)
		print(cc)

		return self.idComponente

	def dfsRcc(self, cc, node):
		cc[node] = self.idComponente
		for i in self.adjacencyNodes(node):
			if cc[i] == -1:
				self.dfsRcc(cc, i)

	# def pontesDFS(self):
	# 	self.pre = {}
	# 	self.pa = {}

	# 	self.idComponente = 0

	# 	for i in self.nodesList:
	# 		self.pre[i] = -1

	# 	for i in self.nodesList:
	# 		if self.pre[i] == -1:
	# 			self.pa[i] = i
	# 			self.pontesDFSVisita(i)
		
		

	# def pontesDFSVisita(self, node):
	# 	self.idComponente += 1
	# 	self.pre[node] = self.idComponente

	# 	for i in self.adjacencyNodes(node):
	# 		if self.pre[i] == -1:
	# 			self.pa[i] = node
	# 			self.pontesDFSVisita(i)

	# def pontes(self):

	# 	self.pontesDFS()

	# 	self.vv = {}

	# 	for i in self.nodesList:
	# 		self.vv[self.pre[i]] = i
		
	# 	for i in range(len(self.nodesList) - 1, -1, -1):
	# 		# print(i)
	# 		v = self.vv[i]
	# 		mini = self.pre[v]

	# 		for adj in self.adjacencyNodes(v):
	# 			if self.pre[adj] 

	# def buscarAdjacente(self, node: str):

	# 	for adj in self.adjacencyNodes(node):

	# 		if ( adj not in self.visitados ):
	# 			self.visitados[adj] = 1
	# 			return adj
	# 	else:
	# 		return None

	def articulacao(self, node, visited: dict = {}, ap: dict = {}, parent: dict = {}, low: dict = {}, disc: dict = {}):

		children = 0

		visited[node] = True

		disc[node] = self.time
		low[node] = self.time

		self.time+=1

		for adj in self.adjacencyNodes(node):
			
			if visited[adj] == False:
				parent[adj] = node
				children+=1

				self.articulacao(adj, visited, ap, parent, low, disc)
		
				low[node] = min(low[node], low[adj])

				if parent[node] == -1 and children > 1:
					ap[node] = True

				if parent[node] != -1 and low[adj] >= disc[node]:
					ap[node] = True
			
			elif adj != parent[node]:
				low[node] = min(low[node], disc[adj])


	def articulacaoHelper(self):
		
		visited = {}
		disc = {}
		low = {}
		parent = {}
		ap = {}

		for i in self.nodesList:
			visited[i] = False
			disc[i] = float("Inf")
			low[i] = float("Inf")
			parent[i] = -1
			ap[i] = False

		for i in self.nodesList:
			if visited[i] == False:
				self.articulacao(i, visited, ap, parent, low, disc)
		
		for i in ap:
			if ap[i] == True:
				print('Articulação:', i)

		


if __name__ == "__main__":
	
	a = Graph(directed=False)

	# Não Euleriano
	# vertices = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H' ]
	# arestas = [ ('A', 'A'), ('A', 'B'), ('B','A'), ('B', 'C'), ('C', 'D'), ('A', 'E'), ('F', 'G')]

	# Teste Euleriano Simples
	# vertices = [ 'A', 'B', 'C', 'D', 'E' ]
	# arestas = [ ('A', 'B'), ('B', 'D'), ('D','E'), ('E', 'C'), ('C', 'A')]

	# Teste Euleriano Complexo
	# vertices = [ 'A', 'B', 'C', 'D', 'E', 'F']
	# arestas = [ ('A', 'B'), ('A', 'B'), ('A', 'C'), ('A','E'), ('A', 'F'), ('B', 'E'), ('B', 'D'), ('B', 'C'), ('C', 'E'), ('C', 'D'), ('E','D'), ('F', 'D')]

	# Teste de grafo simples com ligação únicas
	vertices = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G' ]
	arestas = [ ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'), ('E', 'G'), ('G', 'F') ]

	for i in vertices:
		a.newNode(i)

	for sai, entra in arestas:
		a.newEdge(sai, entra)

	a.AdjacencyList()
	a.AdjacencyMatrix()

	# a.showGraph()

	# Trilha Euleriana
	# print(a.trilhaEulerianaHelper('A'))

	# Ciclo Hamiltoniano
	# a.hamCycle()

	# Componentes
	# print('Componentes:',a.components('A'))

	# Componentes Conexos
	# print(a.componentesConexos())
	
	a.articulacaoHelper()