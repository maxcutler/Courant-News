from django import forms

general = {
    'MAINTENANCE_MODE': {
        'default': False,
        'type': forms.BooleanField(
                 label='Do you want to conduct maintenance on your site? While enabled, only logged-in administrators will be able to access your site - all others will see a "Down for maintenance." page.',
                 required=False)
    }
}

ads = {
    'GAM_ACCOUNT_ID': {
       'default': '',
       'type': forms.CharField(
                label="Google Ad Manager Account ID",
                required=False)
   }
}

usersettings = [
    {'General': general},
    {'Ads': ads}
]
