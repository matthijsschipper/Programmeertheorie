# test program for state space

# Set global variables
L = 13
B = 17
H = 8
N = 31
sum = 0

total_crossings = L * B * H



# solve 2 dimensional problem
if H == 1:
    grid_corners = 4
    grid_sides = (L - 2) * 2 + (B - 2) * 2
    grid_middle = (L - 2) * (B - 2)
    # loop over possible pathlenths
    for i in range(1, total_crossings - 1):
        if i <= grid_middle:
            sum += i ** 4
        elif i <= (grid_middle + grid_sides):
            sum += grid_middle ** 4 * (i - grid_middle) ** 3
        elif i <= (grid_middle + grid_sides + grid_corners):
            sum += grid_middle ** 4 * grid_sides ** 3 * (i - grid_middle - grid_sides) ** 2


# solve 3 dimensional problem
elif H == 2:
    grid_corners = 8
    grid_sides_4_options = ((L - 2) * 2 + (B - 2) * 2) * 2
    grid_middle = (L - 2) * (B - 2) * H
        # loop over possible pathlenths
    for i in range(1, total_crossings - 1):
        if i <= grid_middle:
            sum += i ** 6
        elif i <= (grid_middle + grid_sides_4_options):
            sum += grid_middle ** 6 * (i - grid_middle) ** 4
        elif i <= (grid_middle + grid_sides_4_options + grid_corners):
            sum += grid_middle ** 6 * grid_sides_4_options ** 4 * (i - grid_middle - grid_sides_4_options) ** 3

else:
    grid_corners = 8
    grid_sides_4_options = ((L - 2) * 2 + (B - 2) * 2) * 2
    grid_sides_5_options = (L * 2 + (B - 2)) * (H - 2)
    grid_middle = (L - 2) * (B - 2) * H
    # loop over possible pathlengths
    for i in range(1, total_crossings - 1):
        if i <= grid_middle:
            sum += i ** 6
        elif i <= (grid_middle + grid_sides_5_options):
            sum += grid_middle ** 6 * (i - grid_middle) ** 5
        elif i <= (grid_middle + grid_sides_5_options + grid_sides_4_options):
            sum += grid_middle ** 6 * (grid_sides_5_options) ** 5 * (i - grid_middle - grid_sides_5_options) ** 4
        elif i <= (grid_middle + grid_sides_5_options + grid_sides_4_options + grid_corners):
            sum += grid_middle ** 6 * grid_sides_5_options ** 5 * grid_sides_4_options ** 4 * (i - grid_middle - grid_sides_5_options - grid_sides_4_options) ** 3

print(f"Het totaal aantal mogelijke wegen voor {N} aantal verbindingen in een {L} x {B} x {H} rechthoek is {N*sum}.")