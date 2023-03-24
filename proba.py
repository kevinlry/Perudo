def probabilite_calza (vecteur, mise_adverse):
    
    vecteur_compte= [0 for i in range(6)]
    
    for i in vecteur:
        if i>0:
            vecteur_compte[i-1]+=1
    
    n= mise_adverse[0]-vecteur_compte[mise_adverse[1]-1]
    
    if n<0 : 
        return(0)
    else:
        p=(1/6)**(n)*(5/6)**(mise_adverse[2]-n)

    return(p)

print(probabilite_calza([3,3,2,1,0],[1,3,4]))