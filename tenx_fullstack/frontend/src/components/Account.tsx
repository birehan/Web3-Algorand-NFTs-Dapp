import { useWallet } from '@txnlab/use-wallet'
import { useMemo } from 'react'
import { ellipseAddress } from '../utils/ellipseAddress'
import { getAlgodConfigFromViteEnvironment } from '../utils/network/getAlgoClientConfigs'

const Account = () => {
  const { activeAddress, getAssets } = useWallet()
  const algoConfig = getAlgodConfigFromViteEnvironment()

  const dappFlowNetworkName = useMemo(() => {
    return algoConfig.network === '' ? 'sandbox' : algoConfig.network.toLocaleLowerCase()
  }, [algoConfig.network])

  const getAssetsFunc = async () => {
    const assets = await getAssets()
    console.log(assets)
  }

  getAssetsFunc()

  return (
    <div>
      <a
        className="text-xl"
        target="_blank"
        href={`https://app.dappflow.org/setnetwork?name=${dappFlowNetworkName}&redirect=explorer/account/${activeAddress}/`}
      >
        Address: {ellipseAddress(activeAddress)}
      </a>
      <div className="text-xl">Network: {algoConfig.network === '' ? 'localnet' : algoConfig.network}</div>
    </div>
  )
}

export default Account
