from ape import *
import scripts.address_book as ab

def setAllDelayTo24H():
    DAO = ab.vl_DAO
    payloads = [
                {
                    "target": ab.vl_DAO,
                    "value": 0,
                    "payload": ab.vl_DAO.setVotingDelay.encode_input(24*60*60),
                }, # set voting delay to 1 day (24*60*60 seconds)
                {
                    "target": ab.vl_DAO,
                    "value": 0,
                    "payload": ab.vl_DAO.setVotingPeriod.encode_input(24*60*60),
                },
                {
                    "target": ab.vl_DAO_timelock,
                    "value": 0,
                    "payload": ab.vl_DAO_timelock.updateDelay.encode_input(24*60*60),
                },
            ]

    description =  """# Make vote long again
While some people complain the governanc is a slow process, 7h from proposal to execution is a bit too fast

As such this proposal will set the voting delay, voting period and execution delay to last 1 day each."""
    return DAO, payloads, description

proposals = {"setAllDelayTo24H": setAllDelayTo24H}
