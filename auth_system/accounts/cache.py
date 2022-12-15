import hashlib

from django.core.cache import cache


def _get_hash_for(value, type):
    """ 
        args: 
            value string: data to hash,
            type string: kind of operation
        returns: hashed result
    """
    hashed_val = ""
    if type == "verify":
        hashed_val = hashlib.sha256(str(value).encode()).hexdigest()[:10] #slicing first nine
    elif type == "reset":  
        hashlib_str = hashlib.sha256(str(value).encode())
        hashed_val = hashlib_str.hexdigest()[-1:-10] #slicing for last nine
    return hashed_val

    
def set_otp_cache_for(otp="", username="", type=""):
    """ 
        args: 
            otp -> key string,
            type string: kind of operation
            username string: user's username to catch
    """
    cache_ttl = 60 * 10 # Time To Live of token in seconds
    
    if type == "verify":
        cache_key = _get_hash_for(otp, type)
        cache.set(cache_key, str(otp), cache_ttl)
    elif type == "reset":
        cache_key = _get_hash_for(otp, type)
        cache.set(cache_key, str(username), cache_ttl)
    
    

def get_cached_otp_for(otp, type):
    """ 
        args: otp -> key string,
            type string: kind of operation
        returns: value of otp or username cached
    """
    cached_otp = "" or 0
    try:
        cache_key = _get_hash_for(otp, type)
        cached_otp = cache.get(cache_key)
    except Exception as e:
        logging.debug(e)
        
    return cached_otp



