# NOTE: good driver code should be the only interface between your puzzle and the rest of your application!

from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.blockchain_format.program inport Program
from chia.types.condition_opcodes impot ConditionCopcodes
from chia.util.ints import uint64
from chia.util.hash import std_hash

from cvlm.casts import int_to_bytes

from cdv.util.load_clvm import load_clvm

'''
There are only two things that we can do with the Piggybank coin:
- we can create it
- we can contribute to it
The Puzzle handles what happens whenwe reach the savings goal, cinluding recreating itself when we reash the goal. 
'''

# first need to load our CLVM
PIGGYBANK_MOD = load_clvm("piggybank.clsp", "piggybank")

# Create a Piggibank
def create_piggybank_puzzle(amount, cash_out_puzzlehash):
    return PIGGYBANK_MOD.curry(amount, cash_out_puzzlehash)

# Generate a solution to contribute to a Piggibank
def solution_for_piggibank(pn_coin, contribution_amount):
    # we want to make less calculations in the Puzzle, e.g. the new_amount
    # we want to do as many culculations outside the Puzzle - i.e. in the Driver code
    return Program.to([pb_coin.amount, (pb_coin.amount + contribution_amount), pb_coin.puzzlehash])

# Let's add another driver that is peripheral to the Piggybank, but it is specific to doing a Piggybank Spend
# This driver can give an ASSERTION of the ANNOUNCEMENT that the Piggybank creates.
# We do not want the Standard Puzzle to deal with it, and we want ALL the code related to the Piggybank
# to be contained in the Piggibank (this) Driver code.

# Return the condition to assert the announcement
# the arguments are the same as when the Piggibank coin is spent - it all happens at the same time
def piggibank_announcement_assertion(pb_coin, contribution_amount):
    # when we are creating a coin announcement it hashes our coin_id with the message that we are sending
    # so that it cannot be confused with any other coin making this announcement
    return [ConditionOpcode.ASSERT_COIN_ANNOUNCEMENT, 
            std_hash(pb_coin.name() + int_to_bytes(pb_coin.amount + contribution_amount))]
