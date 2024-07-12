from enum import Enum


class AssetSortBy(str, Enum):
    id = "id"
    created = "created"
    updated = "updated"
    recent_action = "recent_action"
    none = "none"


class AssetSortDirection(str, Enum):
    asc = "asc"
    desc = "desc"


class Interface(str, Enum):
    V1NFT = "V1_NFT"
    Custom = "Custom"
    V1Print = "V1_PRINT"
    LegacyNFT = "Legacy_NFT"
    V2NFT = "V2_NFT"
    FungibleAsset = "FungibleAsset"
    Identity = "Identity"
    Executable = "Executable"
    ProgrammableNFT = "ProgrammableNFT"
    FungibleToken = "FungibleToken"
    V1PRINT = "V1_PRINT"
    LEGACY_NFT = "LEGACY_NFT"
    Nft = "V2_NFT"
    MplCoreAsset = "MplCoreAsset"
    MplCoreCollection = "MplCoreCollection"


class Context(str, Enum):
    wallet_default = "wallet-default"
    web_desktop = "web-desktop"
    web_mobile = "web-mobile"
    app_mobile = "app-mobile"
    app_desktop = "app-desktop"
    app = "app"
    vr = "vr"


class Scope(str, Enum):
    full = "full"
    royalty = "royalty"
    metadata = "metadata"
    extension = "extension"


class UseMethod(str, Enum):
    Burn = "Burn"
    Single = "Single"
    Multiple = "Multiple"


class OwnershipModel(str, Enum):
    Single = "single"
    Token = "token"


class RoyaltyModel(str, Enum):
    Creators = "creators"
    Fanout = "fanout"
    Single = "single"


class SearchConditionType(str, Enum):
    all = "all"
    any = "any"


class TokenType(str, Enum):
    fungible = "fungible"
    non_fungible = "nonFungible"
    compressed_nft = "compressedNft"
    regular_nft = "regularNft"
    all = "all"


class SearchAssetShowNativeBalance(str, Enum):
    native_balance = "nativeBalance"
