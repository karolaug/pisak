KEYBOARD = [['1','2','3','4','5','6','7','8','9','0'],['q','w','e','r','t','y','u','i','o','p'],['a','s','d','f','g','h','j','k','l'],['z','x','c','v','b','n','m'],[' ']]

#KEYBOARD = [['a','o','n','s','y','p','j','g'],['i','z','w','c','d','u','b','f'],['e','r','t','k','m','l','h',''],[' ']]

def search(e, l):
    '''for testing recrusive search, support only 2 dimensions'''
    for row in range(len(l)):
        for col in range(len(l[row])):
            if l[row][col] == e:
                return row+col+1

def search_recr(e,l):
    '''supports n dimensions'''
    if isinstance(l, list):
        for i in range(len(l)):
            b = search_recr(e, l[i])
            if b > 0:
                return b+i
    else:
        if e == l:
            return 1
    return 0

#print(search_recr('z',KEYBOARD))


text = 'mam na imie jarek i mam 30 lat'
suma=0

for a in text:
    suma += search_recr(a,KEYBOARD)
print(suma)
