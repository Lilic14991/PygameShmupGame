global_var1 = []
global_var2 = 1

def func():
    global_var1.append(4)

    global_var2 = 2

    local1 = 2
    def embedded_func():
        local1 = 5
        print(local1)
    embedded_func()
    print(global_var2)

