from mapclassify import EqualInterval,NaturalBreaks,MaximumBreaks,BoxPlot,Quantiles,Percentiles
import simplekml

def classify(classlist,tbclassed):
    classed = False
    for r in range(0,len(classlist)):
        if classlist[r] >= tbclassed and classed is False:
            theclass = classlist[r]
            classed = True
    return theclass

list_n = [1,2,3,3,3,10,12,65,99,88,100]
sq=MaximumBreaks(list_n,5)
print(sq,'\n',sq.bins,'\n')
list_n.sort()
class_n = []
for i in range(0,len(list_n)):
    class_n.append(classify(sq.bins,list_n[i]))
    #classed = False
    #for r in range(0,len(sq.bins)):
        #print(list_n[i],sq.bins[r])
        #if sq.bins[r] >= list_n[i] and classed is False:
        #    class_n.append(sq.bins[r])
        #    classed = True
                   
print(list_n,len(list_n))
print(class_n,len(class_n))
colours = ['#000000', '#f0f0f0', '#e4c85e', '#e9ab00', '#f79130', '#ec8115', '#ff6733', '#d04955', '8a0000', '99182e']
##sq=NaturalBreaks(list,5)
##print(sq,'\n',sq.bins,'\n')
##
##sq=MaximumBreaks(list,5)
##print(sq,'\n',sq.bins,'\n')
##
##sq=BoxPlot(list,4)
##print(sq,'\n',sq.bins,'\n')
##
##sq=Quantiles(list,5)
##print(sq,'\n',sq.bins,'\n')
##
##
##sq=Percentiles(list)
##print(sq,'\n',sq.bins,'\n')

print('simplekml colours')
[print(i) for i in dir(simplekml.Color)]
