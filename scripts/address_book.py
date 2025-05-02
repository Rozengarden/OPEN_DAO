from ape import *

with networks.ethereum.mainnet.use_provider("node"):
    OPEN = Contract(0x323c03c48660fE31186fa82c289b0766d331Ce21)
    SQUILL = Contract(0x7ebab7190d3d574ce82d29f2fa1422f18e29969c)
    vlSQUILL = Contract(0x2aea77c4757d897aae2710b8a60280777f504e8c)
    basket_DAO = Contract(0xedebefe7179c5fc74853ad30147beecc20860579)
    basket_DAO_timelock = Contract(basket_DAO.timelock())
    non_basket_DAO = Contract(0x020d7c4a87485709d91e78aeeb2b2177ebfbaf41)
    non_basket_DAO_timelock = Contract(non_basket_DAO.timelock())
    vl_DAO = Contract(0x34a5fac531a7576d22df18d6cac89478f5688d90)
    vl_DAO_timelock = Contract(vl_DAO.timelock())
