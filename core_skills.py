import random
# rand_list =
rand_list = [random.randint(1,20) for _ in range(0, 10)]

# list_comprehension_below_10 =
list_comprehension_below_10 = [num for num in rand_list if num<10]

# list_comprehension_below_10 =
filter_below_10 = list(filter(lambda x: x<10, rand_list))

print(f"Random list {rand_list} \nList Comprehension {list_comprehension_below_10} \nFilter {filter_below_10}")