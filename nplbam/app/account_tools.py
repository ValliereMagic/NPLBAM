from flask import Request

USER_LEVEL_MAX: int = 5


class NewAccount:
    # Whether this account creation is valid
    valid: bool = True
    username: str = ""
    password_set: bool = True
    password: str = ""
    user_lvl: int = 0
    # The sets signal whether these optional
    # values are present
    rescue_set: bool = False
    rescue_id: int = 0
    pound_set: bool = False
    pound_id: int = 0


def validate_form_input(request: Request,
                        errors: list,
                        editing_account: bool = False) -> NewAccount:
    """
    Validate the form input for the new_account page.
    """
    global USER_LEVEL_MAX
    # Pull and validate the fields:
    username: str = request.form["username"]
    password: str = request.form["password"]
    password_verify: str = request.form["passwordVerify"]
    user_lvl: str = request.form["userLVL"]
    rescue_id: str = request.form["rescueID"]
    pound_id: str = request.form["poundID"]

    account: NewAccount = NewAccount()
    # Validate username and password:
    if username == "":
        errors.append("A username is required.")
        account.valid = False
    if password == "":
        # We may not be getting a new password, since we could
        # be editing an existing account.
        if not editing_account:
            errors.append("A password is required.")
            account.valid = False
        else:
            account.password_set = False
    if (password != password_verify):
        errors.append("The passwords entered do not match.")
        account.valid = False
    #
    # Will need to verify password strength right here
    # Probably a new function or external library for that
    #
    # They are good, add them to the structure.
    account.username = username
    account.password = password
    # Validate against our user level:
    try:
        user_lvl: int = int(user_lvl)
        if (user_lvl < 0) or (user_lvl > USER_LEVEL_MAX):
            errors.append("User level is out of bounds")
            account.valid = False
    except:
        errors.append("user level wasn't entered or was not a number.")
        account.valid = False
    account.user_lvl = user_lvl
    # Validate our optional fields:
    if rescue_id != "":
        try:
            rescue_id: int = int(rescue_id)
        except:
            errors.append("Rescue ID field filled out, and is not a number.")
            account.valid = False
        account.rescue_id = rescue_id
        account.rescue_set = True
    if pound_id != "":
        try:
            pound_id: int = int(pound_id)
        except:
            errors.append("Pound ID field is filled out, and is not a number.")
            account.valid = False
        account.pound_id = pound_id
        account.pound_set = True
    return account
