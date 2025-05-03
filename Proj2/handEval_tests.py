from handRank import ranker

# general tests for hand ranker

def encode(card_str):
    rank_str = "23456789TJQKA"
    suit_str = "CDHS"
    rank = rank_str.index(card_str[0])
    suit = suit_str.index(card_str[1])
    return 13 * suit + rank

tests = [

    # Straight Flush vs. Four of a Kind
    ([encode(c) for c in ["9S", "TS", "JS", "QS", "QC"]],
     [encode(c) for c in ["8S", "7S"]],
     [encode(c) for c in ["QH", "QD"]],
     "realist"),

    # Full House vs. Full House (tie-break on trips)
    ([encode(c) for c in ["3C", "3D", "6S", "6H", "7C"]],
     [encode(c) for c in ["3S", "KH"]],
     [encode(c) for c in ["6C", "2D"]],
     "nominalist"),

    # Trips vs. Trips (kicker tie-break)
    ([encode(c) for c in ["7D", "7S", "7C", "2H", "9H"]],
     [encode(c) for c in ["KH", "QH"]],
     [encode(c) for c in ["JH", "TH"]],
     "realist"),

    # Two Pair vs. Two Pair (higher pair wins)
    ([encode(c) for c in ["5C", "5H", "9D", "TC", "2S"]],
     [encode(c) for c in ["7H", "2C"]],
     [encode(c) for c in ["9S", "6H"]],
     "nominalist"),

    # Pocket Aces vs. High Card
    ([encode(c) for c in ["2C", "4D", "6H", "8S", "TD"]],
     [encode(c) for c in ["AH", "AS"]],
     [encode(c) for c in ["KH", "QH"]],
     "realist"),

    # Straight low ace vs. higher straight
    ([encode(c) for c in ["2S", "3C", "4H", "5D", "9S"]],
     [encode(c) for c in ["AS", "KH"]],
     [encode(c) for c in ["6C", "7H"]],
     "nominalist"),

    # Flush vs. Flush (highest card wins)
    ([encode(c) for c in ["2H", "5H", "7H", "9H", "JH"]],
     [encode(c) for c in ["KH", "3H"]],
     [encode(c) for c in ["QH", "4H"]],
     "realist"),

    # Exact tie
    ([encode(c) for c in ["5C", "6D", "7H", "8S", "9C"]],
     [encode(c) for c in ["TS", "JD"]],
     [encode(c) for c in ["TC", "JH"]],
     "tie"),
]

def test_ranker(tests, ranker):
    for i, (river, realist, nominalist, expected) in enumerate(tests):
        realist_full = river + realist
        nominalist_full = river + nominalist

        realist_rank = ranker(realist_full)
        nominalist_rank = ranker(nominalist_full)

        actual = (
            "tie" if realist_rank == nominalist_rank
            else "realist" if realist_rank > nominalist_rank
            else "nominalist"
        )

        print(f"Test {i+1}: expected {expected}, got {actual}")
        assert actual == expected, f"Test {i+1} failed: expected {expected}, got {actual}"

if __name__ == "__main__":
    test_ranker(tests, ranker)