# Prototype transformer

![Codecov](https://img.shields.io/codecov/c/gh/Plawn/petit_interfacer)
[![GitHub license](https://img.shields.io/github/license/Plawn/petit_interfacer)](https://github.com/Plawn/petit_interfacer/blob/main/LICENSE.TXT)

It's a module of the **petite_stack**

## Whats is that for ?


You have a framework that executes a particular prototype of function but you don't want to bother yourself or the end developper with using the exact prototype, then this will help.

This lib will attempt to automatically build an interface layer, for your functions without using the `**kwargs` magic and the dynamic nature of it.

## Example :

```python
from petit_interfacer import (BlindBind, Dataclass, RealOptional,
                                    interface_binder_for, Dataclass)


def proto(
    worker: RealOptional[Worker],
    session: RealOptional[Session],
    body: BlindBind[RealOptional[Body]], 
    d: Dataclass,
    cookies: RealOptional[Cookies],
): -> Optional[Any]:
...

worker: Worker = ...
session: Session = ...
body: Body = ...
cookies: Cookies = ...
bind_interface = interface_binder_for(proto)

@bind_interface
def example1(body) -> Any:  #notice here that, as body
                            # is BlindBind, we are not obligated to set it's type
    ...

# then you can do 
# without worrying about the user having written the exact prototype
example1(worker=worker, session=session, body=body, cookies=cookies)

@bind_interface
def example2(w: Worker) -> None:
    ...

example2(worker=worker, session=session, body=body, cookies=cookies)

# here we have the same prototype in the end, and we are not using **kwargs, so everything is static
# and any error will raise a warning before your app starts, so no runtime error and less testing required


@bind_interface
def example3(w: Worker, BoDyButStangelyNamed) -> None:
    ...

example3(worker=worker, session=session, body=body, cookies=cookies)

# This will work

@bind_interface
def example3(w, BoDyButStangelyNamed) -> None:
    ...

example3(worker=worker, session=session, body=body, cookies=cookies)


# This will raise an Exception as it can't decide how to bind params together

```


So you see that you can make your life easier, by simply defining the prototype, you want to execute and reliying on static checking and binding.

## Dataclass

As you may know dataclasses does not provide a way to check if a class is a dataclass with `issubclass`, so this libs add the `ClassProxyTest` class which can be inherited in order to add support for other classes.

The petit_interfacer lib provides the support for the dataclasses based on this technique. You can simply import `Dataclass` from it.

If you need to add another custom class / function, then use `ClassProxyTest`:

### Example: How dataclasses is handled:

```python
from petit_interfacer import ClassProxyTest

class Dataclass(ClassProxyTest):
    """As dataclasses does not provide a class to be used with issubclass, we use this proxy to handle it
    """
    def is_correct_type(t: Any) -> bool:
        return is_dataclass(t)

```

## Using it with basic types:

Inherit the type you want to use it with, as without it, the app can't make the difference between two `int` or two `str`


## Next points :

Stop using a lambda for the interface and rather completly redefine and evaluate the function with a modified prototype.