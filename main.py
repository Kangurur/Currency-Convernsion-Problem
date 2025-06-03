import numpy as np
import heapq
from math import floor

class Converter:
    def __init__(self, file:str):
        #self.n = 0
        self.graph = {}
        self.currencies = set()
        
        with open(file, 'r') as f:
            for line in f:
                data = line.strip().split()
                source = data[0] if data[0][-1] != ':' else data[0][:-1]
                base_cur = data[1]
                result_cur = data[2]
                #val = float(data[3])
                val = np.log(np.float64(data[3]))
                if base_cur not in self.graph:
                    self.graph[base_cur] = []
                    #self.n+=1
                self.graph[base_cur].append((result_cur, val, source))
                self.currencies.add(base_cur)
                self.currencies.add(result_cur)
                
    def check_graph(self):
        for base_cur, edges in self.graph.items():
                for result_cur, val, source in edges:
                    print(f"  {base_cur} -> {result_cur}: {np.exp(val)} (source: {source})")
                    
    def convert(self, base_cur, result_cur="all", amount=1.0):
        dist = {}
        prev = {}
        for cur in self.currencies:
            dist[cur] = -float('inf')
            prev[cur] = None
        
        dist[base_cur] = 0 #log(1.0)=0
        pq = [(0, base_cur)]
        
        while pq:
            current_dist, current_cur = heapq.heappop(pq)
            
            if current_dist < dist[current_cur]:
                continue
            
            for neighbor, weight, source in self.graph.get(current_cur, []):
                distance = current_dist + weight
                
                if distance > dist[neighbor]:
                    dist[neighbor] = distance
                    prev[neighbor] = (current_cur, source, weight)
                    heapq.heappush(pq, (distance, neighbor))
                    
        if result_cur != "all":
            if result_cur in dist:
                return np.exp(dist[result_cur]) * amount
            else:
                raise ValueError(f"Currency {result_cur} not found in the graph.")
        else:
            results = {}
            for cur in dist:
                if dist[cur] > -float('inf'):
                    results[cur] = floor(float(np.exp(dist[cur]) * amount*100))/100
            return results
        
                    
                    



XD=Converter('data.txt')
XD.check_graph()
print(XD.convert("pln"))