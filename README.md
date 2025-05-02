# OPEN DAO

> [!NOTE]
> lazy dev ahead, software might be outdated

An (unoficial) sets of tools to participate in the OPEN index token dao

## installation

Require UV and Foundry

Clone the repo and let uv do the rest for u

```
git clone https://github.com/Rozengarden/OPEN_DAO.git
uv sync
```

## Utilisation

### Managing proposals

run the following command to test and create a proposal.

```
uv run ape run open_gov <PROPOSAL_NAME> --use-account
```

The script will automagically take the proposal to the next stage if possible just rerun the command. For such case skipping the test can be usefull.

```
uv run ape run open_gov <PROPOSAL_NAME> --use-account --skip-test
```

In case u can't connect ur wallet to ape (like me) u can remove the `--use-account` flag to get the raw calldata

### Creating proposal

TODO

## Contribution

Why would u contribute to a vaporware, are u sane anon ?

## TODO

- [ ] add --deploy flag to actualy trigger the deploy&progress logic (usefull when u test) 
- [ ] switch `--use-account` to a `--no-account` flag and invert the logic (just 'cause am the dev doesn't mean I can do bad ux to save me a few keystrokes)
- [ ] some logic to list & select the proposals if none provided
