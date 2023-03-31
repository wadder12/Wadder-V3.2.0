from nextcord import ButtonStyle
import nextcord
from nextcord.ext import commands
from random import shuffle
from nextcord import ActionRow, Button


DECK = [
    ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8),
    ('9', 9), ('10', 10), ('J', 10), ('Q', 10), ('K', 10), ('A', 11)
] * 4

def draw_card(deck):
    return deck.pop()

def calculate_hand(hand):
    total = 0
    aces = 0
    for card in hand:
        value = card[1]
        if value == 11:
            aces += 1
        total += value

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total

def hand_str(hand):
    return ', '.join(card[0] for card in hand)
def setup(bot):
    
    @bot.slash_command(name="blackjack", description="Play a simple blackjack minigame")
    async def blackjack(interaction: nextcord.Interaction):
        shuffle(DECK)

        player_hand = [draw_card(DECK), draw_card(DECK)]
        dealer_hand = [draw_card(DECK), draw_card(DECK)]

        await interaction.response.send_message(f"Your hand: {hand_str(player_hand)}\nDealer's hand: {dealer_hand[0][0]}, ?")

        while True:
            components = [
    ActionRow(
        Button(style=Button.primary, label="Hit", custom_id="hit"),
        Button(style=Button.primary, label="Stand", custom_id="stand")
    )
]


            await interaction.followup.send("Do you want to `hit` or `stand`?", components=components)

            def check(inter: nextcord.Interaction):
                return inter.author == interaction.author and inter.custom_id in ['hit', 'stand']

            response = await bot.wait_for("button_click", check=check)
            await response.defer_update()

            if response.custom_id == 'hit':
                player_hand.append(draw_card(DECK))
                player_total = calculate_hand(player_hand)

                if player_total > 21:
                    await interaction.followup.send(f"You drew {player_hand[-1][0]}, now your hand is {hand_str(player_hand)} with a total of {player_total}. You busted! Dealer wins!")
                    return
                elif player_total == 21:
                    await interaction.followup.send(f"You drew {player_hand[-1][0]}, now your hand is {hand_str(player_hand)} with a total of {player_total}. You got a blackjack!")
                    break
                else:
                    await interaction.followup.send(f"You drew {player_hand[-1][0]}, now your hand is {hand_str(player_hand)} with a total of {player_total}.")
            else:
                break

        player_total = calculate_hand(player_hand)
        dealer_total = calculate_hand(dealer_hand)

        while dealer_total < 17:
            dealer_hand.append(draw_card(DECK))
            dealer_total = calculate_hand(dealer_hand)

        if dealer_total > 21:
            await interaction.followup.send(f"Dealer's hand: {hand_str(dealer_hand)} with a total of {dealer_total}. Dealer busted! You win!")
        elif dealer_total == player_total:
            await interaction.followup.send(f"Dealer's hand: {hand_str(dealer_hand)} with a total of {dealer_total}. It's a tie!")
        elif dealer_total > player_total:
            await interaction.followup.send(f"Dealer's hand: {hand_str(dealer_hand)} with a total of {dealer_total}. Dealer wins!")
        else:
            await interaction.followup.send(f"Dealer's hand: {hand_str(dealer_hand)} with a total of {dealer_total}. You win!")