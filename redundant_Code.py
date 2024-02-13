
    def get_Candidates(self, row, col):
        candidates = set(range(1,10))
        
        candidates -= set(self.grid[row])
    
        candidates -= set(self.grid[i][col] for i in range(9))

        boxRow = row // 3 * 3
        boxCol = col // 3 * 3
        
        candidates -= set(self.grid[i][j] for j in range(boxCol, boxCol+3) for i in range(boxRow, boxRow+3)) 
        return candidates




    def get_All_Candidates(self):

        for row in range(9):
            for col in range(9):
                candidates = set(range(1,10))
              
                candidates -= set(self.grid[row])
           
                candidates -= set(self.grid[i][col] for i in range(9))
  
                boxRow = row // 3 * 3
                boxCol = col // 3 * 3
                
                candidates -= set(self.grid[i][j] for j in range(boxCol, boxCol+3) for i in range(boxRow, boxRow+3)) 
                self.candidates[row][col] = candidates
                #print(self.candidates)
                



    def eliminate(self):
        for row in range(9):
            for col in range(9):

                if self.grid[row][col] == 0:

                    self.candidates[row][col] -= set(self.grid[row])

                    self.candidates[row][col] -= set(self.grid[i][col] for i in range(9))

                    boxRow = row // 3 * 3
                    boxCol = col // 3 * 3

                    self.candidates[row][col] -= set(self.grid[i][j] for j in range(boxCol, boxCol+3) for i in range(boxRow, boxRow+3)) 

                if len(self.candidates[row][col]) == 1:
                    self.grid[row][col] = self.candidates[row][col].pop()




