from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from app.utils.helper import generate_random_id

from .enums import (
    AssetSortBy,
    AssetSortDirection,
    Context,
    Interface,
    OwnershipModel,
    RoyaltyModel,
    Scope,
    SearchConditionType,
    TokenType,
    UseMethod,
)
from .options import DisplayOptions, SearchAssetsOptions

## This is for Helius RPC request types
T = TypeVar("T")


class RpcRequest(BaseModel, Generic[T]):
    jsonrpc: str = "2.0"
    id: str = Field(default_factory=generate_random_id)
    method: str
    parameters: T = Field(..., alias="params")

    @classmethod
    def new(cls, method: str, parameters: T) -> "RpcRequest[T]":
        return cls(method=method, parameters=parameters)

    class Config:
        populate_by_name = True
        by_alias = True


class AssetSorting(BaseModel):
    sort_by: AssetSortBy = Field(..., alias="sortBy")
    sort_direction: Optional[AssetSortDirection] = Field(..., alias="sortDirection")


## NOTE: This return both the NFTs and tokens owned by the address
class GetAssetsByOwner(BaseModel):
    owner_address: str = Field(..., alias="ownerAddress")
    page: int
    limit: Optional[int]
    before: Optional[str]
    after: Optional[str]
    display_options: Optional[DisplayOptions] = Field(None, alias="displayOptions")
    sort_by: Optional[AssetSorting] = Field(None, alias="sortBy")
    cursor: Optional[str] = None

    class Config:
        populate_by_name = True


class NotFilter(BaseModel):
    collections: Optional[list[str]] = None
    owners: Optional[list[list[int]]] = None
    creators: Optional[list[list[int]]] = None
    authorities: Optional[list[list[int]]] = None


class SearchAssets(BaseModel):
    negate: Optional[bool] = None
    condition_type: Optional[SearchConditionType] = None
    interface: Optional[Interface] = None
    owner_address: Optional[str] = None
    owner_type: Optional[OwnershipModel] = None
    creator_address: Optional[str] = None
    creator_verified: Optional[bool] = None
    authority_address: Optional[str] = None
    grouping: Optional[tuple[str, str]] = None
    delegate: Optional[str] = None
    frozen: Optional[bool] = None
    supply: Optional[int] = None
    supply_mint: Optional[str] = None
    compressed: Optional[bool] = None
    compressible: Optional[bool] = None
    royalty_target_type: Optional[RoyaltyModel] = None
    royalty_target: Optional[str] = None
    royalty_amount: Optional[int] = None
    burnt: Optional[bool] = None
    sort_by: Optional[AssetSorting] = None
    limit: Optional[int] = None
    page: Optional[int] = None
    before: Optional[str] = None
    after: Optional[str] = None
    json_uri: Optional[str] = None
    not_: Optional[NotFilter] = Field(None, alias="not")
    displayOptions: Optional[SearchAssetsOptions] = Field(None, alias="displayOptions")
    cursor: Optional[str] = None
    name: Optional[str] = None
    collections: Optional[list[str]] = None
    token_type: Optional[TokenType] = None
    tree: Optional[str] = None
    collection_nft: Optional[bool] = None

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class Error(BaseModel):
    code: int
    message: str


## This is for return of helius response types
class RpcResponse(BaseModel, Generic[T]):
    jsonrpc: str
    id: str
    error: Optional[Error] = None
    result: T

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class PriceInfo(BaseModel):
    price_per_token: float
    currency: str
    total_price: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class TokenInfo(BaseModel):
    symbol: Optional[str] = None
    balance: Optional[int] = None
    supply: Optional[int] = None
    decimals: Optional[int] = None
    token_program: Optional[str]
    associated_token_address: Optional[str] = Field(
        None, alias="associatedTokenAddress"
    )
    price_info: Optional[PriceInfo] = None
    mint_authority: Optional[str] = None
    freeze_authority: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class Supply(BaseModel):
    print_max_supply: Optional[int]
    print_current_supply: Optional[int]
    edition_nonce: Optional[int] = None
    edition_number: Optional[int]
    master_edition_mint: Optional[str]

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class Asset(BaseModel):
    interface: Interface
    id: str
    supply: Optional[Supply] = None
    token_info: Optional[TokenInfo] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class AssetError(BaseModel):
    id: str
    error: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class NativeBalance(BaseModel):
    lamports: int
    price_per_sol: float
    total_price: float

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class AssetList(BaseModel):
    grand_total: Optional[int] = None
    total: int
    limit: int
    page: Optional[int] = None
    before: Optional[str] = None
    after: Optional[str] = None
    cursor: Optional[str] = None
    items: list[Asset]
    errors: Optional[list[AssetError]] = None
    nativeBalance: Optional[NativeBalance] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        extra="allow",
    )
