# coding: utf-8
from ape import *
from eth_utils import keccak
from datetime import timedelta
from scripts.proposals import proposals
import click

def print_raw_tx(address, calldata, value):
    print(f"""
Visit https://transact.swiss-knife.xyz/send-tx and input the following:
Address: {address}
Data: 0x{calldata.hex()}
Value: {value}
""")

def print_gov_state(DAO):
    delay = DAO.votingDelay()
    period = DAO.votingPeriod()
    timelock = Contract(DAO.timelock()).getMinDelay()
    threshold = DAO.proposalThreshold()/Contract(DAO.token()).totalSupply()
    quorum = DAO.quorumNumerator()/DAO.quorumDenominator()

    print(
f"""
Governance state ({DAO.address}):
    Voting Delay: {timedelta(seconds=delay)}
    Voting Period: {timedelta(seconds=period)}
    Execution Delay: {timedelta(seconds=timelock)}
    Proposal Threshold: {threshold*100}%
    Proposal Quorum: {quorum*100}%
""")

def get_gov_state(DAO):
    state = {
                "DAO": DAO.address,
                "Voting Delay": DAO.votingDelay(),
                "Voting Period": DAO.votingPeriod(),
                "Execution Delay": Contract(DAO.timelock()).getMinDelay(),
                "Proposal Threshold": DAO.proposalThreshold()/Contract(DAO.token()).totalSupply(),
                "Proposal Quorum": DAO.quorumNumerator()/DAO.quorumDenominator(),
            }
    return state

def print_state_diff(pre, post):
    print(f"State diff for Governance ({pre['DAO']}):")
    for k in pre.keys():
        if pre[k] != post[k]:
            if k in ["Voting Delay", "Voting Period", "Execution Delay"]:
                print(f"\t{k}: {timedelta(seconds=pre[k])}\n\t\t-> {timedelta(seconds=post[k])}")
            elif k in ["Proposal Threshold", "Proposal Quorum"]:
                print(f"\t{k}: {pre[k]*100}%\n\t\t-> {post[k]*100}%")
            else:
                print(f"\t{k}: {pre[k]}\n\t\t-> {post[k]}")

def test_proposal(DAO, payloads, description, tester):
    tester.balance += int(1e18)
    description_hash = keccak(bytes(description, 'utf-8'))

    tx = DAO.propose([i["target"] for i in payloads], [i["value"] for i in payloads], [i["payload"] for i in payloads], description, sender=tester)
    proposalID = tx.events[0]["proposalId"]
    print(f"proposal {proposalID} created")

    delay = DAO.votingDelay()
    print(f"Skipping {timedelta(seconds=delay +1)}")
    chain.pending_timestamp += delay+1
    DAO.castVote(proposalID, 1, sender=tester)
    print("vote mocked")

    period = DAO.votingPeriod()
    print(f"Skipping {timedelta(seconds=period +1)}")
    chain.pending_timestamp += period+1
    DAO.queue([i["target"] for i in payloads], [i["value"] for i in payloads], [i["payload"] for i in payloads], description_hash, sender=tester)
    print("proposal queued")

    timelock = Contract(DAO.timelock()).getMinDelay()
    print(f"Skipping {timedelta(seconds=timelock+1)}")
    chain.pending_timestamp += timelock+1
    DAO.execute([i["target"] for i in payloads], [i["value"] for i in payloads], [i["payload"] for i in payloads], description_hash, sender=tester)
    print("proposal executed")

    return proposalID

def progress_proposal(DAO, payloads, description, sender):
    progressed = False
    description_hash = keccak(bytes(description, 'utf-8'))
    proposalID = DAO.hashProposal([i["target"] for i in payloads], [i["value"] for i in payloads], [i["payload"] for i in payloads], description_hash)
    state = DAO.proposalSnapshot(proposalID)
    if (state != 0): state = DAO.state(proposalID) # idealy I would just querry state and try catch the revert if proposal not created and assign 0 to state

    match state: # as defined by OZ 5.1.0 in IGovernor
        case 0: # not created
            print(f"Creating proposal {proposalID}")
            if sender is not None:
                DAO.propose([i["target"] for i in payloads], [i["value"] for i in payloads], [i["payload"] for i in payloads], description, sender=sender)
            else:
                print_raw_tx(
                    DAO,
                    DAO.propose.encode_input([i["target"] for i in payloads], [i["value"] for i in payloads], [i["payload"] for i in payloads], description),
                    0
                    )
            progressed = True

        case 1: # Pending
            print("Pre voting delay in progress, please wait")

        case 2: # Active
            print("Voting in progress, please wait")

        case 3 | 4: # Canceled or Defeated
            print("proposal either defeated or canceled")

        case 5: # Succeeded
            print(f"Queueing proposal {proposalID}")
            if sender is not None:
                DAO.queue([i["target"] for i in payloads], [i["value"] for i in payloads], [i["payload"] for i in payloads], description_hash, sender=sender)
            else:
                print_raw_tx(
                    DAO,
                    DAO.queue.encode_input([i["target"] for i in payloads], [i["value"] for i in payloads], [i["payload"] for i in payloads], description_hash),
                    0
                    )
            progressed = True

        case 6: # Queued
            if Contract(DAO.timelock()).isOperationReady():
                print(f"Executing proposal {proposalID}")
                if sender is not None:
                    DAO.execute([i["target"] for i in payloads], [i["value"] for i in payloads], [i["payload"] for i in payloads], description_hash, sender=sender)
                else:
                    print_raw_tx(
                        DAO,
                        DAO.execute.encode_input([i["target"] for i in payloads], [i["value"] for i in payloads], [i["payload"] for i in payloads], description_hash),
                        0
                        )
            else:
                print("Proposal still in timelock")
            progressed = True

        case 7: # Expired
            print("Proposal expired, there is nothing to do")

        case 8: # Executed
            print("Proposal already executed, there is nothing to do")

    return progressed


@click.command()
@click.option('--no-account', is_flag=True, help='wether to use your ape account')
@click.option('--skip-test', is_flag=True, help='wether to skip tests')
@click.option('--deploy', is_flag=True, help='wether to deploy&progress')
@click.argument('proposal')
def cli(no_account, skip_test, deploy, proposal):

    with networks.ethereum.mainnet.use_provider("node"):
        DAO, payloads, description = proposals[proposal]()

        if not skip_test:
            pre = get_gov_state(DAO)

            with networks.ethereum.mainnet_fork.use_provider("foundry"):
                test_proposal(DAO, payloads, description, accounts["0x81f9B40Dee106a4C5822aED7641D5C1e2B40F922"])

                post = get_gov_state(DAO)
                print_state_diff(pre, post)

        if deploy:
            if no_account:
                account = None
            else:
                account = select_account("Select an account to use")

            progress_proposal(DAO, payloads, description, account)

