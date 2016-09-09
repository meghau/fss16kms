"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""
from __future__ import division, print_function
from Card import *
import sys


class PokerHand(Hand):

    def suit_hist(self):
        """Builds a histogram of the suits that appear in the hand.

        Stores the result in attribute suits.
        """
        self.suits = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1

    def rank_hist(self):
        """Builds a histogram of the ranks that appear in the hand.

        Stores the result in attribute ranks.
        """
        self.ranks = {}
        for card in self.cards:
            self.ranks[card.rank] = self.ranks.get(card.rank, 0) + 1
            
    def group_by_suit(self):
        self.suit_groups = {}
        for card in self.cards:
            if card.suit not in self.suit_groups:
                self.suit_groups[card.suit] = [card.rank]
            else:
                self.suit_groups[card.suit].append(card.rank)
            
    def has_n_of_a_kind(self,n):
        """Returns True if the hand has n of a kind, False otherwise.
        """
        self.rank_hist()
        for val in self.ranks.values():
            if val == n:
                return True
        return False
    
    def has_pair(self):
        """Returns True if the hand has a pair, False otherwise.
        """
        return self.has_n_of_a_kind(2)
        
    def has_twopair(self):
        """Returns True if the hand has two pair, False otherwise.
        """
        self.rank_hist()
        found_first_pair = False
        for val in self.ranks.values():
            if val >= 2:
                if found_first_pair:
                    return True
                found_first_pair = True
        return False
    
    def has_three_of_a_kind(self):
        """Returns True if the hand has three of a kind, False otherwise.
        """
        return self.has_n_of_a_kind(3)
    
    def has_straight(self):
        """Returns True if the hand has a straight, False otherwise.
        """
        self.rank_hist()
        count = 0
        for r in xrange(1,15):
            rank = (r % 14) if r < 14 else 1
            if rank in self.ranks:
                count += 1
                if count >= 5:
                    return True
            else:
                count = 0
        return False
        
    def has_flush(self):
        """Returns True if the hand has a flush, False otherwise.
      
        Note that this works correctly for hands with more than 5 cards.
        """
        self.suit_hist()
        for val in self.suits.values():
            if val >= 5:
                return True
        return False
    
    def has_fullhouse(self):
        """Returns True if the hand has a full house, False otherwise.
        """
        self.rank_hist()
        found_two = found_three = False
        for val in self.ranks.values():
            if val == 2:
                found_two = True
            elif val == 3:
                found_three = True
            if found_three and found_two:
                return True
        return False
    
    def has_four_of_a_kind(self):
        """Returns True if the hand has four of a kind, False otherwise.
        """
        return self.has_n_of_a_kind(4)
        
    def has_straightflush(self):
        """Returns True if the hand has a straight flush, False otherwise.
        """
        self.group_by_suit()
        for suit in self.suit_groups.keys():
            card_list = self.suit_groups[suit]
            count = 0
            for r in xrange(1,15):
                rank = (r % 14) if r < 14 else 1
                if rank in card_list:
                    count += 1
                    if count >= 5:
                        return True
                else:
                    count = 0
        return False
    
    def has_five_of_a_kind(self):
        """Returns True if the hand has five of a kind, False otherwise.
        """
        return self.has_n_of_a_kind(5)
    
    def classify(self):
        """Classify the hand.
        """
        self.label = 'High Card'
        if self.has_five_of_a_kind():
            self.label = 'Five of a Kind'
        elif self.has_straightflush():
            self.label = 'Straight Flush'
        elif self.has_four_of_a_kind():
            self.label = 'Four of a Kind'
        elif self.has_fullhouse():
            self.label = 'Full House'
        elif self.has_flush():
            self.label = 'Flush'
        elif self.has_straight():
            self.label = 'Straight'
        elif self.has_three_of_a_kind():
            self.label = 'Three of a Kind'
        elif self.has_twopair():
            self.label = 'Two pair'
        elif self.has_pair():
            self.label = 'Pair'
        
def estimate_probability(num_hands, num_cards):
    classification_count = {}
    for i in xrange(num_hands):
        deck = Deck()
        deck.shuffle()
        hand = PokerHand()
        deck.move_cards(hand, num_cards)
        hand.classify()
        classification_count[hand.label] = classification_count.get(hand.label, 0) + 1
    print("Label\t\t\tProbability")
    for label, count in classification_count.items():
        print("%s" % (label+str(count/num_hands).rjust(30-len(label))))
        
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python PokerHand.py <number-of-hands> <number-of-cards-in-hand>")
        print("number-of-cards-in-hand = 5 or 7")
        exit(1)
    
    num_hands = int(sys.argv[1])
    num_cards = int(sys.argv[2])
    estimate_probability(num_hands,num_cards)