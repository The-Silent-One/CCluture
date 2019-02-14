from graphics import *
from time import *
import random
import operator
x,y=500,500
space=1
random.seed(None)

culture=['#ff0000','#00ff00','#0000ff']
nb_pop=10
t_anim=2
speed=10
nb_generation=100
circle_size=4
j_mar=5
nb_min_children=2
nb_max_children=5

#boolean
static=False
manual=True

#percentages
c_perc=50
rebel_perc=2


def build_scene(x,y):
    win = GraphWin("Cultural Algorithm",x,y)
    divL = Line(Point(0,y/2),Point(x,y/2))
    divL.setWidth(3)
    divL.setOutline(color_rgb(200,200,200))
    divL.draw(win)
    return win

def build_culture(win,culture):
    rect1 = Rectangle(Point(x/4,y/8),Point(5*x/12,3*y/8))
    rect1.setOutline('black')
    rect1.setFill(culture[0])
    rect1.draw(win)

    rect2 = Rectangle(Point(5*x/12+space,y/8),Point(7*x/12,3*y/8))
    rect2.setOutline('black')
    rect2.setFill(culture[1])
    rect2.draw(win)
    
    rect3 = Rectangle(Point(7*x/12+space,y/8),Point(3*x/4,3*y/8))
    rect3.setOutline('black')
    rect3.setFill(culture[2])
    rect3.draw(win)
    return [rect1,rect2,rect3]

def build_population(win,nb_pop):
    pop=[]
    for i in range(nb_pop):
        px=random.uniform(x/10,9*x/10)
        py=random.uniform(3*y/5,9*y/10)
        pop.append(Circle(Point(px,py),circle_size))
        pop[i].draw(win)
        sleep(0.5/speed)
    return pop

def update_pop(pop,next_pop):
    for i in range(len(pop)):
        pop[i].setFill(next_pop[i])

def shift(win,pop):
    t1=time()
    t2=time()
    while t2-t1< t_anim:
        for i in pop:
            i.move(0,2)
            sleep(0.1/speed)
            i.move(0,-2)
        t2=time()
    
def first_generation(win,pop):
    for i in pop:
        rand_c=int(random.uniform(0,3))
        i.setFill(culture[rand_c])
    shift(win,pop)

def new_generation(win,pop,pop_c):
    for i in range(len(pop)):
        pop[i].setFill(pop_c[i])
    
def var_selection(parent1,parent2):
    color1=parent1.config['fill']
    color2=parent2.config['fill']
    #print(nb_children)
    nb_children=int(random.uniform(nb_min_children,nb_max_children+1))
    if(nb_children>=2):
        rebel=int(random.uniform(1,101))
        if(rebel<=rebel_perc):
            ch1=mutation()
        else:
            ch1=color1
        rebel=int(random.uniform(1,101))
        if(rebel<=rebel_perc):
            ch2=mutation()
        else:
            ch2=color2
        ch=[ch1,ch2]
        for i in range(nb_children-2):
            rebel=int(random.uniform(1,101))
            if(rebel<=rebel_perc):
                ch.append(mutation())
            else:
                ch.append(RGBtohex(mix2(color1,color2,c_perc/(i+1))))
    elif(nb_children==1):
        rebel=int(random.uniform(1,101))
        if(rebel<=rebel_perc):
            ch1=mutation()
        else:
            ch1=color1
        ch=[ch1]
    elif(nb_children==0):
        return []
    return ch
            
def static_selection(parent1,parent2):
    color1=parent1.config['fill']
    color2=parent2.config['fill']
    rebel=int(random.uniform(1,101))
    #print("rebel : {0} \n".format(rebel))
    if(rebel<=rebel_perc):
        traditional=mutation()
    else:
        rand_c=int(random.uniform(0,2))
        traditional=[color1,color2][rand_c]
    rebel=int(random.uniform(1,101))
    #print("rebel : {0}\n".format(rebel))
    if(rebel<=rebel_perc):
        hybrid=mutation()
    else:
        hybrid=RGBtohex(mix2(color1,color2,c_perc))
    return [traditional,hybrid]

def ith_generation(win,pop):
    tmp=pop.copy()
    next_pop=[]
    while (len(tmp)>1) :
        p1 = int(random.uniform(0,len(tmp)))
        p2 = int(random.uniform(0,len(tmp)))
        while(p1==p2):
            p2 = int(random.uniform(0,len(tmp)))
        if(static):
            np=static_selection(tmp[p1],tmp[p2])
            for i in np:
                next_pop.append(i)
        else:
            np=var_selection(tmp[p1],tmp[p2])
            if(len(np)>=2):
                for i in np[:2]:
                    next_pop.append(i)
                new_g=build_population(win,len(np)-2)
                pop=pop+new_g
                for i in np[2:]:    
                    next_pop.append(i)
            elif(len(np)==1):
                next_pop.append(np[0])
                pop.remove(tmp[p1])
                kill_pop(win,[tmp[p1]])
            else:
                pop.remove(tmp[p1])
                pop.remove(tmp[p2])
                kill_pop(win,[tmp[p1],tmp[p2]])
        tmp.pop(p1)
        if(p1<p2):
            tmp.pop(p2-1)
        else:
            tmp.pop(p2)
    if(len(tmp)==1):
        next_pop.append(tmp.pop(0).config["fill"])
    update_pop(pop,next_pop)
    return pop

def hextoRGB(color):
    r=int(color[1:3],16)
    g=int(color[3:5],16)
    b=int(color[5:],16)
    return [r,g,b]

def kill_pop(win,pop):
    for i in pop:
        i.undraw()

def RGBtohex(color):
    hr = hex(color[0])[2:]
    hg = hex(color[1])[2:]
    hb = hex(color[2])[2:]
    if(len(hr)<2):
        hr="0"+hr
    if(len(hg)<2):
        hg="0"+hg
    if(len(hb)<2):
        hb="0"+hb
    return "#"+hr+hg+hb

def mix(c1,c2):
    c1=hextoRGB(c1)
    c2=hextoRGB(c2)
    return [min(c1[i]+c2[i],255) for i in range(0,3)]

def mix2(c1,c2,p):
    if(p>100):
        p=100
    c1=hextoRGB(c1)
    c2=hextoRGB(c2)
    return[int(min(c1[i]*p/100+c2[i]*p/100,255)) for i in range(0,3)]

def color_sorter(pop):
    colors=dict()
    for i in pop:
        if(i.config['fill'] not in colors):
            colors[i.config['fill']]=1
        else:    
            colors[i.config['fill']]=colors.get(i.config['fill'])+1
    return sorted(colors.items(),reverse=True,key=operator.itemgetter(1))

def update_culture(c,pop):
    tmp =color_sorter_filter(pop)[:3]
    if(len(tmp)>=1):
        c[0].setFill(tmp[0][0])
    if(len(tmp)>=2):
        c[1].setFill(tmp[1][0])
    if(len(tmp)==3):
        c[2].setFill(tmp[2][0])
    return c

def hextosum(color):
    rgb=hextoRGB(color)
    s=0
    for i in range(len(rgb)):
        s+=rgb[-i-1]*(256**i)
    return s

def sumtohex(s):
    rgb=[0,0,0]
    i=2
    while(i>=0):
        rgb[i]=s % 256
        s=int(s/256)
        i=i-1
    return RGBtohex(rgb)

def similar_color(c,pop_color):
    culture=["","",""]
    for i in range(len(c)):
        culture[i]=c[i].config['fill']
    mar=[[],[],[]]
    x=hextosum(pop_color)
    for i in range(len(culture)):
        mar[i]=[abs(hextosum(culture[i])-x),culture[i]]
    sorted(mar,key=operator.itemgetter(0))
    return mar[0]

def similar_with_mar(c,colors,mar):
    x=hextoRGB(c[0])
    index=[]
    for i in colors:
        tmp = hextoRGB(i[0])
        if(abs(x[0]-tmp[0])<=mar and abs(x[1]-tmp[1])<=mar
           and abs(x[2]-tmp[2])<=mar):
            index.append(i)
    return index

def color_sorter_filter(pop):
    tmp1=color_sorter(pop)
    tmp2=tmp1.copy()
    for i in tmp1:
        res=similar_with_mar(i,tmp2,j_mar)
        if(len(res)!=1):
            count=0
            for j in res:
                count=count+j[1]
                tmp2.remove(j)
            tmp2.append(tuple([i[0],count]))
    return sorted(tmp2,key=operator.itemgetter(1),reverse=True)
    
def pop_to_culture(c,pop):
    for i in pop:
        tmp = RGBtohex(mix2(similar_color(c,i.config['fill'])[1],i.config['fill'],c_perc))
        i.setFill(tmp)

def mutation():
    s=int(random.uniform(0,hextosum("#ffffff")+1))
    res=sumtohex(s)
    #print("mutation happened ! color : "+res+"\n");
    return res
    
def main():
    win = build_scene(x ,y)
    c=build_culture(win,culture)
    pop=build_population(win,nb_pop)
    win.getMouse()
    first_generation(win,pop)
    win.getMouse()
    for i in range(nb_generation):
        print(len(pop))
        print(color_sorter_filter(pop))
        c=update_culture(c,pop)
        pop_to_culture(c,pop)
        pop=ith_generation(win,pop)
        shift(win,pop)
        sleep(1/speed)
        if(manual):
            win.getMouse()
    win.close()
main()
