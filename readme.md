# Prototype transformer

It's a module of the **petite_stack**

## Whats is that for ?


You have a framework that executes a particular prototype of function but you don't want to bother yourself or the end developper with using the exact prototype, then this will help

This lib will attempt to automatically build an interface layer, for your functions without using the `**kwargs` magic and the dynamic nature of it.

## Example :

```python
from petit_transformer import (BlindBind, Dataclass, RealOptional,
                                    interface_binder_for)


def proto(
    worker: RealOptional[Worker],
    session: RealOptional[Session],
    body: BlindBind[RealOptional[Body]], 
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


## Next points :

Stop using a lambda for the interface and rather completly redefine and evaluate the function with a modified prototype.