# Giá trị sai số giới hạn
saiso=0.15

def compare_lists(list1, list2, tolerance = saiso):
    # Check if the lists have the same length
    if len(list1) != len(list2):
        return "Không khớp"  # Different lengths cannot match
    temp = 0
    # Compare each pair of elements with the tolerance
    for i in range(len(list1)):
        temp = 0
        if ( abs(list1[i]) > abs(list2[i]) ):
            temp = abs(list1[i])
        else:
            temp = abs(list2[i])
        if abs(list1[i] - list2[i]) > tolerance * temp:
            return "Không khớp"  # Mismatch found

    return "Khớp"  # All elements match within tolerance

# Example usage
list_a = [
3566, -3443, 890, -2560, 888, -2562, 888, -871, 895, -2554, 892, -2557, 860, -2591, 890, -867, 920, -839, 880, -879, 891, -868, 897, -861, 894, -2556, 893, -865, 886, -871, 897, -2554, 854, -905, 890, -867, 879, -880, 879, -2571, 918, -2533, 917, -2533, 891, -2559, 887, -2562, 892, -867, 888
]
list_b = [
3564, -3469, 858, -2560, 855, -2562, 852, -873, 854, -2563, 849, -2566, 856, -2561, 853, -873, 853, -871, 855, -871, 851, -873, 852, -873, 851, -2565, 853, -873, 853, -872, 851, -2566, 856, -869, 851, -874, 852, -873, 852, -2565, 850, -2566, 852, -2590, 851, -2566, 850, -2592, 830, -895, 850
]

result = compare_lists(list_a, list_b)
print(result)  # Output: "Khớp" or "Không khớp"
