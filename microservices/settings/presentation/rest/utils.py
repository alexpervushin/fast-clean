from typing import Dict, Any

def mask_sensitive_config(config: Dict[str, Any]) -> Dict[str, Any]:
    masked_config = config.copy()

    sensitive_keys = ['api_token', 'api_key']

    for key in sensitive_keys:
        if key in masked_config and masked_config[key] is not None:
            masked_config[key] = '********'

    if 'credentials_json' in masked_config:
        if masked_config['credentials_json'] is not None and isinstance(masked_config['credentials_json'], dict):
            masked_config['credentials_json'] = {'status': 'configured (masked)'}
        elif masked_config['credentials_json'] is not None:
             masked_config['credentials_json'] = {'status': 'invalid_format (masked)'}


    return masked_config