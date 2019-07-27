This file consists of a list of instructions to use CCulture.py, a cultural algorithm to simulate a population of individuals (cells) whom each follows a belief (a color) then passes it to the next generation while selecting the 3 major beliefs that then affects their choices.

For the graphics , I used a file called graphics.py which is a simpler syntax and method to talk to the os to draw objects. It is needed for it to work. You can find it [Here](https://www.irif.fr/~sangnier/enseignement/IP1-Python/Tp10b/graphics.py)

## Here the explaination of all the variables :

- **x** and **y** are the height and weidth of the application screen in pixels.

- **space** is the space between each rectangle of the culture.

- **culture** is a list consisting of a fixed number of 3 colors. They are initially set red , green and blue by their hex represnetation.

> Do note , that alot of convertion was made due to different protocols. for example : 
the hex representation of the color white is "#ffffff" but to transform it to RGB , a convertion from hex to int is needed , but the problem is for python that color in hex is "0xFFFFFF". For that reason those fucntions are needed.

- **nb_pop** is the number of the initial population.

- **t_anim** is time in seconds for the animation.

- **speed** is a factor of speed (example: 2 means double speed)

- **nb_generation** is the number of generations until the program finishes.

- **circle_size** is the size of a cell in a population (do note that a cell's position is not unique, that means more than one can stack on top of each other)

- **j_mar** (*jump margin*) determins how much difference between two colors to deem in the same group. If it is small then similar shades of the same color with show up and the population will converge to a narrow spector of that color (hence the name jump margin) it determines the space between colors thus the likelyhood for very different colors in the selected culture.

- **nb_min_children** is the minimal number of permitted children per parents (it is recommended that the number be *>=2* for the survival of the population)

- **nb_max_children** is the maximal number of permitted children per parents (it is recommended that the number be *<=5* since the number of the population grows exponentially)

- **static** : if **True** the minimal and maximal nubmer of children will not be taken into consideration, every pair of cells with have **2 offsprings** and pass away thus the size of the population will stay fixed. if **False** each pair of cells will have offsprings between the minal and maximal number of permitted children.

- **manual** : if **True** at the end of each generation, the user must click on the mouse for it to pass to the next thus have more time to observe the changes.

- **c_perc** is a percentage for mixing colors, the formular of a new color is 
```color1*c_perc + color2*c_perc```

Do note if this value is set to 100 the population and the culture will converge to the color white and if set to 0 to the color black thus it must be set away from the edge.

- **rebel_perc** is the probabilty of a mutation happening so, an offspring will be randomly assigned a color not necessary related to his parents (a rebel that doesn't follow its parents belief you can say)

while running the application will print out a number representing the current size of the population followed by a sorted list of tuples containing each two values the value of the color in its hex representation and the number of cells having that color.

Do note this is used for debugging and more inside observation, it will be removed in future release.

# future version:
- add gifs to the documentation.
- excpetion handling.
- a gui to insert the parameters.
- the ability to change parameters while running.
