import * as algokit from '@algorandfoundation/algokit-utils'
import { useWallet } from '@txnlab/use-wallet'
import algosdk from 'algosdk'
import { useSnackbar } from 'notistack'
import { useState } from 'react'
import { getAlgodConfigFromViteEnvironment } from '../utils/network/getAlgoClientConfigs'

interface TransactInterface {
  openModal: boolean
  setModalState: (value: boolean) => void
}

const CreateAsset = ({ openModal, setModalState }: TransactInterface) => {
  const [loading, setLoading] = useState<boolean>(false)
  const [receiverAddress, setReceiverAddress] = useState<string>('')
  const [pinataUrl, setPinataUrl] = useState<string>('')

  const algodConfig = getAlgodConfigFromViteEnvironment()
  const algodClient = algokit.getAlgoClient({
    server: algodConfig.server,
    port: algodConfig.port,
    token: algodConfig.token,
  })

  const { enqueueSnackbar } = useSnackbar()

  const { signer, activeAddress, signTransactions, sendTransactions } = useWallet()

  const handleSubmitAlgo = async () => {
    setLoading(true)

    if (!signer || !activeAddress) {
      enqueueSnackbar('Please connect wallet first', { variant: 'warning' })
      return
    }

    const suggestedParams = await algodClient.getTransactionParams().do()

    // const transaction = algosdk.makeAssetConfigTxnWithSuggestedParamsFromObject({

    // })
    const transaction = algosdk.makeAssetCreateTxnWithSuggestedParamsFromObject({
      from: activeAddress,
      suggestedParams: suggestedParams,
      assetURL: pinataUrl,
      assetName: "Certificate",
      unitName: 'algo',
      total: 0,
      decimals: 0,
      defaultFrozen: false
    })

    const encodedTransaction = algosdk.encodeUnsignedTransaction(transaction)

    const signedTransactions = await signTransactions([encodedTransaction])

    const waitRoundsToConfirm = 4

    try {
      enqueueSnackbar('Sending transaction...', { variant: 'info' })
      const { id } = await sendTransactions(signedTransactions, waitRoundsToConfirm)
      enqueueSnackbar(`Transaction sent: ${id}`, { variant: 'success' })
      setReceiverAddress('')
      alert(transaction.toString())
    } catch (e) {
      enqueueSnackbar('Failed to send transaction', { variant: 'error' })
    }

    setLoading(false)
  }

  return (
    <dialog id="transact_modal" className={`modal ${openModal ? 'modal-open' : ''} bg-slate-200`}>
      <form method="dialog" className="modal-box">
        <h3 className="font-bold text-lg">Create Trainee Certificate</h3>
        <br />
        {/* <input
          type="text"
          data-test-id="receiver-address"
          placeholder="Provide wallet address"
          className="input input-bordered w-full"
          value={receiverAddress}
          onChange={(e) => {
            setReceiverAddress(e.target.value)
          }}
        /> */}
         <input
          type="text"
          data-test-id="pinata-url"
          placeholder="Provide Pinata Asset Url"
          className="input input-bordered w-full"
          value={pinataUrl}
          onChange={(e) => {
            setPinataUrl(e.target.value)
          }}
        />
        <div className="modal-action ">
          <button className="btn" onClick={() => setModalState(!openModal)}>
            Close
          </button>
          <button
            data-test-id="send-algo"
            className={`btn lo`}
            onClick={handleSubmitAlgo}
          >
            {loading ? <span className="loading loading-spinner" /> : 'Create Certificate'}
          </button>
        </div>
      </form>
    </dialog>
  )
}

export default CreateAsset
