class AuthenticationEvent:

    def __init__(
        self,
        username,
        target_asset,
        result
    ):
        self.username = username
        self.target_asset = target_asset
        self.result = result