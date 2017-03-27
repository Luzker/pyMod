# pyMod
This software provide a way to make static class/object in Python.
Class decorated with ModularObj are initialized and replaced with the instance.
You can use fields or function in any time by import the ModularObj instance.

```
Example:
[file a]
    \@MudularObj
    class my-class: 
        def test(self):
            print "hello world!"
[file b]
    from a import my-class
    my-class.test()
```  
You can add a new function in any time.
To adding a function you must decorate the function with the name of ModulareObj 
instance.
The function must require at least self as parameter.
```
[file c]
    from a import my-class
    \@my-class
    def test1(self):
        print "i'm a my-class function!"
    my-class.test1()
```

You can override method in any time by decorate a function, that has the same 
name, with the name of ModulareObj instance. 
```
[file c]
    [...]
    \@my-class
    def test1(self): 
        print "override!"
    my-class.test1()
```
    
When you override a function the new function replace the old one, so you loose 
the old function, except if the old function is a ModularObj build-in function: 
if you want to retrieve the build-in function that was overrided, you can do it
by simply disable the new function.

You can disable and enable any function in any time, except the ModularObj 
build-in function.
For disable/enable function you have to call the build-in method:
```
my-class.enable(func_name)
my-class.enableAll()
my-class.disable(func_name)
my-class.disableAll()
```

Every function, except buildin's, are wrapped in another function: 
you can override preFunc and postFunc to do specific task before and after a 
function calling.
PreFunc takes: self, funcName and all the function parameter.
PostFunc takes: self, funcName, everything returned by preFunc and the function,
all the function parameter.
```
@my-class
def preFunc(self,funcName,*arg,**karg):
  print "this code will be executed before every my-class function call"
  
@my-class
def postFunc(self,funcName,return,*arg,**karg):
  print "this code will be executed after every my-class function call"
```

Everything returned by a function call is stored in a tuple. 
In this tuple we can find preFunc returns, function Returns and postFunc returns. 
You won't find a None type returned by a function calling: 
if nothing is returned you will find an empty tuple.
