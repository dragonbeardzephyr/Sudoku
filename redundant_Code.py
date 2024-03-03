
    def get_Candidates(self, row, col):
        candidates = set(range(1,10))
        
        candidates -= set(self.grid[row])
    
        candidates -= set(self.grid[i][col] for i in range(9))

        boxRow = row // 3 * 3
        boxCol = col // 3 * 3
        
        candidates -= set(self.grid[i][j] for j in range(boxCol, boxCol+3) for i in range(boxRow, boxRow+3)) 
        return candidates




    

                