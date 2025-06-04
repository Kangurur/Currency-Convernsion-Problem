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
                    
    def convert(self, base_cur, final_cur="all", amount=1.0):
        dist = {}
        prev = {}
        for cur in self.currencies:
            dist[cur] = -float('inf')
            prev[cur] = None
        
        dist[base_cur] = 0 #log(1.0)=0
        n = len(self.currencies)
        for _ in range(n):
            new_dist=dist.copy()
            for cur, edges in self.graph.items():
                for result_cur, val, source in edges:
                    if dist[cur] + val > new_dist[result_cur]:
                        new_dist[result_cur] = dist[cur] + val
                        prev[result_cur] = (cur, source, val)
            dist = new_dist
                        
        if final_cur == "all":
            for cur in self.currencies:
                if dist[cur] > -float('inf'):
                    print(f"{base_cur} -> {cur}: {np.exp(dist[cur]) * amount}")
                else:
                    print(f"{base_cur} -> {cur}: No conversion available")
        else:
            if final_cur in dist and dist[final_cur] > -float('inf'):
                print(f"{base_cur} -> {final_cur}: {np.exp(dist[final_cur]) * amount}")
                print(f"Conversion path:")
                path = []
                current = final_cur
                while current is not None:
                    if prev[current] is not None:
                        path.append((prev[current][0], current, np.exp(prev[current][2])))
                    current = prev[current][0] if prev[current] else None
                path.reverse()
                for src, dest, val in path:
                    print(f"  {src} -> {dest}: {val} (source: {prev[dest][1]})")
            else:
                print(f"{base_cur} -> {final_cur}: No conversion available")
                
        
                               
XD=Converter('data.txt')
XD.check_graph()
XD.convert("pln","target")