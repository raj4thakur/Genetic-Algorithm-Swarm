import numpy as np

def cal_fitness(ind):
    value=0
    for i in ind:
        if 2 == i:
            value+=1
    return value

def sort_individuals(s):
    if len(s) > 1:
        # Finding the middle of the array
        m = len(s) // 2
        # Dividing the array elements into 2 halves
        left = s[:m]
        right = s[m:]
        # Sorting the first half
        sort_individuals(left)
        # Sorting the second half
        sort_individuals(right)
        i = j = k = 0
        # Merging the sorted halves
        while i < len(left) and j < len(right):
            if cal_fitness(left[i]) > cal_fitness(right[j]):
                s[k] = left[i]
                i += 1
            else:
                s[k] = right[j]
                j += 1
            k += 1
        
        # Checking if any element was left in the left half
        while i < len(left):
            s[k] = left[i]
            i += 1
            k += 1
        
        # Checking if any element was left in the right half
        while j < len(right):
            s[k] = right[j]
            j += 1
            k += 1
        return s
    

def selection(population, Np=2 ,method='ranked based'):
    if method == 'ranked based':
        ranked_population=np.array([cal_fitness(i) for i in population])
        ranked_population=ranked_population/np.sum(ranked_population)
        cum_sum=np.cumsum(ranked_population)
        parents=population[np.searchsorted(cum_sum,np.random.rand(Np), side='left')]
        return parents
        

def crossover(ind1,ind2):
    # crossover operation
    crossover_point=np.random.randint(1,50)
    child=np.concatenate((ind1[:crossover_point],ind2[crossover_point:]))
    return child

def mutation(child):
    mutation_point=np.random.randint(0,50)
    child[mutation_point]=np.random.choice((0,1,2))
    return child

def main():
    np.random.seed(4)
    population=np.random.choice((0,1,2),size=(25,50))
    # best fitness of initial population 
    for i in range(10):
        ind1,ind2=selection(population)
        print("",ind1,'\n',ind2)
        print('fitness values of individual 1 and 2:',cal_fitness(ind1),cal_fitness(ind2))
        child=crossover(ind1,ind2)
        # print("New generation:",child)
        # print("Fitness value of the new genertion:",fitness)
        child=mutation(child)
        # print("New generation after mutation:",child)
        # print("Fitness value of the new genertion after mutation:",fitness)
        population=np.append(population,child)
    
    best=0
    for i in range(50):
        if cal_fitness(i)>best:
            best=cal_fitness(i)
    print("best fitness value:",best)

main()

            