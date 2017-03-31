# pyMod
This software provide a way to make static class/object in Python.
Class decorated with ModularObj are initialized and replaced with the instance.
You can use fields or function in any time by import the ModularObj instance.

```
Example:
[file a]
    @MudularObj
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
    @my-class
    def test1(self):
        print "i'm a my-class function!"
    my-class.test1()
```

You can override method in any time by decorate a function, that has the same 
name, with the name of ModulareObj instance. 
```
[file c]
    [...]
    @my-class
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
you can make the instance immutable by call build-in mkImmutable function. when an istance is immutable you cannot add, override, disable or enable function and you cannot add or modify attributes. you can only use attribute or functions.
```
my-class.mkImmutable()
```

Every function, except build-in's, are wrapped in another function: 
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

!!replace self attribute. 
in this version of ModularObj you will make an object by "join" 
two or more instanced object.
this obj will be destroyed after function execution.
```
[file d]
    @my-class-1
    @my-class-2
    def test(self): 
        pass
```

in this function self has all attribute of my-class-1 and all 
attribute of my-class-2

bind can execute a function every event or every [sec] seconds:

* for binding a function by time you must provide: 
function reference, how many second must be wait befor every execution,
and a dictionary of key arguments. the binder will call the function passing
all the key argument stored in kargs.
```
bind.time(func,sec,kargs)
```

* bind a function by event name you must provide: 
the event name and the function reference. the function will be call when 
an event witch has event.name equals to eventName is raised. 
when the event occurs the bind call the function with event arguments. 
```
bind.event(eventName,func)
```

the event is used by the raiseEvent method to load a new event, the event will 
be caught by the binder. the binder call every function binded with that specifical
event.name and pass the arguments stored in event.kargs
```
e = event(eventName, kargs)
raiseEvent(e)
```
