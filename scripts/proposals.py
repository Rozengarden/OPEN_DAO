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

As such this proposal will set the voting delay, voting period and execution delay to last 1 day each.

See https://github.com/Rozengarden/OPEN_DAO/blob/ab2d5c7ed79ce8104c011a06c6473511bc2b1d8e/scripts/proposals.py for implementation"""

    return DAO, payloads, description

def set_vlDAO_Delays():
    DAO = ab.vl_DAO
    payloads = [
                {
                    "target": ab.vl_DAO,
                    "value": 0,
                    "payload": ab.vl_DAO.setVotingDelay.encode_input(2 * 24 * 60 * 60),
                }, # set voting delay to 2 day (2*24*60*60 seconds)
                {
                    "target": ab.vl_DAO,
                    "value": 0,
                    "payload": ab.vl_DAO.setVotingPeriod.encode_input(3 * 24 * 60 * 60),
                }, # set voting period to 3 day (3*24*60*60 seconds)
                {
                    "target": ab.vl_DAO_timelock,
                    "value": 0,
                    "payload": ab.vl_DAO_timelock.updateDelay.encode_input(2 * 24 * 60 * 60),
                }, # set execution delay to 2 day (2*24*60*60 seconds)
            ]

    description =  """# Adjust the vlDAO delays

> target: vlDAO

Currently the vlDAO can expediate a vote in 7h. Which is both a risk of governance attack and a problem to coordinate voters (see the [first ever proposal on this DAO who collected 0 votes](https://app.reserve.org/ethereum/index-dtf/0x323c03c48660fe31186fa82c289b0766d331ce21/governance/proposal/26436857730956334062589037166126567845454062707908893165812112571719833847097) )

As such this proposal will set the voting delay to two day, the voting period to three day and the execution delay to last two day for the vlDAO.

## TL;DR:

**vlDAO:**
| Parameter       | Before  | After  |
| --------------- | ------- | ------ |
| voting delay    | 2 hours | 2 days |
| voting period   | 3 hours | 3 days |
| execution delay | 2 hours | 2 days |

See https://github.com/Rozengarden/OPEN_DAO/blob/main/scripts/proposals.py for implementation"""

    return DAO, payloads, description


proposals = {"setAllDelayTo24H": setAllDelayTo24H,
             "set_vlDAO_Delays": set_vlDAO_Delays}
