import heapq

class STC:
    def generate_path(self, sub_grid, path_from, grid, start_point):
        path_set_bi = set()
        for k, v in path_from.items():
            if v is not None:
                path_set_bi.add((k, v))
                path_set_bi.add((v, k))
        
        rows, cols = len(grid), len(grid[0])

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    sub_grid[r*2][c*2] = sub_grid[r*2+1][c*2] = sub_grid[r*2][c*2+1] = sub_grid[r*2+1][c*2+1] = 1

        path = []
        stack = [(start_point[0] * 2, start_point[1] * 2)]
        visited = set()
        
        while stack:
            r, c = stack[-1]
            if (r, c) not in visited:
                visited.add((r, c))
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                for dr, dc in directions:
                    rr, cc = r + dr, c + dc
            
                    if 0 <= rr < len(sub_grid) and 0 <= cc < len(sub_grid[0]) and sub_grid[rr][cc] == 0 and (rr, cc) not in visited:
              
                        if r // 2 == rr // 2 and c // 2 == cc // 2:
                            outside = (r // 2, c // 2)
                            if c % 2 == 0 and cc % 2 == 0 \
                            and path_set_bi.__contains__((outside, (outside[0], outside[1] - 1))):
                                continue
                            if c % 2 == 1 and cc % 2 == 1 \
                            and path_set_bi.__contains__((outside, (outside[0], outside[1] + 1))):
                                continue
                            if r % 2 == 0 and rr % 2 == 0 \
                            and path_set_bi.__contains__((outside, (outside[0] - 1, outside[1]))):
                                continue
                            if r % 2 == 1 and rr % 2 == 1 \
                            and path_set_bi.__contains__((outside, (outside[0] + 1, outside[1]))):
                                continue
                    
                        else:
                            if (r // 2, c // 2) != (rr // 2, cc // 2) and not path_set_bi.__contains__(((r // 2, c // 2), (rr // 2, cc // 2))):
                                continue
                        stack.append((rr, cc))
                        path.append((r, c))
                        path.append((rr, cc))
                        break
                else:
                    stack.pop()
            else:
                stack.pop()

        return path

    def subdivide_grid(self, grid):
        sub_rows, sub_cols = len(grid) * 2, len(grid[0]) * 2
        sub_grid = [[0 for _ in range(sub_cols)] for _ in range(sub_rows)]

  
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                sub_grid[r*2][c*2] = grid[r][c]
                sub_grid[r*2+1][c*2] = grid[r][c]
                sub_grid[r*2][c*2+1] = grid[r][c]
                sub_grid[r*2+1][c*2+1] = grid[r][c]

        return sub_grid

    def plan_path(self, grid=[[0,0,1,0], [0,0,1,0], [0,0,0,0], [0,0,0,0]], start_point=(0,0)):
        rows, cols = len(grid), len(grid[0])

        mst = set()
        path_from = {}
        visit_order = {}
        order = 1
        # print("start_point", start_point)
        edges = [(0, start_point, None)] 

        # Generate the MST
        while edges and len(mst) < rows * cols:
            weight, (r, c), from_cell = heapq.heappop(edges)
            if (r, c) in mst:
                continue
            mst.add((r, c))
            if from_cell is not None:
                path_from[(r, c)] = from_cell
            visit_order[(r, c)] = order
            order += 1
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                rr, cc = r + dr, c + dc
                if 0 <= rr < rows and 0 <= cc < cols and (rr, cc) not in mst and grid[rr][cc] == 0:
                    heapq.heappush(edges, (1, (rr, cc), (r, c)))

        sub_grid = self.subdivide_grid(grid)
        
        hamiltonian_path = self.generate_path(sub_grid, path_from, grid, start_point)

        return hamiltonian_path