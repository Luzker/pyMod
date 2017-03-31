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
import sys, time, cPickle, os 
from threading import Thread
from socket import socket, AF_UNIX, SOCK_STREAM

socketPath="/tmp/SCK"+str(int(time.time()))

'''
this method send created event to the bind class
event must be a string! 
'''
def raiseEvent(event):
    if event.__class__.__name__=="event":
        s = socket(AF_UNIX,SOCK_STREAM)
        s.connect(socketPath)
        s.send(str(event).encode())
        s.close()
    else:
        raise AttributeError("Expected \"event\" got \""+event.__class__.__name__+"\"")
    pass

'''
obj replace self attribute. this class make an object by "join" 
two or more instanced object.
the obj will be destroyed after function execution.

[file d]
    \@my-class-1
    \@my-class-2
    def test(self): 
        pass

in this function self has all attribute of my-class-1 and all 
attribute of my-class-2
'''
class obj:
    def __getattr__(self,fname):
        try:
            return self.__dict__[self.__name__].__dict__[fname]
        except:
            for d in self.__dict__:
                try:
                    return self.__dict__[d].__dict__[fname]
                except: pass
        raise AttributeError("ModularObj has no attribute "+fname) 
        pass
                
    def __setattr__(self,name,value):
        for d in self.__dict__:
            try:
                self.__dict__[d].__setattr__(name,value)
            except: pass
        pass
    pass

class ModularObj:
    def __init__(self, modObj):
        if not self.__dict__.has_key("__name__"): 
            self.__staticDict__={}
            self.__name__ = modObj.__name__
            for i in modObj.__dict__:
                if type(modObj.__dict__[i])==type(lambda t:()):
                    self.__call__(modObj.__dict__[i])
            if self.__dict__.has_key("_init"):
                self._init()
        else:
            raise SyntaxError("Can not initialize ModularObj twice")
        pass

    def __wrapper__(self,func):
        def wrp(*arg,**karg):
            retv = self.preFunc(func.__name__,*arg,**karg)
            ret = self.__ret__(retv)
            retv = func(*arg,**karg)
            ret = ret+self.__ret__(retv)
            retv = self.postFunc(func.__name__,ret,*arg,**karg)
            ret = ret+self.__ret__(retv)
            return ret
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
    
    def __selfWrp__(self,func):
        try:
            func.__fDict__[self.__name__] = self
            return func 
        except:
            def funcWrp(self,*args,**kargs):
                funcWrp.__fDict__[self.__name__] = self
                nobj = obj()
                nobj.__dict__["__name__"] = self.__name__
                nobj.__dict__ = funcWrp.__fDict__
                return func(nobj, *args,**kargs)
            funcWrp.__name__ = func.__name__
            funcWrp.__fDict__ = {}
            funcWrp.__fDict__[self.__name__] = self
            return funcWrp
        pass
    
    def __setattr__(self,name,value):
        self.__dict__[name]=value
        pass
 
    def __call__(self, func):
        if func.__name__!="preFunc" and func.__name__!="postFunc" \
            and func.__name__!="_init" and type(func)==type(lambda t:()):
            func = self.__selfWrp__(func)
            self.__staticDict__[func.__name__] = \
                self.__wrapper__(func.__get__(self,self))
            self.__dict__[func.__name__] = self.__staticDict__[func.__name__]
        elif type(func)==type(lambda t:()):  
            self.__staticDict__[func.__name__] = func.__get__(self,self)
            self.__dict__[func.__name__] = self.__staticDict__[func.__name__]
        else:
            raise SyntaxError("Expected <type 'function'> got "+str(type(func)))
        return func
               
    def disable(self,func_name):
        self.__dict__.pop(func_name)
        pass
        
    def disableAll(self):
        for k in self.__staticDict__:
            self.__dict__.pop(k)
        pass

    def enable(self,func_name):
        self.__dict__[func_name] = self.__staticDict__[func_name]
        pass
    
    def enableAll(self):
        for k in self.__staticDict__:
            self.__dict__[k] = self.__staticDict__[k]
        pass
    
    '''
    when call this function you cannot add disable or enable function you cannot
    disable, enable, add or modify anything you can only use fields or functions.
    '''
    def mkImmutable(self):
        def im(self): pass
        self.__dict__["__call__"]=im
        self.__dict__["disable"]=im
        self.__dict__["disableAll"]=im
        self.__dict__["enable"]=im
        self.__dict__["enableAll"]=im
        self.__dict__["__setattr__"]=im
        
    def version(self):
        return "ModularObj ver. 1.0.0"
    pass

'''
execute a function every event or every [sec] seconds
'''
@ModularObj
class bind:
    def _init(self):
        self.__bindTimeDict__ = {}
        self.__bindEventDict__ = {}
        self.s = socket(AF_UNIX,SOCK_STREAM)
        self.s.bind(socketPath)
        self.s.listen(1)
        Thread(target=self.__bindEvent__, args=()).start()
        Thread(target=self.__bindTime__, args=()).start()
        pass
    
    '''
    bind a function by time you must provide: 
    function reference, how many second must be wait to every execution,
    and a dictionary of key arguments  
    '''
    def time(self, func, sec, **kargs):
        now = int(time.time())
        timer = now+int(sec)
        try:
            self.__bindTimeDict__[timer].append([func,kargs,sec])
        except:
            self.__bindTimeDict__[timer] = [[func,kargs,sec]]
        pass
    
    '''
    bind a function by event name you must provide: 
    function reference, and the event name. 
    when the event occurs the call the function with event arguments.  
    '''
    def event(self, eventName, func):
        try:
            self.__bindEventDict__[str(eventName)].append(func)
        except:
            self.__bindEventDict__[str(eventName)] = [func]
        pass
    
    def __bindTime__(self):
        while True:
            now = int(time.time())
            try:
                liste = self.__bindTimeDict__[now]
                for l in liste:
                    Thread(target=l[0], kwargs=l[1]).start()
                    try:
                        self.__bindTimeDict__[now+l[2]].append([l[0],l[1],l[2]])
                    except:
                        self.__bindTimeDict__[now+l[2]]=[[l[0],l[1],l[2]]]
                self.__bindTimeDict__.pop(now)
            except: pass
            time.sleep(1)
        pass
    
    
    def __bindEvent__(self):
        while True:
            c = self.s.accept()[0]
            part = ""
            BUFF_SIZE = 4096 # 4 KiB
            while True:
                partof = c.recv(BUFF_SIZE)
                part += partof.decode()
                buff = sys.getsizeof(partof)
                if buff<BUFF_SIZE:
                    break
            try:
                event = cPickle.loads(str(part))
                liste = self.__bindEventDict__[event.name]   
                for l in liste:
                    Thread(target=l, kwargs=event.kargs).start()
            except: pass
        pass
    pass

'''
the event is used by the raiseEvent method to load a new event, the event will 
be caught by the binder. the binder call every function binded with that specifical
event.name and pass the arguments stored in event.kargs
'''
class event:
    def __init__(self, name, **kargs):
        self.name=name
        self.kargs = kargs
        
    def __str__(self):
        return cPickle.dumps(self)
        
    