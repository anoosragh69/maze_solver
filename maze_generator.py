from pyamaze import maze,agent

m = maze(5,5)
m.CreateMaze()
a = agent(m)
m.run()