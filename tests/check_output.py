def check_output(result, true):
    ''' Checking if calculated output equals expected output
    '''
    if(result == true): print('success')
    else: 
        print('failure')
        print('Expected Output:')
        print(true)
        print('Actual Output:')
        print(result)