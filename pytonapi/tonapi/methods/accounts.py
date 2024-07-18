from typing import List, Optional, Dict

from pytonapi.schema.events import AccountEvents, AccountEvent
from pytonapi.tonapi.client import TonapiClient
from pytonapi.schema._address import Address
from pytonapi.schema.accounts import Account, Accounts, FoundAccounts, Subscriptions, DnsExpiring, PublicKey, \
    BalanceChange
from pytonapi.schema.domains import DomainNames
from pytonapi.schema.jettons import JettonsBalances
from pytonapi.schema.nft import NftItems
from pytonapi.schema.traces import TraceIds


class AccountMethod(TonapiClient):

    def get_info(self, account_id: str) -> Account:
        """
        Get human-friendly information about an account without low-level details.

        :param account_id: Account ID
        :return: :class:`Account`
        """
        method = f"v2/accounts/{account_id}"
        response = self._get(method=method)

        return Account(**response)
    
    def parse_address(self, account_id: str) -> Address:
        """
        Parse an address
        """
        method = f"v2/address/{account_id}/parse"
        response = self._get(method=method)
        return response

    def get_bulk_info(self, account_ids: List[str]) -> Accounts:
        """
        Get human-friendly information about multiple accounts without low-level details.

        :param account_ids: List of account IDs
        return: :class:`Accounts`
        """
        method = f"v2/accounts/_bulk"
        params = {"account_ids": account_ids}
        response = self._post(method=method, body=params)

        return Accounts(**response)

    def search_by_domain(self, name: str) -> FoundAccounts:
        """
        Search by account domain name.

        :param name: domain name
        :return: :class:`Account`
        """
        method = f"v2/accounts/search"
        params = {"name": name}
        response = self._get(method=method, params=params)

        return FoundAccounts(**response)

    def get_domains(self, account_id: str) -> DomainNames:
        """
        Get domains for wallet account.

        :param account_id: account ID
        :return: :class:`DomainNames`
        """
        method = f"v2/accounts/{account_id}/dns/backresolve"
        response = self._get(method=method)

        return DomainNames(**response)

    def get_jettons_balances(self, account_id: str) -> JettonsBalances:
        """
        Get all Jettons balances by owner address.

        :param account_id: account ID
        :return: :class:`JettonsBalances`
        """
        method = f"v2/accounts/{account_id}/jettons"
        response = self._get(method=method)

        return JettonsBalances(**response)

    def get_jettons_history(self, account_id: str, limit: int = 100, before_lt: Optional[int] = None,
                            accept_language: str = "en", subject_only: bool = False,
                            start_date: Optional[int] = None, end_date: Optional[int] = None
                            ) -> AccountEvents:
        """
        Get the transfer jettons history for account.

        :param account_id: account ID
        :param limit: Default value : 100
        :param before_lt: omit this parameter to get last events
        :param accept_language: Default value : en
        :param subject_only: Default value : False
        :param start_date: Default value : None
        :param end_date: Default value : None
        :return: :class:`AccountEvents`
        """
        method = f"v2/accounts/{account_id}/jettons/history"
        params = {"limit": limit}
        if before_lt: params["before_lt"] = before_lt  # noqa:E701
        if subject_only: params["subject_only"] = "true"  # noqa:E701
        if start_date: params["start_date"] = start_date  # noqa:E701
        if end_date: params["end_date"] = end_date  # noqa:E701
        headers = {"Accept-Language": accept_language}
        response = self._get(method=method, params=params, headers=headers)

        return AccountEvents(**response)

    def get_jettons_history_by_jetton(self, account_id: str, jetton_id: str,
                                      limit: int = 100, before_lt: Optional[int] = None,
                                      accept_language: str = "en", subject_only: bool = False,
                                      start_date: Optional[int] = None, end_date: Optional[int] = None
                                      ) -> AccountEvents:
        """
        Get the transfer jetton history for account and jetton.


        :param account_id: account ID
        :param jetton_id: jetton ID
        :param limit: Default value : 100
        :param before_lt: omit this parameter to get last events
        :param accept_language: Default value : en
        :param subject_only: Default value : False
        :param start_date: Default value : None
        :param end_date: Default value : None
        :return: :class:`AccountEvents`
        """
        method = f"v2/accounts/{account_id}/jettons/{jetton_id}/history"
        params = {"limit": limit}
        if before_lt: params["before_lt"] = before_lt  # noqa:E701
        if subject_only: params["subject_only"] = "true"  # noqa:E701
        if start_date: params["start_date"] = start_date  # noqa:E701
        if end_date: params["end_date"] = end_date  # noqa:E701
        headers = {"Accept-Language": accept_language}
        response = self._get(method=method, params=params, headers=headers)

        return AccountEvents(**response)

    def get_nfts(self, account_id: str, limit: int = 1000, offset: int = 0,
                 collection: str = None, indirect_ownership: bool = False) -> NftItems:
        """
        Get NFT items by owner address.

        :param account_id: account ID
        :param limit: Default value : 1000
        :param offset: Default value : 0
        :param collection: filter NFT by collection address
        :param indirect_ownership: Selling nft items in ton implemented usually via transfer items
         to special selling account. This option enables including items which owned not directly.
        :return: :class:`NftItems`
        """
        method = f"v2/accounts/{account_id}/nfts"
        params = {
            "limit": limit, "offset": offset,
            'indirect_ownership': 'true' if indirect_ownership else 'false'
        }
        if collection: params["collection"] = collection  # noqa:E701
        response = self._get(method=method, params=params)

        return NftItems(**response)

    def get_all_nfts(self, account_id: str, collection: str = None, indirect_ownership: bool = True) -> NftItems:
        """
        Get all NFT items by owner address.

        :param account_id: account ID
        :param collection: filter NFT by collection address
        :param indirect_ownership: Selling nft items in ton implemented usually via transfer items
         to special selling account. This option enables including items which owned not directly.
        :return: :class:`NftItems`
        """
        nft_items = []
        offset, limit = 0, 1000

        while True:
            result = self.get_nfts(
                account_id=account_id, limit=limit, offset=offset,
                collection=collection, indirect_ownership=indirect_ownership,
            )
            nft_items += result.nft_items
            offset += limit

            if len(result.nft_items) != limit:
                break

        return NftItems(nft_items=nft_items)

    def get_traces(self, account_id: str, limit: int = 100) -> TraceIds:
        """
        Get traces for account.

        :param account_id: account ID
        :param limit: Default value : 100
        :return: :class:`TraceIds`
        """
        method = f"v2/accounts/{account_id}/traces"
        params = {"limit": limit}
        response = self._get(method=method, params=params)

        return TraceIds(**response)

    def get_event(self, account_id: str, event_id: str, accept_language: str = "en",
                  subject_only: Optional[bool] = False) -> AccountEvent:
        """
        Get event for an account by event_id

        :param account_id: account ID
        :param event_id: event ID
        :param accept_language: Default value : en
        :param subject_only: Default value : False
        :return: :class:`AccountEvent`
        """
        method = f"v2/accounts/{account_id}/events/{event_id}"
        params = {"subject_only": subject_only} if subject_only else {}
        headers = {"Accept-Language": accept_language}
        response = self._get(method=method, params=params, headers=headers)

        return AccountEvent(**response)

    def get_events(self, account_id: str, limit: int = 100, before_lt: Optional[int] = None,
                   accept_language: str = "en", subject_only: Optional[bool] = False,
                   start_date: Optional[int] = None, end_date: Optional[int] = None
                   ) -> AccountEvents:
        """
        Get events for an account. Each event is built on top of a trace which is a series of transactions
        caused by one inbound message. TonAPI looks for known patterns inside the trace and splits the trace
        into actions, where a single action represents a meaningful high-level operation like a Jetton
        Transfer or an NFT Purchase. Actions are expected to be shown to users. It is advised not to build
        any logic on top of actions because actions can be changed at any time.

        :param account_id: account ID
        :param limit: Default value : 100
        :param before_lt: omit this parameter to get last events
        :param accept_language: Default value : en
        :param subject_only: Default value : False
        :param start_date: Default value : None
        :param end_date: Default value : None
        :return: :class:`AccountEvents`
        """
        method = f"v2/accounts/{account_id}/events"
        params = {"limit": limit}
        if before_lt: params["before_lt"] = before_lt  # noqa:E701
        if subject_only: params["subject_only"] = "true"  # noqa:E701
        if start_date: params["start_date"] = start_date  # noqa:E701
        if end_date: params["end_date"] = end_date  # noqa:E701
        headers = {"Accept-Language": accept_language}
        response = self._get(method=method, params=params, headers=headers)

        return AccountEvents(**response)

    def get_nft_history(self, account_id: str, limit: int = 100, before_lt: Optional[int] = None,
                        accept_language: str = "en", subject_only: bool = False,
                        start_date: Optional[int] = None, end_date: Optional[int] = None
                        ) -> AccountEvents:
        """
        Get the transfer nft history.

        :param account_id: account ID
        :param limit: Default value : 100
        :param before_lt: omit this parameter to get last events
        :param accept_language: Default value : en
        :param subject_only: Default value : False
        :param start_date: Default value : None
        :param end_date: Default value : None
        :return: :class:`AccountEvents`
        """
        method = f"v2/accounts/{account_id}/nfts/history"
        params = {"limit": limit}
        if before_lt: params["before_lt"] = before_lt  # noqa:E701
        if subject_only: params["subject_only"] = "true"  # noqa:E701
        if start_date: params["start_date"] = start_date  # noqa:E701
        if end_date: params["end_date"] = end_date  # noqa:E701
        headers = {"Accept-Language": accept_language}
        response = self._get(method=method, params=params, headers=headers)

        return AccountEvents(**response)

    def get_subscriptions(self, account_id: str) -> Subscriptions:
        """
        Get all subscriptions by wallet address

        :param account_id: account ID
        :return: :class:`Subscriptions`
        """
        method = f"v2/accounts/{account_id}/subscriptions"
        response = self._get(method=method)

        return Subscriptions(**response)

    def get_expiring_dns(self, account_id: str, period: Optional[int] = None) -> DnsExpiring:
        """
        Get expiring account .ton dns.

        :param account_id: account ID
        :param period: number of days before expiration
        :return: :class:`DnsExpiring`
        """
        method = f"v2/accounts/{account_id}/dns/expiring"
        params = {"period": period} if period else {}
        response = self._get(method=method, params=params)

        return DnsExpiring(**response)

    def get_public_key(self, account_id: str) -> PublicKey:
        """
        Get public key by account id.

        :param account_id: account ID
        :return: :class:`PublicKey`
        """
        method = f"v2/accounts/{account_id}/publickey"
        response = self._get(method=method)

        return PublicKey(**response)

    def get_balance_change(self, account_id: str, start_date: int, end_date: int) -> BalanceChange:
        """
        Get account's balance change.

        :param account_id: account ID
        :param start_date: start date
        :param end_date: end date
        :return: :class:`BalanceChange`
        """
        method = f"v2/accounts/{account_id}/diff"
        params = {"start_date": start_date, "end_date": end_date}
        response = self._get(method=method, params=params)

        return BalanceChange(**response)

    def reindex(self, account_id: str) -> bool:
        """
        Update internal cache for a particular account

        :param account_id: account ID
        :return: :class:`bool`
        """
        method = f"v2/accounts/{account_id}/reindex"
        response = self._post(method=method)

        return bool(response)
