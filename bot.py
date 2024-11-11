import cv2
import numpy as np
import pyautogui
import time
import os

# Path to templates
script_dir = os.path.dirname(os.path.abspath(__file__))
template_card_path = os.path.join(script_dir, 'templates/card_template.png')  # Generic card template
template_attack_button_path = os.path.join(script_dir, 'templates/attack_button_template.png')  # Attack button
template_defend_button_path = os.path.join(script_dir, 'templates/take_button_template.png')  # Take/defend button
template_lose_screen_path = os.path.join(script_dir, 'templates/lose_screen_template.png')  # Lose screen

# Load templates
template_card = cv2.imread(template_card_path, 0)
template_attack_button = cv2.imread(template_attack_button_path, 0)
template_defend_button = cv2.imread(template_defend_button_path, 0)
template_lose_screen = cv2.imread(template_lose_screen_path, 0)

# Ensure templates are loaded
if template_card is None or template_attack_button is None or template_defend_button is None:
    raise FileNotFoundError(f"One of the template files is missing.")

# Template sizes
w_card, h_card = template_card.shape[::-1]
w_attack, h_attack = template_attack_button.shape[::-1]
w_defend, h_defend = template_defend_button.shape[::-1]

trump_suit = "hearts"


def update_hand_cards():
    hand_cards = []
    for template_name, card in card_templates.items():
        loc = detect_template_on_screen(template_card, threshold=0.8)
        for pt in zip(*loc[::-1]):
            card_position = (pt[0], pt[1])  # Assuming this is the center of the card
            card.position = card_position  # Store position for clicking
            hand_cards.append(card)
    return hand_cards


class Card:
    def __init__(self, value, suit, is_trump=False):
        self.value = value
        self.suit = suit
        self.is_trump = is_trump
        self.position = None

card_templates = {
    # Hearts (non-trump examples; set is_trump=True later if trump suit is hearts)
    "6_hearts": Card(6, "hearts"),
    "7_hearts": Card(7, "hearts"),
    "8_hearts": Card(8, "hearts"),
    "9_hearts": Card(9, "hearts"),
    "10_hearts": Card(10, "hearts"),
    "J_hearts": Card(11, "hearts"),
    "Q_hearts": Card(12, "hearts"),
    "K_hearts": Card(13, "hearts"),
    "A_hearts": Card(14, "hearts"),

    # Diamonds
    "6_diamonds": Card(6, "diamonds"),
    "7_diamonds": Card(7, "diamonds"),
    "8_diamonds": Card(8, "diamonds"),
    "9_diamonds": Card(9, "diamonds"),
    "10_diamonds": Card(10, "diamonds"),
    "J_diamonds": Card(11, "diamonds"),
    "Q_diamonds": Card(12, "diamonds"),
    "K_diamonds": Card(13, "diamonds"),
    "A_diamonds": Card(14, "diamonds"),

    # Clubs
    "6_clubs": Card(6, "clubs"),
    "7_clubs": Card(7, "clubs"),
    "8_clubs": Card(8, "clubs"),
    "9_clubs": Card(9, "clubs"),
    "10_clubs": Card(10, "clubs"),
    "J_clubs": Card(11, "clubs"),
    "Q_clubs": Card(12, "clubs"),
    "K_clubs": Card(13, "clubs"),
    "A_clubs": Card(14, "clubs"),

    # Spades
    "6_spades": Card(6, "spades"),
    "7_spades": Card(7, "spades"),
    "8_spades": Card(8, "spades"),
    "9_spades": Card(9, "spades"),
    "10_spades": Card(10, "spades"),
    "J_spades": Card(11, "spades"),
    "Q_spades": Card(12, "spades"),
    "K_spades": Card(13, "spades"),
    "A_spades": Card(14, "spades"),
}



def detect_template_on_screen(template, threshold=0.9):
    screenshot = pyautogui.screenshot()
    screenshot.save("current_screen.png")
    img = cv2.imread("current_screen.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    print(f"Detected locations for template: {loc}")
    return loc


# Simulate a click on the detected template
# def simulate_click_on_detected(template, width, height, threshold=0.7):
#     loc = detect_template_on_screen(template, threshold)
#     for pt in zip(*loc[::-1]):
#         click_x = pt[0] + width // 2
#         click_y = pt[1] + height // 2
#         print(f"Clicking at: ({click_x}, {click_y})")  # Debug print statement
#         pyautogui.moveTo(click_x, click_y)
#         pyautogui.click()
#         time.sleep(1)
#         return True  # Stop after first detect
#     return False

def simulate_click_on_detected(template, width, height, threshold=0.7):
    loc = detect_template_on_screen(template, threshold)
    for pt in zip(*loc[::-1]):
        click_x = pt[0] + width // 2
        click_y = pt[1] + height // 2
        pyautogui.moveTo(click_x, click_y)
        pyautogui.click()
        time.sleep(1)
        return True
    return False


# the card can be denend
def can_defend(attack_card, defense_card):
    if defense_card.suit == attack_card.suit and defense_card.value > attack_card.value:
        return True
    if defense_card.is_trump and not attack_card.is_trump:
        return True
    return False


def find_defense_card(attack_card, hand_cards):
    for card in hand_cards:
        if can_defend(attack_card, card):
            return card
    return None


def find_attack_card(opponent_cards, hand_cards):
    opponent_values = [card.value for card in opponent_cards]
    hand_cards_sorted = sorted(hand_cards, key=lambda c: (c.suit != trump_suit, c.value))
    for card in hand_cards_sorted:
        if card.value in opponent_values:
            return card
    return hand_cards_sorted[0]


def play_card(card):
    click_x, click_y = card.position
    pyautogui.moveTo(click_x, click_y)
    pyautogui.click()
    time.sleep(1)
    desk_x, desk_y = 800, 400
    pyautogui.moveTo(desk_x, desk_y)
    pyautogui.click()
    time.sleep(1)


def choose_card_for_attack(hand_cards, opponent_card):
    card_to_play = find_attack_card(opponent_card, hand_cards)
    if card_to_play:
        play_card(card_to_play)


def choose_card_for_defense(attack_cards, hand_cards):
    defense_card = find_defense_card(attack_cards, hand_cards)
    if defense_card:
        play_card(defense_card)
    else:
        print("no valid cards ofr defencse")
        simulate_click_on_detected(template_defend_button, w_defend, h_defend)


# Function to check if the game is over
def check_game_over():
    # Look for "lose" screen template
    return simulate_click_on_detected(template_lose_screen, 0, 0)


def game_loop():
    while True:
        hand_cards = update_hand_cards()  # Update hand with current cards
        opponent_card = []  # Define how you retrieve or detect opponent cards for attack

        is_defend_turn = simulate_click_on_detected(template_defend_button, w_defend, h_defend)
        if is_defend_turn:
            print("Opponent is attacking! Selecting defense cards..")
            # You need an `attack_card` to defend against - define it based on game state
            # For now, let's assume the first card in opponent's cards as an attack card
            attack_card = opponent_card[0] if opponent_card else None
            if attack_card:
                choose_card_for_defense([attack_card], hand_cards)
            else:
                print("No attack card detected to defend against.")

        is_attack_turn = simulate_click_on_detected(template_attack_button, w_attack, h_attack)
        if is_attack_turn:
            print("Our turn to attack! Selecting attacking cards..")
            # For attacking, we need `opponent_card` or an empty slot to place a card
            if opponent_card:
                choose_card_for_attack(hand_cards, opponent_card)

        if check_game_over():
            print("Game over. You lost!")
            break
        time.sleep(2)

game_loop()