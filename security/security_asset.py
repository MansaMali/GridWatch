class SecurityAsset:
    def __init__(
            self,
            asset_id,
            asset_type,
            ip_address,
            criticality
    ):
        self.asset_id = asset_id
        self.asset_type = asset_type
        self.ip_address = ip_address
        self.criticality = criticality
        self.status = "ONLINE"
        