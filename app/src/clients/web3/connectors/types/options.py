from pydantic import BaseModel, Field


class DisplayOptions(BaseModel):
    show_collection_metadata: bool = Field(..., alias="showCollectionMetadata")
    show_grand_total: bool = Field(..., alias="showGrandTotal")
    show_unverified_collections: bool = Field(..., alias="showUnverifiedCollections")
    show_raw_data: bool = Field(..., alias="showRawData")
    show_fungible: bool = Field(..., alias="showFungible")
    require_full_index: bool = Field(..., alias="requireFullIndex")
    show_system_metadata: bool = Field(..., alias="showSystemMetadata")
    show_zero_balance: bool = Field(..., alias="showZeroBalance")
    show_closed_accounts: bool = Field(..., alias="showClosedAccounts")


class GetAssetOptions(BaseModel):
    show_collection_metadata: bool = Field(..., alias="showCollectionMetadata")
    show_unverified_collections: bool = Field(..., alias="showUnverifiedCollections")
    show_raw_data: bool = Field(..., alias="showRawData")
    show_fungible: bool = Field(..., alias="showFungible")
    require_full_index: bool = Field(..., alias="requireFullIndex")
    show_system_metadata: bool = Field(..., alias="showSystemMetadata")
    show_native_balance: bool = Field(..., alias="showNativeBalance")
    show_inscription: bool = Field(..., alias="showInscription")


class SearchAssetsOptions(BaseModel):
    show_collection_metadata: bool = Field(
        default=False, alias="showCollectionMetadata"
    )
    show_grand_total: bool = Field(default=False, alias="showGrandTotal")
    show_unverified_collections: bool = Field(
        default=False, alias="showUnverifiedCollections"
    )
    show_raw_data: bool = Field(default=False, alias="showRawData")
    require_full_index: bool = Field(default=False, alias="requireFullIndex")
    show_system_metadata: bool = Field(default=False, alias="showSystemMetadata")
    show_zero_balance: bool = Field(default=False, alias="showZeroBalance")
    show_closed_accounts: bool = Field(default=False, alias="showClosedAccounts")
    show_native_balance: bool = Field(default=False, alias="showNativeBalance")
