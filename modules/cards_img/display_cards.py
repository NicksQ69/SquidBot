from PIL import Image
import os

print('display_cards import success !')

def get_folder():
    return os.path.dirname(__file__)


def load_card(cardTuple):
    cardPath = get_folder()+ "\\" + cardTuple[1] + ".jpg"
    return Image.open(cardPath)

def load_stack():
    stack_path = get_folder() + "\\stack.png"
    return  Image.open(stack_path)

def get_position(row, column, card_index = None, cards_number = None):

    card_width = 50
    card_height = 67
    horizontal_gap = 40
    vertical_gap1 = 24
    vertical_gap2 = 25
    cards_disparity = 35

    if card_index == None or cards_number == None:


        position1 = (column*(horizontal_gap+card_width) + horizontal_gap, row*(vertical_gap2+card_height) + vertical_gap1)
        position2 = (position1[0] + card_width, position1[1] + card_height)

    else:

        position1 = (int(column*(horizontal_gap+card_width)  + horizontal_gap + ((cards_number - card_index - 1)*cards_disparity / (cards_number - 1))), row*(vertical_gap2+card_height) + vertical_gap1)
        position2 = (position1[0] + card_width, position1[1] + card_height)

    print(position1+position2)
    return position1 + position2


def get_current_round(up_last_card, middle_last_card, down_last_card):


    if up_last_card[0] > middle_last_card[0] and up_last_card[0] > down_last_card[0]:

        return up_last_card[0]

    elif middle_last_card[0] > down_last_card[0]:

        return middle_last_card[0]

    else:

        return down_last_card[0]


def paste_card(cardTuple, position, stack):
    card_image = load_card(cardTuple)
    stack.paste(card_image,position)
    return stack

def create_image(up_row, middle_row, down_row):

    stack = load_stack()

    current_round = get_current_round(up_row[-1], middle_row[-1], down_row[-1])

    print('appelle de paste_middle_row:\n')
    stack = paste_middle_row(middle_row, current_round, stack)
    print('appelle de paste_down_row:\n')
    stack = paste_border_row(down_row, 2, current_round, stack)
    stack = paste_border_row(up_row, 0, current_round, stack)
    stack.save(get_folder() + "\\temp.png")


def paste_middle_row(middle_row, current_round, stack):

    row = 1

    for index in range(-1, -5, -1):

        if index <= -len(middle_row):

            return stack

        card_tuple = middle_row[index]
        column = 3 - (current_round - card_tuple[0])

        if column <= 3 and column >= 0:

            stack = paste_card(card_tuple, get_position(row, column), stack)

    return stack

def paste_border_row(row_list, row_number, current_round, stack):

    stop_round = current_round - 4
    index = -1

    while index >= -len(row_list):


        previous_index = index
        card_tuple = row_list[index]
        card_round = card_tuple[0]

        if card_tuple[0] <= stop_round:

            break

        while card_round == card_tuple[0]:

            index = index - 1
            if index < -len(row_list):

                break

            card_tuple = row_list[index]


        print(index)
        print(previous_index)
        cards_number = previous_index - index
        print('cards_number')
        print(cards_number)
        column = 3 - (current_round - card_round)
        if cards_number == 1:
            card_tuple = row_list[previous_index]
            if card_tuple[0] == 0:
                return stack
            stack = paste_card(card_tuple, get_position(row_number, column), stack)

        else:
            for x in range(previous_index, index, -1):


                card_tuple = row_list[x]

                card_index = -(x - previous_index)
                print('card_index')
                print(card_index)
                stack = paste_card(card_tuple, get_position(row_number, column, card_index, cards_number), stack)

    return stack


if __name__ == '__main__':
    up_row = [(0, '3_Spades')]
    middle_row = [(0, '3_Spades'),  (1, '5_Hearts')]
    down_row = [(0, '3_Spades'),]
    print(get_folder())
    create_image(up_row, middle_row, down_row)
