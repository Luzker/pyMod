'''
Created on Mar 16, 2017

@author: slusenti
@date: 24/03/2017
@version 1.0.0
@pyVersion 2.7 or higher

This software provide a way to make static class/object in Python.
Class decorated with ModularObj are initialized and replaced with the instance.
You can use fields or function in any time by import the ModularObj instance.
Example:
[file a]
    \@MudularObj
    class my-class: 
        def test(self):
            print "hello world!"
[file b]
    from a import my-class
    my-class.test()
    
You can add a new function in any time.
To adding a function you must decorate the function with the name of ModulareObj 
instance.
The function must require at least self as parameter.
[file c]
    from a import my-class
    \@my-class
    def test1(self):
        print "i'm a my-class function!"
    my-class.test1()
    
You can override method in any time by decorate a function, that has the same 
name, with the name of ModulareObj instance. 
[file c]
    [...]
    \@my-class
    def test1(self): 
        print "override!"
    my-class.test1()
    
When you override a function the new function replace the old one, so you loose 
the old function, except if the old function is a ModularObj build-in function: 
if you want to retrieve the build-in function that was overrided, you can do it
by simply disable the new function.

You can disable and enable any function in any time, except the ModularObj 
build-in function.
For disable/enable function you have to call the build-in method:
my-class.enable(func_name)
my-class.enableAll()
my-class.disable(func_name)
my-class.disableAll()

Every function, except buildin's, are wrapped in another function: 
you can override preFunc and postFunc to do specific task before and after a 
function calling.
PreFunc takes: self, funcName and all the function parameter.
PostFunc takes: self, funcName, everything returned by preFunc and the function,
all the function parameter.

Everything returned by a function call is stored in a tuple. 
In this tuple we can find preFunc returns, function Returns and postFunc returns. 
You won't find a None type returned by a function calling: 
if nothing is returned you will find an empty tuple.
   
'''

class ModularObj:
    def __init__(self, modObj): 
        self.__staticDict__={}
        for i in modObj.__dict__:
            if type(modObj.__dict__[i])==type(lambda t:()):
                self.__call__(modObj.__dict__[i])
        self.__name__ = modObj.__name__

    def __wrapper__(self,func):
        def wrp(*arg,**karg):
            retv = self.preFunc(func.__name__,*arg,**karg)
            ret = self.__ret__(retv)
            retv = func(*arg,**karg)
            ret = ret+self.__ret__(retv)
            retv = self.postFunc(func.__name__,ret,*arg,**karg)
            ret = ret+self.__ret__(retv)
            return ret
            def __call__():
                print "ok"
        wrp.__name__ = func.__name__
        return wrp
    
    def __ret__(self,varret):
        ret = ()
        if varret!=None and type(varret)==type(()):
            ret = varret
        elif varret!=None:
            ret = (varret,) 
        return ret
        
    def preFunc(self,*arg,**karg):
        pass
    
    def postFunc(self,*arg,**karg):
        pass
    
    def __call__(self, func):
        if func.__name__!="preFunc" and func.__name__!="postFunc":
            self.__staticDict__[func.__name__] = self.__wrapper__(func.__get__(self,self))
            self.__dict__[func.__name__] = self.__staticDict__[func.__name__]
        else:  
            self.__staticDict__[func.__name__] = func.__get__(self,self)
            self.__dict__[func.__name__] = self.__staticDict__[func.__name__]
        return func
               
    def disable(self,func_name):
        self.__dict__.pop(func_name)
        
    def disableAll(self):
        for k in self.__staticDict__:
            self.__dict__.pop(k)

    def enable(self,func_name):
        self.__dict__[func_name] = self.__staticDict__[func_name]
    
    def enableAll(self):
        for k in self.__staticDict__:
            self.__dict__[k] = self.__staticDict__[k]
    
    def version(self):
        return "ModularObj ver. 1.0.0"
