#Prime Sieve

#Uses the Sieve of Eratosthenes
#https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes

#Can search to any number, but it may take several seconds if the number is larger than 4 digits


from time import time

#the index, i, is used in place of a list containing all items

n=int(input('Enter a number to search to'))

#generate list
#numbers=[]
status=[True, True]
primes=[]
c=1
while c<n:
    #numbers.append(i)
    status.append(False)
    c+=1

timer_start=time()

#search the list until all items are marked
while False in status:
    
    #find the first unmarked item
    i=2
    while not status[i]==False:
        i+=1
        
    #mark the item, add to primes
    status[i]=True
    primes.append(i)
    print(i, 'is prime')
    
    
    #mark multiples of i that are >=i^2 and <=n
    c=i**2
    while c<=n:
        print(c)
        status[c]=True
        c+=i


#Finished, print results
timer_end=time()
print('\nDone\n\nFound', len(primes), 'primes between 0 and', str(n)+'.\n\nPrimes:')
print(primes)
total_time=timer_end-timer_start
print('\nTime taken:', total_time, 'seconds')
    
        
