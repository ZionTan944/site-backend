def merge_sort(lst):
    # 1. Store the length of the list
    lst_length = len(lst)

    # 2. List with length less than is already sorted
    if lst_length == 1:
        return lst

    # 3. Identify the list midpoint and partition the list into a left_partition and a right_partition
    mid_point = lst_length // 2

    # 4. To ensure all partitions are broken down into their individual components,
    # the merge_sort function is called and a partitioned portion of the list is passed as a parameter
    left_partition = merge_sort(lst[:mid_point])
    right_partition = merge_sort(lst[mid_point:])

    # 5. The merge_sort function returns a list composed of a sorted left and right partition.
    return merge(left_partition, right_partition)


# 6. takes in two lists and returns a sorted list made up of the content within the two lists
def merge(left, right):
    # 7. Initialize an empty list output that will be populated with sorted elements.
    # Initialize two variables i and j which are used pointers when iterating through the lists.
    output = []
    i = j = 0

    # 8. Executes the while loop if both pointers i and j are less than the length of the left and right lists
    while i < len(left) and j < len(right):
        # 9. Compare the elements at every position of both lists during each iteration
        # left{i] 63 18 73  64 18 59
        if left[i].points > right[j].points:
            output.append(left[i])
            i += 1
        elif left[i].points < right[j].points:
            output.append(right[j])
            j += 1
        elif (
            left[i].points == right[j].points
            and left[i].goal_difference > right[j].goal_difference
        ):
            output.append(left[i])
            i += 1
        elif (
            left[i].points == right[j].points
            and left[i].goal_difference < right[j].goal_difference
        ):
            output.append(right[j])
            j += 1
        elif (
            left[i].goal_difference == right[j].goal_difference
            and left[i].goals_for > right[j].goals_for
        ):
            output.append(left[i])
            i += 1
        elif (
            left[i].goal_difference == right[j].goal_difference
            and left[i].goals_for < right[j].goals_for
        ):
            output.append(right[j])
            j += 1
        else:
            output.append(right[j])
            j += 1
    # 11. The remnant elements are picked from the current pointer value to the end of the respective list
    output.extend(left[i:])
    output.extend(right[j:])

    return output


def run_merge_sort(arr):
    ##    print(unsorted_list)
    sorted_lst = merge_sort(arr)
    # for i in sorted_list:
    #    print(i.Points, i["GD"],i["GF"])
    return sorted_lst


# run_merge_sort(unsorted_list)
