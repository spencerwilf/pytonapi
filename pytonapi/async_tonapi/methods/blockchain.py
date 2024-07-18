from typing import Optional

from pytonapi.async_tonapi.client import AsyncTonapiClient
from pytonapi.schema.blockchain import Block, Transactions, Transaction, Validators, BlockchainBlock, \
    BlockchainRawAccount, BlockchainAccountInspect, MethodExecutionResult


class BlockchainMethod(AsyncTonapiClient):

    async def get_block_data(self, block_id: str) -> Block:
        """
        Get block data.

        :param block_id: block ID (string), example: "(-1,8000000000000000,4234234)"
        :return: :class:`Block`
        """
        method = f"v2/blockchain/blocks/{block_id}"
        response = await self._get(method=method)

        return Block(**response)

    async def get_transaction_from_block(self, block_id: str) -> Transactions:
        """
        Get transactions from block.

        :param block_id: block ID (string), example: "(-1,8000000000000000,4234234)"
        :return: :class:`Block`
        """
        method = f"v2/blockchain/blocks/{block_id}/transactions"
        response = await self._get(method=method)

        return Transactions(**response)

    async def get_transaction_data(self, transaction_id: str) -> Transaction:
        """
        Get transaction data.

        :param transaction_id: Transaction_id ID (string),
         example: "97264395BD65A255A429B11326C84128B7D70FFED7949ABAE3036D506BA38621"
        :return: :class:`Transaction`
        """
        method = f"v2/blockchain/transactions/{transaction_id}"
        response = await self._get(method=method)

        return Transaction(**response)

    async def get_transaction_by_message(self, msg_id: str) -> Transaction:
        """
        Get transaction data by message hash.

        :param msg_id: message ID
        :return: :class:`Transaction`
        """
        method = f"v2/blockchain/messages/{msg_id}/transaction"
        response = await self._get(method=method)

        return Transaction(**response)

    async def get_validators(self) -> Validators:
        """
        Get blockchain validators.

        :return: :class:`Validators`
        """
        method = f"v2/blockchain/validators"
        response = await self._get(method=method)

        return Validators(**response)

    async def get_last_masterchain_block(self) -> BlockchainBlock:
        """
        Get last known masterchain block.

        :return: :class:`BlockchainBlock`
        """
        method = f"v2/blockchain/masterchain-head"
        response = await self._get(method=method)

        return BlockchainBlock(**response)

    async def get_account_info(self, account_id: str) -> BlockchainRawAccount:
        """
        Get low-level information about an account taken directly from the blockchain.

        :param account_id: Account ID
        :return: :class:`BlockchainRawAccount`
        """
        method = f"v2/blockchain/accounts/{account_id}"
        response = await self._get(method=method)

        return BlockchainRawAccount(**response)

    async def get_account_transactions(self, account_id: str, after_lt: Optional[int] = None,
                                       before_lt: int = 0, limit: int = 100) -> Transactions:
        """
        Get account transactions.

        :param account_id: account ID
        :param after_lt: omit this parameter to get last transactions
        :param before_lt: omit this parameter to get last transactions
        :param limit: Default value : 100
        :return: :class:`Transactions`
        """
        method = f"v2/blockchain/accounts/{account_id}/transactions"
        params = {'before_lt': before_lt, 'limit': limit}
        if after_lt is not None:
            params['after_lt'] = after_lt
        response = await self._get(method=method, params=params)

        return Transactions(**response)

    async def inspect_account(self, account_id: str) -> BlockchainAccountInspect:
        """
        Blockchain account inspect.

        :param account_id: account ID
        :return: :class:`BlockchainAccountInspect`
        """
        method = f"v2/blockchain/accounts/{account_id}/inspect"
        response = await self._get(method=method)

        return BlockchainAccountInspect(**response)

    async def execute_get_method(self, account_id: str, method_name: str,
                                 args: Optional[str] = None
                                 ) -> MethodExecutionResult:
        """
        Execute get method for account.

        :param account_id: account ID
        :param method_name: contract get method name
        :param args: contract get method args
        """
        method = f"v2/blockchain/accounts/{account_id}/methods/{method_name}"
        params = {'args': args} if args else {}
        response = await self._get(method=method, params=params)

        return MethodExecutionResult(**response)
