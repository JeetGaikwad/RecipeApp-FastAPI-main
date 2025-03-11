class Constants:
    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    MOBILE_NUMBER_REGEX = r"^\+?[1-9]\d{9,14}$"
    PASSWORD_REGEX = (
        r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    )
    PAGE_SIZE = 15
