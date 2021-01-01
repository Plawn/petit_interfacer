string = """
def test(): 
    print('yay')
    return None
res['func'] = test
"""

a = {'func':None}

exec(string, {'res':a})
new_func = a ['func']
print(new_func())
