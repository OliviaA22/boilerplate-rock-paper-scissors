import random


def player(prev_play, opponent_history=[]):

    if not hasattr(player, "my_history"):
        player.my_history = []          # Our own move history
        player.identified_bot = None    # Which opponent strategy we've detected
        player.opp_markov = {}          # 4-move Markov chain: maps 4-move sequences to counter Abbey's move

    # Reset state at the start of a new match.
    if prev_play == "":
        opponent_history.clear()
        player.my_history.clear()
        player.identified_bot = None
        player.opp_markov.clear()
        move = random.choice(["R", "P", "S"])
        player.my_history.append(move)
        return move

    # Record opponent's last move.
    opponent_history.append(prev_play)
    counter = {"R": "P", "P": "S", "S": "R"}

    if player.identified_bot is None:
        # Identify Quincy: if first 5 moves match [R, P, P, S, R]
        if len(opponent_history) >= 5 and opponent_history[:5] == ["R", "P", "P", "S", "R"]:
            player.identified_bot = "quincy"
        # Identify Kris: opponent always counters our previous move.
        elif len(opponent_history) > 1 and all(
            opponent_history[i] == counter[player.my_history[i-1]] for i in range(1, len(opponent_history))
        ):
            player.identified_bot = "kris"
        # Identify Mrugesh: after 10 rounds, if in the last three rounds the opponent often counters our most frequent move.
        elif len(opponent_history) >= 10:
            recent_my = player.my_history[-10:]
            most_freq = max(set(recent_my), key=recent_my.count)
            if opponent_history[-3:].count(counter[most_freq]) >= 2:
                player.identified_bot = "mrugesh"

    if player.identified_bot == "quincy":
        pattern = ["R", "P", "P", "S", "R"]
        next_in_cycle = pattern[len(opponent_history) % 5]
        move = counter[next_in_cycle]
    elif player.identified_bot == "kris":
        last_move = player.my_history[-1]
        move = counter[counter[last_move]]
    elif player.identified_bot == "mrugesh":
        if len(player.my_history) < 10:
            move = random.choice(["R", "P", "S"])
        else:
            recent_my = player.my_history[-10:]
            most_freq = max(set(recent_my), key=recent_my.count)
            move = counter[counter[most_freq]]
    else:
        if len(opponent_history) >= 5:
            key = ''.join(opponent_history[-5:-1])  # last 4 moves form the key
            if key in player.opp_markov:
                predicted = max(player.opp_markov[key], key=player.opp_markov[key].get)
            else:
                predicted = random.choice(["R", "P", "S"])
        else:
            predicted = random.choice(["R", "P", "S"])
        move = counter[predicted]

        if len(opponent_history) >= 5:
            key = ''.join(opponent_history[-5:-1])
            if key not in player.opp_markov:
                player.opp_markov[key] = {}
            player.opp_markov[key][opponent_history[-1]] = player.opp_markov[key].get(opponent_history[-1], 0) + 1

    player.my_history.append(move)
    return move
