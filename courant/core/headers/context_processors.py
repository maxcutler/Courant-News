def headers(request):
    """
    Adds variables set by the Headers app to the context.
    """
    return {
        'HEADER_VARS': request.HEADER_VARS
    }