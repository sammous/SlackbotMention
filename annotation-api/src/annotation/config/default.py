DATABASE_DEFAULT = {
    'host_db': 'localhost',
    'user_db': 'root',
    'password_db': 'password',
    'name_db': 'Annotation'
}

VERIFICATION_TOKEN = '***'

PARSERS = {
    'annotate_post': {
        'bundle_errors': True,
        'arguments': [
            {
                'name': 'mention_id',
                'type': str,
                'required': True,
                'help': 'Missing mention id to annotate!'
            },
            {
                'name': 'sentiment',
                'type': str,
                'required': True,
                'help': 'Missing sentiment to annotate!'
            }
        ]
    }
}
