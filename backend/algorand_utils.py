import logging
from typing import Union
from algosdk import kmd, mnemonic
from algosdk.wallet import Wallet
from algosdk.v2client import algod  
from algosdk import transaction


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

DEFAULT_KMD_WALLET_NAME = "unencrypted-default-wallet"
DEFAULT_KMD_WALLET_PASSWORD = ""
# default_wallet = kmd_algo.create_user_wallet(wallet_name=DEFAULT_KMD_WALLET_NAME, wallet_password=DEFAULT_KMD_WALLET_PASSWORD)

class Algorand:
    """
    Create wallets, list available wallets, fetch account in wallet and query account information
    Also, get passphrase(mnemonic) and public and private keys from mnemonic
    """
    
    def connect_kmd_client(self) -> Union[kmd.KMDClient, None]:
        """
        Connects to the Algorand Key Management Daemon (KMD) client.

        Returns:
            kmd.KMDClient: An instance of the KMDClient if the connection is successful.
            None: If there is an exception during the connection attempt.
        """
        try:
            kmd_address = "http://localhost:4002"
            kmd_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            kmd_client = kmd.KMDClient(kmd_token, kmd_address)

            logging.info("Connected to KMD client successfully.")
            return kmd_client
        
        except Exception as e:
            logging.error(f"Connecting to KMD client failed: {e}")
            return None


    def set_up_algod_client(self):
        try:
            algod_address = "http://localhost:4001" 
            algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"  
            algod_client = algod.AlgodClient(algod_token, algod_address)
            
            logging.info("Connected to algo client successfully.")
            return algod_client
        
        except Exception as e:
            logging.error(f"Connecting to algod client failed: {e}")
            return None

    def create_user_wallet(self, wallet_name, wallet_password):
        """
        Parameters: wallet_name, wallet password
        Returns: Wallet object
        
        Create a Wallet object to manage everything including wallet handles, IDs, and passwords 
        With the Algorand Wallet, users can hold, transact, and request Algos or other assets built on the Algorand blockchain.
        Wallets are collections of addresses and their corresponding keys. 
        Every node can have one or more wallet(s), but only one default wallet.
        """
        client = self.connect_kmd_client()
        try:
            wallet = Wallet(wallet_name, wallet_password, client)
            logging.info("Created wallet successfully")
            return wallet
        except Exception as e:
            logging.error(f"Error creating wallet: {e}")
            return None

    def create_account_address(self, wallet_object):
        """
        Creates an account for the wallet and returns its address
        
        Parameters: wallet_id, wallet_password
        Returns: wallet address
        
        """
        try:
            account_address = wallet_object.generate_key()
            logging.info("Created account address successfully")
            return account_address
        except Exception as e:
            logging.error(f"Error creating account address: {e}")
            return None
    
    def get_account_balance(self, account_address):
        try:
            account_info = self.query_account_information(account_address)
            balance = account_info["amount"]
            logging.info("get account balance successfully")
            return balance
        except Exception as e:
            logging.error(f"Error getting account balance: {e}")
            return None
    
    def query_account_information(self, account_address):
        """
        algod_address is the IP from which API endpoints can be accessed.
        4001 is the default port
        algod_token is an authentication token
        'aaaa.....' is the default value for the sandbox
        
        Parameter: Account address 
        Returns: account information such as address,amount, assets, created-apps, created-assets
        """
        try:
            algod_client = self.set_up_algod_client()
            account_info = algod_client.account_info(account_address) 
            logging.info("get account info successfully")
            return account_info
        except Exception as e:
            logging.error(f"Error getting account info: {e}")
            return None

    def send_alogs_transaction(self, receiver_address, sender_address=None, sender_private_key=None, amount=1000000):
        try:
            algod_client = self.set_up_algod_client()
        
            if sender_address == None:
                default_wallet = self.create_user_wallet(wallet_name=DEFAULT_KMD_WALLET_NAME, wallet_password=DEFAULT_KMD_WALLET_PASSWORD)
                sender_address = default_wallet.list_keys()[0]
                sender_private_key = default_wallet.export_key(sender_address)

            
            # Construct the transaction
            params = algod_client.suggested_params()

            txn = transaction.PaymentTxn(
                sender=sender_address,
                receiver=receiver_address,
                amt=amount,
                sp=params
            )

            # Sign the transaction with the sender's private key
            signed_txn = txn.sign(sender_private_key)

            # Send the transaction to the Algorand network
            tx_id = algod_client.send_transaction(signed_txn)
            logging.info(f"Transaction completed successfully, transaction id: {tx_id}")
            return tx_id
        
        except Exception as e:
            print("Transaction failed:", e)
            return None
        
    def create_user(self, username, password):
        """
        """

        try:
            wallet = self.create_user_wallet(username, password)
            if wallet == None: raise Exception("Error while creating walllet")

            account_address = None

            if len(wallet.list_keys()) == 0:
                account_address = self.create_account_address(wallet)
                if account_address == None: raise Exception("Error while creating account address")

            account_address = wallet.list_keys()[0]

            if self.get_account_balance(account_address) == 0:
                tx_id = self.send_alogs_transaction(account_address)
                if tx_id == None: raise Exception("Error while transfering algos")
            
            logging.info(f"User created successfully")
            return account_address
        
        except Exception as e:
            logging.error(f"Error creating user: {e}")
            return None

    def login_user(self, username, password):
        """
        """

        try:
            wallet = self.create_user_wallet(username, password)
            if wallet == None: raise Exception("Error while creating walllet")

            account_address = None

            if len(wallet.list_keys()) == 0:
                account_address = self.create_account_address(wallet)
                if account_address == None: raise Exception("Error while creating account address")

            account_address = wallet.list_keys()[0]

            if self.get_account_balance(account_address) == 0:
                tx_id = self.send_alogs_transaction(account_address)
                if tx_id == None: raise Exception("Error while transfering algos")
            
            logging.info(f"User login successfully")
            return wallet
        
        except Exception as e:
            logging.error(f"Error login user: {e}")
            return None
        

    def list_wallets(self):
        """    
        Returns: list of wallet objects
        """
        client = self.connect_kmd_client()
        wallets = client.list_wallets()
        return wallets


    def get_passphrase(self, wallet_object):
        """
        Parameter: wallet object
        Returns: Mnemonic phrase

        Public/private key pairs are generated from a single master derivation key. 
        
        Just remember the single mnemonic that represents this master derivation key (i.e. the wallet passphrase/mnemonic) to regenerate all of the accounts in that wallet.

        The master derivation key for the wallet will always generate the same addresses in the same order
        """
        # get the wallet's master derivation key
        mdk = wallet_object.ex
        # get the backup phrase using the master derivation key
        mnemonic_phrase = mnemonic.from_master_derivation_key(mdk)
        return mnemonic_phrase


    def get_public_from_mnemo(self,mnemonic_str):
        """
        Parameter: 25 word passphrase
        Returns: public key
        """
        return mnemonic.to_public_key(mnemonic=mnemonic_str)


    def get_private_from_mnemo(self, mnemonic_str):
        """
        Parameter: 25 word passphrase
        Returns: private key used to sign transactions
        """
        return mnemonic.to_private_key(mnemonic=mnemonic_str)

    def get_private_key(self, wallet, account):
        try:
            private_key = wallet.export_key(account)
            logging.info(f"get private key successfully")
            return private_key
        
        except Exception as e:
            logging.error(f"Error getting private key: {e}")
            return None
  

    
    def create_asset(self, sender_address, sender_private_key, asset_url, asset_name):
        try:
            algod_client = self.set_up_algod_client()
            sp = algod_client.suggested_params()

            txn = transaction.AssetConfigTxn(
                sender=sender_address,
                sp=sp,
                default_frozen=False,
                unit_name="rug",
                asset_name=asset_name,
                manager=sender_address,
                reserve=sender_address,
                freeze=sender_address,
                clawback=sender_address,
                url=asset_url,
                total=1000,
                decimals=0,
            )

            # Sign with secret key of creator
            stxn = txn.sign(sender_private_key)
            txid = algod_client.send_transaction(stxn)
            
            # Wait for the transaction to be confirmed
            results = transaction.wait_for_confirmation(algod_client, txid, 4)
            logging.info(f"Result confirmed in round: {results['confirmed-round']}")
            return results["asset-index"]
        except Exception as e:
            logging.error(f"Error login user: {e}")
            return None

    def opt_in_asset(self, nft_id, sender_address, sender_private_key):
        try:
            algod_client = self.set_up_algod_client()
            sp = algod_client.suggested_params()
            # Create opt-in transaction
            # asset transfer from me to me for asset id we want to opt-in to with amt==0
            optin_txn = transaction.AssetOptInTxn(
                sender=sender_address, sp=sp, index=nft_id
            )
            signed_optin_txn = optin_txn.sign(sender_private_key)
            txid = algod_client.send_transaction(signed_optin_txn)
            logging.info(f"Sent opt in transaction with txid: {txid}")

            # Wait for the transaction to be confirmed
            results = transaction.wait_for_confirmation(algod_client, txid, 4)
            logging.info(f"Result confirmed in round: {results['confirmed-round']}")
            return results
        except Exception as e:
            logging.error(f"Error optin asset: {e}")
            return None

    def transfer_asset(self, sender_address, sender_private_key, receiver_address, nft_id):
      try:
        algod_client = self.set_up_algod_client()
        sp = algod_client.suggested_params()
        # Create transfer transaction
        xfer_txn = transaction.AssetTransferTxn(
            sender=sender_address,
            sp=sp,
            receiver=receiver_address,
            amt=1,
            index=nft_id,
        )
        signed_xfer_txn = xfer_txn.sign(sender_private_key)
        txid = algod_client.send_transaction(signed_xfer_txn)
        logging.info(f"Sent transfer transaction with txid: {txid}")

        results = transaction.wait_for_confirmation(algod_client, txid, 4)
        logging.info(f"Result confirmed in round: {results['confirmed-round']}")
        return results
      except Exception as e:
            logging.error(f"Error transfering asset: {e}")
            return None
        
    def revoke_asset(self, sender_address, sender_private_key, nft_id, receiver_address):
        try:
            algod_client = self.set_up_algod_client()
            sp = algod_client.suggested_params()
            # Create clawback transaction to freeze the asset in acct2 balance
            clawback_txn = transaction.AssetTransferTxn(
                sender=sender_address,
                sp=sp,
                receiver=sender_address,
                amt=1,
                index=nft_id,
                revocation_target=receiver_address,
            )
            signed_clawback_txn = clawback_txn.sign(sender_private_key)
            txid = algod_client.send_transaction(signed_clawback_txn)
            print(f"Sent clawback transaction with txid: {txid}")

            results = transaction.wait_for_confirmation(algod_client, txid, 4)
            print(f"Result confirmed in round: {results['confirmed-round']}")

        except Exception as e:
            logging.error(f"Error transfering asset: {e}")
            return None