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


class PriceInfo(BaseModel):
    price_per_token: float
    currency: str
    total_price: Optional[float] = None


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


class Inscription(BaseModel):
    order: int
    size: int
    content_type: str
    encoding: str
    validation_hash: str
    inscription_data_account: str
    authority: str


class FileQuality(BaseModel):
    schema: str = Field(..., alias="$$schema")

    model_config = ConfigDict(
        populate_by_name=True,
    )


class File(BaseModel):
    uri: Optional[str] = None
    mime: Optional[str] = None
    cdn_uri: Optional[str] = None
    quality: Optional[FileQuality] = None
    contexts: Optional[list[Context]] = None


class Attribute(BaseModel):
    value: Any
    trait_type: str


class Metadata(BaseModel):
    attributes: Optional[list[Attribute]] = None
    description: Optional[str] = None
    name: Optional[str] = None
    symbol: Optional[str] = None


class Links(BaseModel):
    external_url: Optional[str] = None
    image: Optional[str] = None
    animation_url: Optional[str] = None


class Content(BaseModel):
    schema_: str = Field(..., alias="$schema")
    json_uri: str
    files: Optional[list[File]] = None
    metadata: Metadata
    links: Optional[Links] = None

    class Config:
        populate_by_name = True


class Authorities(BaseModel):
    address: str
    scopes: list[Scope]


class CollectionMetadata(BaseModel):
    name: Optional[str] = None
    symbol: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    external_url: Optional[str] = None


class Group(BaseModel):
    group_key: str
    group_value: Optional[str] = None
    verified: Optional[bool] = None
    collection_metadata: Optional[CollectionMetadata] = None


class Compression(BaseModel):
    eligible: bool
    compressed: bool
    data_hash: str
    creator_hash: str
    asset_hash: str
    tree: str
    seq: int
    leaf_id: int


class Creator(BaseModel):
    address: str
    share: int
    verified: bool


class Royalty(BaseModel):
    royalty_model: RoyaltyModel
    target: Optional[str] = None
    percent: float
    basis_points: int
    primary_sale_happened: bool
    locked: bool


class Ownership(BaseModel):
    frozen: bool
    delegated: bool
    delegate: Optional[str] = None
    ownership_model: OwnershipModel
    owner: str


class Uses(BaseModel):
    use_method: UseMethod
    remaining: int
    total: int


class Supply(BaseModel):
    print_max_supply: Optional[int]
    print_current_supply: Optional[int]
    edition_nonce: Optional[int] = None
    edition_number: Optional[int]
    master_edition_mint: Optional[str]

    class Config:
        populate_by_name = True


class GroupDefinition(BaseModel):
    group_key: str
    group_value: Optional[str] = None
    size: Optional[int] = None
    asset_id: list[int]


class MplCoreInfo(BaseModel):
    num_minted: Optional[int] = None
    current_size: Optional[int] = None
    plugins_json_version: Optional[int] = None


class Asset(BaseModel):
    interface: Interface
    id: str
    content: Optional[Content] = None
    authorities: Optional[list[Authorities]] = None
    compression: Optional[Compression] = None
    grouping: Optional[list[Group]] = None
    royalty: Optional[Royalty] = None
    creators: Optional[list[Creator]] = None
    ownership: Ownership
    uses: Optional[Uses] = None
    supply: Optional[Supply] = None
    mutable: bool
    burnt: bool
    mint_extensions: Optional[Any] = None
    token_info: Optional[TokenInfo] = None
    group_definition: Optional[GroupDefinition] = None
    plugins: Optional[Any] = None
    unknown_plugins: Optional[Any] = None
    mpl_core_info: Optional[MplCoreInfo] = None

    class Config:
        populate_by_name = True


class AssetError(BaseModel):
    id: str
    error: str


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

    class Config:
        populate_by_name = True
