def original_to_basic(f):
    f=f.replace(","," ")
    text=f.splitlines()
    flag=1
    str=""
    for i in text:
        if(i==".data"):
            flag=0
        if(flag==1):
            str=str+i+"\n"
        if(i==".text"):
            flag=1
    print (str)

    return str

def text_to_original(f):
    text=f.splitlines()
    flag=1
    str=""
    for i in text:
        if(i==".data"):
            flag=0
        if(flag==1):
            str=str+i+"\n"
        if(i==".text"):
            flag=1
    print (str)

    return str
 
#string =""
#original_to_basic(string)