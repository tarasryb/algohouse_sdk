class Connection:
    """

    Algohouse Connection class
    :param user_email: e-mail of the Algohouse user who registered as API user
    :param signkey: the key to sign the request
    """

    def __init__(self, user_email: str, signkey: str):
        self.__user_email = user_email
        self.__signkey = signkey

    @property
    def user_email(self):
        return self.__user_email

    @property
    def signkey(self):
        return self.__signkey

