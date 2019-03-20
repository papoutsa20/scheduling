import copy
# this program is a sceduling algortium that uses the greedy approach

#the assumption is that resources are unlimited

# Got this from https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
scheduling = []


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_simplified(s):
    return s[0] == "(" and s[len(s)-1] == ")"


def is_var(s):
    return is_number(s) or (ord(s) in list(range(65, 90)) + list(range(97, 122)))

#this function looks at all the cases that a single equation may be faced with


def is_schedulable(x,scdulingLevel,index):

    #if the operand has two numbers next to it, can be scedulaed
    if is_var(x[index-1]) and is_var(x[index+1]):
        # -10,-9,-11,is an code that the opperation doesn't contain any previous sceduled
        return True, x[index-1:index+2]

    #if both numbers next to the opperand have been sceduled, then check if it can be scduled
    if x[index-1] is "#" and x[index+1] is "#":
        if int(x[index - 3]) < scdulingLevel and int(x[index+2]) < scdulingLevel:
            return True, x[index - 4:index + 5]
        return False, -12
        # if next to paraenthesis, can't be
    if x[index + 1] is "~" or x[index - 1] is "~":
        return False, -11
   #if one number has been sceduled, check
    if x[index-1] is "#":
        if int(x[index-3]) < scdulingLevel:
            return True, x[index-4:index+2]
        else:
            return False, -9
    # if one number has been sceduled, check
    if x[index+1] is "#":
        if int(x[index+2]) < scdulingLevel:
            return True, x[index-1:index+5]
        return False, -10
    # if next to paraenthesis, can't be
    if x[index+1] is "~" or x[index-1] is "~":
        return False, -11


def schedulor(x, secdulinglist, secdulingLevel, count):
    #this are needed because we may have to skip some values
    DUMMY_VALUES = {"*":"~00~","/":"~01~","+":"~10~","-":"~11~"}
    while "*" in x or "/" in x:
        div = "/" in x
        magicIndex = x.find("/") if div else x.find("*")



        boolen, equ = is_schedulable(x,secdulingLevel,magicIndex)

        if boolen:
            x = x.replace(equ,"#" + str(secdulingLevel) + chr(count) + "#")
            secdulinglist.append(equ)
            count+=1
        else:
            x = x.replace(x[magicIndex], DUMMY_VALUES[x[magicIndex]],1)
    x = x.replace(DUMMY_VALUES["*"],"*")
    x = x.replace(DUMMY_VALUES["/"], "/")
    for w in ("*","/"):
        if w in x:
         return x,secdulinglist, count
    while "+" in x or "-" in x:
        add = "+" in x
        magicIndex = x.find("+") if add else x.find("-")
        boolen, equ = is_schedulable(x, secdulingLevel, magicIndex)

        if boolen:
            x = x.replace(equ, "#" + str(secdulingLevel) + chr(count) + "#")
            secdulinglist.append(equ)
            count += 1
        else:
            x = x.replace(x[magicIndex], DUMMY_VALUES[x[magicIndex]], 1)
    x = x.replace(DUMMY_VALUES["+"], "+")
    x = x.replace(DUMMY_VALUES["-"], "-")
    if (x[1] is "#" and x[len(x) - 2] is "#"):
        x = x[1:len(x) - 1]
    return x, secdulinglist, count








def display(equations):
    count = 0
   # display each sceduling level
    for x in equations:

        charValue = 97
        print("/******" + str(count) + "******/")
        # for each asigment in the sceduling level
        for y in x:
            print(y + " = #" + str(count)+chr(charValue) + "#")
            print()
            charValue+=1
        print("/*************")
        print()
        count+=1


def GreedyAlg(experssion):
    scheduling = []
    recordOfEquations = {}
    secdulinglist = []
    numberOfPer = 97
    parEqu = []
    secdulingLevel = 0

    # first step is to scedule the parenesis
    while "(" in experssion:
         #spliting the string into each parenesie function
         x = experssion[experssion.rfind("("): experssion[experssion.rfind("("):len(experssion)].find(")") +\
                                               1 + len(experssion[0:experssion.rfind("(")])]

         experssion = experssion.replace(x, "~P"+chr(numberOfPer) + "P~")
         recordOfEquations[x] = "~P"+chr(numberOfPer) + "P~"
         numberOfPer+=1
         parEqu.append(x)
    if not is_simplified(experssion):
        parEqu.append(experssion)
    # at this point, the experssion has been simplified to smaller independent pieces
    # which can all be sceduled
    count = 97
    #gooding through each equations and sceduling it
    while (len(parEqu) > 0):
        for ex in parEqu:
            newEx, secdulinglist, count,= schedulor(ex,secdulinglist,secdulingLevel,count)
            if newEx != ex:
                #updating dictionary with a new value
                try:
                    temp = recordOfEquations[ex]
                    del recordOfEquations[ex]
                    recordOfEquations[newEx] = temp
                except KeyError:
                        print()
                parEqu.insert(parEqu.index(ex),newEx)
                parEqu.remove(ex)

    #if the experssion has finished, replace it in all the areas it is in the bigger equation

# here we are replacing each para value with the evaulted value and then deleting that equation

        tempdic = {}
        for ex in parEqu:
            if(len(ex) == 4):
                try:
                    parvalue = recordOfEquations[ex]
                    for ex2 in parEqu:
                        parEqu[parEqu.index(ex2)] = ex2.replace(parvalue,ex)
                    for ex3 in recordOfEquations.keys():
                        if parvalue in ex3:
                            temp = recordOfEquations[ex3]
                            temp1 = ex3.replace(parvalue,ex)
                            tempdic[temp1] = temp
                        else:
                            tempdic[ex3] = recordOfEquations[ex3]

                    parEqu.insert(parEqu.index(ex),"DELETE")
                    parEqu.remove(ex)
                except KeyError:
                    print()
            if ex in recordOfEquations.keys():
                tempdic[ex] = recordOfEquations[ex]



        parEqu[:] = [w for w in parEqu if w != "DELETE"]
        recordOfEquations = tempdic
        secdulingLevel+=1
        scheduling.append(copy.deepcopy(secdulinglist))
        secdulinglist.clear()
        count = 97
        # break out if this is true
        if len(parEqu) == 1 and len(parEqu[0]) == 4:
            break
    display(scheduling)









































# first we ask the user for an equation
print("please enter a equation with simple PEMDAS operations")
equation = input()
GreedyAlg(equation)






