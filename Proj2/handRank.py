from collections import Counter

# helper to normalize for suit
def check_suit(hand):
    suits = [card // 13 for card in hand]
    common_suits = Counter(suits).most_common(1)[0][1]
    if (common_suits >= 5):
        return True
    else:
        return False
    
# sliding window solution for checking straights
def check_straight(hand):
    ranks = [card % 13 for card in hand]

    rank_bits = [0] * 14  
    for r in ranks:
        rank_bits[r] = 1
        if r == 0:
            rank_bits[13] = 1

    for i in range(10):
        if sum(rank_bits[i:i+5]) == 5:
            return True, ranks
    return False, ranks

# rank hands with (rank, tiebreak1, tiebreak2...)
# determines score of best hand available of the seven cards
# go from strong to weak so we can short circuit at the first hand found
# returns hand rank plus tiebreaking info so we can easily compare hands

def ranker(hand):

    # first normalize for suit to rule out flushes
    flush = check_suit(hand)

    # then check for straight
    (straight, ranks) = check_straight(hand)

    # for tiebreaking, to compare best cards first
    ranks.sort(reverse=True)

    if flush:
        if straight:
    # Royal Flush: 10
            rf = {8, 9, 10, 11, 12}
            if set(ranks) == rf:
                return 10, ranks

    # Straight Flush: 9
            return 9, ranks

    # from here down we need the most frequent ranks
    freq_ranks = Counter(ranks).most_common()
    (rank1Card, rank1Count) = freq_ranks[0]
    (rank2Card, rank2Count) = freq_ranks[1]

    # Four of a Kind: 8, tiebreak on rank of four
    if rank1Count == 4:
        return 8, rank1Count, ranks

    # Full House: 7
    if rank1Count == 3 and rank2Count == 2:
        return 7, rank1Card, rank2Card # compare who has best trips, then best pair

    # Flush: 6
    if flush:
        return 6, (ranks[0], ranks[1]) # only way to tiebreak flush is on pocket cards
    # assuming first two are pocket cards in descending order

    # Straight: 5, rank of straight included in comparison for tiebreaking
    if straight:
        return 5, ranks

    # Trips: 4, tiebreak on rank of trips, then rest of hand
    if rank1Count == 3:
        return 4, rank1Count, ranks

    # Two Pair: 3
    if rank1Count == 2 and rank2Count == 2:
        return 3, sorted((rank1Card, rank2Card), reverse=True), ranks # order pairs first to compare best pairs

    # One Pair: 2, tiebreak on pair rank, then rest of hand
    if rank1Count == 2:
        return 2, rank1Card, ranks

    # High Card: 1
    return 1, ranks