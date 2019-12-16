def render_image(raw_input, width, height):
    amount_of_layers = int(len(raw_input) / (width * height))
    image_size = width * height     # for readability
    layers = []
    for i in range(amount_of_layers):
        image = []
        for j in range(height):
            row = list(raw_input[i*image_size+j*width:i*image_size+j*width+width])
            # print(f'New row for layer {i}, height {j}: {row}')
            image.append(row)
        layers.append(image)

    return layers


def part1_solver(image):
    winning_layer = []
    winning_layer_count = 9999999       # Arbitrarily large
    for layer in image:
        zero_count = 0
        for row in layer:
            zero_count += row.count('0')
        if zero_count < winning_layer_count:
            # print(f'New winner! {layer}')
            winning_layer_count = zero_count
            winning_layer = layer
    return winning_layer


if __name__ == '__main__':
    puzzle_input = open('input.txt', 'r').read()
    img = render_image(puzzle_input, 25, 6)

    part1_output_layer = part1_solver(img)
    ones = 0
    twos = 0
    for part1_row in part1_output_layer:
        ones += part1_row.count('1')
        twos += part1_row.count('2')

    print(f'\t-- Part 1 output: {ones * twos}')

