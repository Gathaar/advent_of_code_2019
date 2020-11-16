from tkinter import *


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


def render_visible(image):
    visible = image[0]
    for layer in image[1:]:
        for i in range(len(layer)):
            for j in range(len(layer[0])):
                if visible[i][j] == '2' and layer[i][j] != '2':
                    print(f'Adjusted {i} {j}')
                    visible[i][j] = layer[i][j]
    return visible


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


def part2_solver(image, width, height):
    visible_to_user = render_visible(image)
    app = Tk()
    img_scale = 100
    picture_width = width * img_scale
    picture_height = height * img_scale
    window = Canvas(app, width=picture_width, height=picture_height)
    window.pack()
    colours = {
        '0': '#000000',
        '1': '#FFFFFF',
        '2': '#888888'
    }
    for i in range(height):
        for j in range(width):
            window.create_rectangle(j*img_scale, i*img_scale, j*img_scale+img_scale, i*img_scale+img_scale, fill=colours[visible_to_user[i][j]])
    mainloop()


if __name__ == '__main__':
    puzzle_input = open('input.txt', 'r').read()
    img = render_image(puzzle_input, 25, 6)

    part1_output_layer = part1_solver(img)
    print(f'Part 1 height: {len(part1_output_layer)} -- width: {len(part1_output_layer[0])}')
    ones = 0
    twos = 0
    for part1_row in part1_output_layer:
        ones += part1_row.count('1')
        twos += part1_row.count('2')

    print(f'\t-- Part 1 output: {ones * twos}')

    part2_solver(img, 25, 6)

